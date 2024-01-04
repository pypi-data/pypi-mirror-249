'''
@author: Shanjidul Islam Sadhin
Email: sadhin.aiub.cse@gmail.com
Date: 31-dec-2023
'''

"""
This file is responsible for the training of the model define by the user.
Such as:
    - Model training
    - Model evaluation
    - Show training results
    - Model save
"""




import os
import sys
import numpy as np
import tensorflow as tf
from spectraclassify import logger, get_unique_file_name
from spectraclassify.utility import data_manager
from spectraclassify.utility.model_builder import get_model
from spectraclassify.utility.keras_callbacks import get_callbacks


def start_training(model_conifg: dict, data_config: dict):
    try:
        logger.info("Getting model {}".format(model_conifg['MODEL_NAME']))
        print("Getting model {}".format(model_conifg['MODEL_NAME']))

        _model = get_model(name=model_conifg['MODEL_NAME'],
                           freeze_layer=model_conifg['FREEZE_LAYER'],
                           no_of_classes=data_config['CLASSES'],
                           lr=model_conifg['LEARNING_RATE'],
                           optimizer_fn_name=model_conifg['OPTIMIZER'],
                           loss_fn_name=model_conifg['LOSS']
                           )

        if _model is None:
            logger.error("Error loading model")
            print("Error loading model")
            sys.exit(1)

        logger.info("")
        training_data, validation_data = data_manager.get_data_generator(
            training_dir=data_config['TRAINING_DIR'],
            validation_dir=data_config['VALIDATION_DIR'],
            target_size=data_config['IMG_SIZE'],
            batch_size=data_config['BATCH_SIZE'],
            do_augmentation=bool(data_config['AUGMENTATION'])
        )

        CBS = get_callbacks()
        steps_per_epoch = training_data.samples // training_data.batch_size
        validation_steps = validation_data.samples // validation_data.batch_size
        logger.info("Training model started..")

        _model.fit(
            training_data,
            epochs=model_conifg['EPOCHS'],
            validation_data=validation_data,
            steps_per_epoch=steps_per_epoch,
            validation_steps=validation_steps,
            callbacks=CBS)

        saved_model_path = get_unique_file_name(
            f"{model_conifg['MODEL_NAME']}", "keras")
        os.makedirs('Trained_model', exist_ok=True)
        saved_model_path = os.path.join("Trained_model", saved_model_path)

        logger.info(f"Trained model saved path: {saved_model_path}")
        _model.save(saved_model_path)
        print(f"Model saved at the following location : {saved_model_path}")
        # showing the model performance.
        show_training_results(saved_model_path, validation_data, model_conifg, data_config, False)

    except Exception as err:
        logger.error(f"Error in training model: {err}")


def show_training_results(model_path: str, val_data: None, model_conifg: dict, data_config: dict, show_results: bool = False):
    # evaluateing the model

    try:
        _classes = data_manager.input_classes(
            training_dir=data_config['TRAINING_DIR'],
            batch_size=data_config['BATCH_SIZE'],
            target_size=data_config['IMG_SIZE'],
            do_augmentation=bool(data_config['AUGMENTATION'])
        )
        if val_data:
            logger.info("Loading the trained model {}".format(
                model_conifg['MODEL_NAME']))
            print("Loading the trained model {}".format(
                model_conifg['MODEL_NAME']))
        else:
            _, val_data = data_manager.get_data_generator(
                training_dir=data_config['TRAINING_DIR'],
                validation_dir=data_config['VALIDATION_DIR'],
                target_size=data_config['IMG_SIZE'],
                batch_size=data_config['BATCH_SIZE'],
                do_augmentation=bool(data_config['AUGMENTATION'])
            )

        _model = tf.keras.models.load_model(model_path)

        logger.info("Evaluating the model")
        print("Evaluating the model")
        l, a = _model.evaluate(val_data)

        logger.info("Loss: {}".format(l))
        logger.info("Accuracy: {}".format(a))

        if show_results:
            logger.info("Predicting the model")
            print("Predicting the model")
            predictions = _model.predict(val_data)

            logger.info("Showing the results")
            print("Showing the results")
            for i in range(len(predictions)):
                logger.info("Prediction: {}".format(
                    _classes[np.argmax(predictions[i])]))
                print("Prediction: {}".format(
                    _classes[np.argmax(predictions[i])]))

    except Exception as err:
        logger.error(f"Error in model evaluation: {err}")
