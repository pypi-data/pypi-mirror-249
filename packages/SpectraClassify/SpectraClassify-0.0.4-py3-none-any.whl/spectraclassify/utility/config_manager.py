# this file is responsive for the management of configuration of the model and the data is passed by the user
import os
import pathlib
import sys
import yaml
import json
import warnings
from spectraclassify import logger
from spectraclassify.utility.utils import load_json

training_dir = ""
validation_dir = ""
classes = 0
model_name = ''
img_size = (0, 0, 0)
h = 0
w = 0
channels = 0
epochs = 2
batch_size = 2
augmentation = False
freeze_layer = False
learning_rate = 0.0
optimizer = ""
loss = ""
__file__ = 'configs.json'
try:
    __path = pathlib.Path.joinpath(pathlib.Path(
        __file__).parent.absolute(), __file__)
    if __path.exists():
        print(f"Loading configs.json from {__path}")
    else:
        __path.write_text("")
    PARAMS = load_json(__path)

    # user passed configuration data
    training_dir = pathlib.Path(PARAMS['Training_Dir'])
    validation_dir = pathlib.Path(PARAMS['Validation_Dir'])
    classes = int(PARAMS['Classes'])
    img_size = PARAMS['Image_Size'].split(',')
    h = int(img_size[0])
    w = int(img_size[1])
    channels = int(img_size[2])
    model_name = PARAMS['Model_Name']
    epochs = int(PARAMS['Epochs'])
    batch_size = int(PARAMS['Batch_Size'])
    learning_rate = float(PARAMS['Learning_Rate'])
    augmentation = bool(PARAMS['Augmentation'])
    freeze_layer = bool(PARAMS['Freeze_Layer'])
    optimizer = PARAMS['Optimizer']
    loss = PARAMS['Loss']

except Exception as err:
    logger.error(f" Error loading configs.json: {err}")


def get_data_conf(
        training_dir=training_dir,
        validation_dir=validation_dir,
        classes=classes,
        h=h, w=w, channels=channels, batch_size=batch_size, augmentation=augmentation) -> dict:
    try:
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


def get_model_conf(
        model_name=model_name,
        epochs=epochs,
        freeze_layer=freeze_layer,
        learning_rate=learning_rate,
        optimizer=optimizer,
        loss=loss) -> dict:
    try:
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
