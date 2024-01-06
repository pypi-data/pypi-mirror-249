# this file is responsive for the management of configuration of the model and the data is passed by the user
import os
import pathlib
import sys
import yaml
import json
import warnings
from spectraclassify import logger
from spectraclassify.utility.utils import load_json

loss = ""
__file__ = 'configs.json'


def get_data_conf() -> dict:
    try:
        __path = pathlib.Path.joinpath(pathlib.Path(
            __file__).parent.absolute(), __file__)
        if __path.exists():
            print(f"Loading configs.json from {__path}")
        else:
            __path.write_text("")
        PARAMS = load_json(__path)
        training_dir = pathlib.Path(PARAMS['Training_Dir'])
        validation_dir = pathlib.Path(PARAMS['Validation_Dir'])
        classes = int(PARAMS['Classes'])
        img_size = PARAMS['Image_Size'].split(',')
        h = int(img_size[0])
        w = int(img_size[1])
        channels = int(img_size[2])
        batch_size = int(PARAMS['Batch_Size'])
        augmentation = bool(PARAMS['Augmentation'])
        CONFIG = {
            'TRAINING_DIR': pathlib.Path(training_dir),
            'VALIDATION_DIR': validation_dir,
            'CLASSES': classes,
            'IMG_SIZE': (h, w, channels),
            'BATCH_SIZE': int(batch_size),
            'AUGMENTATION': bool(augmentation)
        }
    except Exception as err:
        logger.error(f"Error in get_Data_conf: {err}")
        CONFIG = {
            'TRAINING_DIR': None,
            'VALIDATION_DIR': None,
            'CLASSES': 0,
            'IMG_SIZE': (0, 0, 0),
            'BATCH_SIZE': 0,
            'AUGMENTATION': None
        }
    return CONFIG


def get_model_conf() -> dict:
    try:
        __path = pathlib.Path.joinpath(pathlib.Path(
            __file__).parent.absolute(), __file__)
        if __path.exists():
            print(f"Loading configs.json from {__path}")
        else:
            __path.write_text("")
        PARAMS = load_json(__path)

        model_name = PARAMS['Model_Name']
        epochs = int(PARAMS['Epochs'])

        learning_rate = float(PARAMS['Learning_Rate'])

        freeze_layer = bool(PARAMS['Freeze_Layer'])
        optimizer = PARAMS['Optimizer']
        loss = PARAMS['Loss']

        CONFIG = {
            'MODEL_NAME': model_name,
            'FREEZE_LAYER': freeze_layer,
            'EPOCHS': int(epochs),
            'LEARNING_RATE': float(learning_rate),
            'OPTIMIZER': optimizer,
            'LOSS': loss
        }
    except Exception as err:
        logger.error(f"Error in get_model_conf: {err}")
        CONFIG = {
            'MODEL_NAME': None,
            'FREEZE_LAYER': None,
            'EPOCHS': None,
            'LEARNING_RATE': None,
            'OPTIMIZER': None,
            'LOSS': None
        }
    return CONFIG
