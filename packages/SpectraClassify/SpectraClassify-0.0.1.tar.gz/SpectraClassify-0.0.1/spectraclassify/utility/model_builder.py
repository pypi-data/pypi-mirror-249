"""
This file is responsive for the management of the model passed by the user.
Such as:
    - Model architecture
    - Model weights
    - Model optimizer
    - Model loss function
    - Model metrics
"""

import os
import sys
import numpy as np
import tensorflow as tf
from spectraclassify import logger
from spectraclassify.utility.config_manager import get_model_conf, get_Data_conf
from spectraclassify.utility.pretrained_models import get_pretrained_model

model_conifg = get_model_conf()
data_config = get_Data_conf()


def load_pretrain_model(model_name: str = model_conifg['MODEL_NAME']):
    try:
        os.makedirs('Models', exist_ok=True)
        logger.info(f"Loading pretrained {model_name} model")
        print(f"Loading pretrained {model_name} model")
        model = get_pretrained_model(model_name)
        return model
    except Exception as e:
        logger.error(f"Error loading pretrained model: {e}")
        print(f"Error loading pretrained model: {e}")
        return None


def get_model(name: str = model_conifg['MODEL_NAME']):
    try:

        model = load_pretrain_model(model_name=name)
        if model is not None:
            if model_conifg['FREEZE_LAYER']:
                for layer in model.layers:
                    if isinstance(layer, tf.keras.layers.BatchNormalization):
                        layer.trainable = True
                    layer.trainable = False

            # adding last layers of the model
            x = model.output
            x = tf.keras.layers.GlobalAveragePooling2D()(x)
            x = tf.keras.layers.Dense(512, activation='relu')(x)
            x = tf.keras.layers.Dropout(0.3)(x)
            x = tf.keras.layers.Dense(128, activation='relu')(x)

            # output layer
            if int(data_config['CLASSES']) == 2:
                logger.info("Binary classification. Adding Sigmoid activation")
                output = tf.keras.layers.Dense(2, activation='sigmoid')(x)
            else:
                logger.info(f"Multi-class classification with class number: {data_config['CLASSES']}. Adding Softmax activation")
                output = tf.keras.layers.Dense(
                    data_config['CLASSES'], activation='softmax')(x)

            # defining the model
            final_model = tf.keras.models.Model(
                inputs=model.input, outputs=output)

            logger.info(f"Model summary:\n{final_model.summary()}")
            print("\n\n", final_model.summary(), "\n\n")

            # compiling the model
            logger.info("Compiling the model")
            final_model.compile(
                optimizer= tf.keras.optimizers.Adam(learning_rate=model_conifg['LEARNING_RATE']) if model_conifg['OPTIMIZER'] == 'Adam' else tf.keras.optimizers.SGD(
                    learning_rate=model_conifg['LEARNING_RATE']) if model_conifg['OPTIMIZER'] == 'SGD' else tf.keras.optimizers.RMSprop(learning_rate=model_conifg['LEARNING_RATE']) if model_conifg['OPTIMIZER']=='RMSprop' else None,
                loss=model_conifg['LOSS'],
                metrics=['accuracy']
            )

            logger.info(
                f"Model compiled with {model_conifg['OPTIMIZER']} optimizer, {model_conifg['LOSS']} loss and accuracy metrics")

            return final_model
        else:
            raise Exception(
                "Error loading pretrained or creating the define model")
    except Exception as e:
        logger.error(f"Error in get_model: {e}")
        print(f"Error in get_model: {e}")
