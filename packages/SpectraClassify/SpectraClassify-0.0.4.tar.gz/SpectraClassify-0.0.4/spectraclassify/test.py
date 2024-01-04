from spectraclassify.utility import config_manager
from spectraclassify.training_service import start_training, show_training_results


start_training(model_conifg=config_manager.get_model_conf(),
               data_config=config_manager.get_data_conf())
