'''
@author: Shanjidul Islam Sadhin
Email: sadhin.aiub.cse@gmail.com
Date: 29-dec-2023
'''

import os
import sys
import logging
import time


TRAINED_MODEL_PATH = "E:\Projects\SpectraClassify\spectraclassify\Trained_model\VGG16_20240105_222128.keras"   # Path: latest trained model path
CLASSES={0:'cat',1:'dog'}              # list: class indexs of the training data

logging_str = "[%(asctime)s]: %(levelname)s: %(module)s: %(message)s"
log_dir = "logs"
log_filesPath = os.path.join(log_dir, "running_logs.log")
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(level=logging.INFO,
                    format=logging_str,
                    handlers=[
                        logging.FileHandler(log_filesPath),
                        logging.StreamHandler(sys.stdout)
                    ])

logger = logging.getLogger("spectraclassify")


def set_trained_model_path(path: str):
    global TRAINED_MODEL_PATH   # Use the global TRAINED_MODEL_PATH variable
    TRAINED_MODEL_PATH = path


def get_trained_model_path() -> str:
    return TRAINED_MODEL_PATH

def set_classes(classes: dict):
    global CLASSES
    CLASSES = classes


def get_classes() -> dict:
    return CLASSES


def get_unique_file_name(prefix: str, ext: str = "log") -> str:
    return f"{prefix}_{time.strftime('%Y%m%d_%H%M%S')}.{ext}"
