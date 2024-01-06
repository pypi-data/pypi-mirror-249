
import os
import numpy as np
from pathlib import Path
import base64
import cv2
import webbrowser
from threading import Timer
from flask_cors import CORS, cross_origin
from flask import Flask, render_template, request, flash, jsonify
from spectraclassify.utility import config_manager
from spectraclassify.utility.utils import save_json, decodeImage
from spectraclassify.training_service import start_training
from spectraclassify.prediction_service import PrecictionService
from spectraclassify import logger, get_trained_model_path, get_classes, set_trained_model_path, set_classes

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')
app = Flask(__name__)
app.secret_key = "abc"
CORS(app)


@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def home():
    logger.info("Home page")

    if request.method == 'POST':
        print('Post request recived')
        config_dict = request.form.to_dict()
        save_json(path=Path('configs.json'), data=config_dict)
        logger.info('saving config json file')

        logger.info('Training started')
        model_cfg = config_manager.get_model_conf()
        data_cfg = config_manager.get_data_conf()
        temp_model_path, temp_classes = start_training(
            model_config=model_cfg, data_config=data_cfg)

        set_trained_model_path(temp_model_path)
        set_classes(temp_classes)

        flash('Training started. Please wait and check your terminal for more details.')
        logger.info('Training complete')
    return render_template('home.html')


@app.route("/predict", methods=['GET', 'POST'])
@cross_origin()
def prediction():
    logger.info("Prediction page")
    if request.method == 'POST':
        img_base64 = request.json.get('image')
        decodeImage(img_base64, 'input_image.jpg')
        # model_cfg = config_manager.get_model_conf()
        data_cfg = config_manager.get_data_conf()
        result = PrecictionService(
            model_path=get_trained_model_path(),
            classes=get_classes()
        ).predict('input_image.jpg', do_preprocess=True, target_size=data_cfg['IMG_SIZE'])

        logger.info(f"result: {result}")
        return jsonify(result)
    return render_template('prediction.html')


@app.route("/wecam", methods=['GET', 'POST'])
@cross_origin()
def webcam():
    return render_template('webcam.html')


@app.route('/analyze', methods=['POST'])
@cross_origin()
def analyze():
    # Extract the base64 image from the POST request
    image_data = request.form['imageBase64'].split(',')[1]
    decoded_img = base64.b64decode(image_data)

    # Correct way to convert string to np array
    nparr = np.frombuffer(decoded_img, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Load configuration and preprocess the image
    data_cfg = config_manager.get_data_conf()
    x = cv2.resize(img, dsize=data_cfg['IMG_SIZE'][:-1])
    x = np.expand_dims(x, axis=0)

    # Predict the class
    result = PrecictionService(model_path=get_trained_model_path(),
                               classes=get_classes()).predict(do_preprocess=False, x=x)

    # Display the result on the image
    cv2.putText(img, result, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Convert the image back to base64 to send as JSON
    _, buffer = cv2.imencode('.jpg', img)
    jpg_as_text = base64.b64encode(buffer).decode("utf-8")

    return jsonify(img_base64=jpg_as_text)


def open_browser():
    webbrowser.open_new('http://127.0.0.1:8080/')
    print("Opening browser")


def runnapplication():
    # application = UserApplication()
    Timer(1, open_browser).start()
    app.run(host="127.0.0.1", port=8080, debug=True,  use_reloader=False)


if __name__ == "__main__":
    """
        runnapplication() it is a function which is responsible for running the flask application.
    """
    runnapplication()
