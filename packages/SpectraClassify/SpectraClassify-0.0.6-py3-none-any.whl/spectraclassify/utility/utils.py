import os
import yaml
import joblib
import json
import base64
from typing import Any
from pathlib import Path
from box import ConfigBox
from ensure import ensure_annotations
from box.exceptions import BoxValueError
from spectraclassify import logger


def decodeImage(img_string, fileName):
    try:
        imgdata = base64.b64decode(img_string)
        with open(fileName, 'wb') as f:
            f.write(imgdata)
            f.close()
    except Exception as e:
        logger.error(e)
        raise e


def encode_Image_to_Base64(croppedImagePath):
    try:
        with open(croppedImagePath, "rb") as f:
            return base64.b64encode(f.read())
    except Exception as e:
        logger.error(e)
        raise e


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Read the yaml file and returns
    Args:
        path_to_yaml (str): path like input
    Raise:
        ValueError: if yaml file is empty
        e: empty file
    :return:
        ConfigBox: ConfigBox type
    """

    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully!")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError(f"{path_to_yaml} file is empty")
    except Exception as e:
        logger.error(e)
        raise e


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """
    Create list of directories
    Args:
    path_to_directories (list): list of path of directories
    ignore_log (bool, optional): ignore if multiple dirs is to be created.

    :return: None
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Created directory at : {path}")


@ensure_annotations
def save_json(path: Path, data: dict):
    """
    Save json data
    :param path: path of the json file
    :param data: data to be saved in json file
    :return:
    """
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        logger.info(f"Json file saved at: {path}")
    except Exception as e:
        logger.error(e)
        raise e


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """
    load a json files data
    :param path: path to the json file
    :return:
        ConfigBox: data as class attributes instead of dict
    """
    try:
        with open(path) as f:
            content = json.load(f)

        logger.info(f"json file loaded successfully from: {path}")
        return ConfigBox(content)
    except Exception as e:
        logger.error(e)
        raise e


@ensure_annotations
def get_size(path: Path) -> str:
    """get size in KB

    Args:
        path (Path): path of the file

    Returns:
        str: size in KB
    """
    try:
        size_in_kb = round(os.path.getsize(path) / 1024)
        return f"~ {size_in_kb} KB"
    except Exception as e:
        logger.error(e)
        raise e
