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
from spectraclassify.utility import pretrained_models



def load_pretrain_model(model_name: str):
    try:
        os.makedirs('Models', exist_ok=True)
        logger.info(f"Loading pretrained {model_name} model")
        print(f"Loading pretrained {model_name} model")
        model = pretrained_models.get_pretrained_model(model_name)
        return model
    except Exception as e:
        logger.error(f"Error loading pretrained model: {e}")
        print(f"Error loading pretrained model: {e}")
        return None


def get_model(name: str, freeze_layer: bool, no_of_classes: int, lr: float, optimizer_fn_name: str, loss_fn_name: str):
    try:

        model = load_pretrain_model(model_name=name)
        if model is not None:
            if freeze_layer:
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
            if no_of_classes == 2:
                logger.info("Binary classification. Adding Sigmoid activation")
                output = tf.keras.layers.Dense(2, activation='sigmoid')(x)
            else:
                logger.info(
                    f"Multi-class classification with class number: {no_of_classes}. Adding Softmax activation")
                output = tf.keras.layers.Dense(
                    no_of_classes, activation='softmax')(x)

            # defining the model
            final_model = tf.keras.models.Model(
                inputs=model.input, outputs=output)

            logger.info(f"Model summary:\n{final_model.summary()}")
            print("\n\n", final_model.summary(), "\n\n")

            # compiling the model
            logger.info("Compiling the model")
            final_model.compile(
                optimizer=tf.keras.optimizers.Adam(learning_rate=lr) if optimizer_fn_name == 'Adam' else tf.keras.optimizers.SGD(
                    learning_rate=lr) if optimizer_fn_name == 'SGD' else tf.keras.optimizers.RMSprop(learning_rate=lr) if optimizer_fn_name == 'RMSprop' else None,
                loss=loss_fn_name,
                metrics=['accuracy']
            )

            logger.info(
                f"Model compiled with {optimizer_fn_name} optimizer, {loss_fn_name} loss and accuracy metrics")

            return final_model
        else:
            raise Exception(
                "Error loading pretrained or creating the define model")
    except Exception as e:
        logger.error(f"Error in get_model: {e}")
        print(f"Error in get_model: {e}")
