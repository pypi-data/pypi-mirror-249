from spectraclassify.utility import config_manager
from spectraclassify.training_service import start_training


start_training(model_config=config_manager.get_model_conf(),
               data_config=config_manager.get_data_conf())
