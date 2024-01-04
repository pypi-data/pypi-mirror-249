import os
from pathlib import Path
import json
import webbrowser
from threading import Timer
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, jsonify
from flask_cors import CORS

from spectraclassify import logger
from spectraclassify.utility.utils import save_json
from spectraclassify.utility import config_manager
from spectraclassify.training_service import start_training, show_training_results

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')
app = Flask(__name__)
app.secret_key = "abc"
CORS(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    logger.info("Home page")

    if request.method == 'POST':
        print('Post request recived')
        # print(request.form)
        config_dict = request.form.to_dict()
        # print(config_dict)
        save_json(path=Path('configs.json'), data=config_dict)
        logger.info('saving config json file')
        logger.info('Training started')
        mode_configaration = config_manager.get_model_conf()
        data_configaration = config_manager.get_data_conf()
        start_training(model_conifg=mode_configaration,
                       data_config=data_configaration)
        flash('Training started. Please wait and check your terminal for more details.')
        logger.info('Training complete')
    return render_template('home.html')


def open_browser():
    webbrowser.open_new('http://127.0.0.1:8080/')
    print("Opening browser")


def runnapplication():
    Timer(1, open_browser).start()
    app.run(host="127.0.0.1", port=8080, debug=False, use_reloader=False)


if __name__ == "__main__":
    """
        runnapplication() it is a function which is responsible for running the flask application.
    """
    runnapplication()
