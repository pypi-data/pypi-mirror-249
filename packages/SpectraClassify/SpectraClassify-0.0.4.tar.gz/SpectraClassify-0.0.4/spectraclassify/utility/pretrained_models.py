from tensorflow.keras.applications import ResNet50, ResNet101, ResNet152, ResNet50V2, ResNet101V2, ResNet152V2
from tensorflow.keras.applications import VGG16, VGG19, Xception, InceptionV3, InceptionResNetV2, MobileNet, MobileNetV2
from tensorflow.keras.applications import DenseNet121, DenseNet169, DenseNet201, NASNetLarge, NASNetMobile

from spectraclassify import logger
def get_pretrained_model(model_name):
    logger.info(f"Loading pretrained {model_name} model")

    _model = None
    if model_name == "ResNet50":
        print(f"Loading pretrained ResNet50 model")

        _model = ResNet50(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
    elif model_name == "ResNet101":
        print(f"Loading pretrained ResNet101 model")
        _model = ResNet101(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
    elif model_name == "ResNet152":
        print(f"Loading pretrained ResNet152 model")
        _model = ResNet152(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
    elif model_name == "ResNet50V2":
        print(f"Loading pretrained ResNet50V2 model")
        _model = ResNet50V2(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
    elif model_name == "ResNet101V2":
        print(f"Loading pretrained ResNet101V2 model")
        _model = ResNet101V2(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
    elif model_name == "ResNet152V2":
        print(f"Loading pretrained ResNet152V2 model")
        _model = ResNet152V2(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
    elif model_name == "VGG16":
        print(f"Loading pretrained VGG16 model")
        _model = VGG16(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
    elif model_name == "VGG19":
        print(f"Loading pretrained VGG19 model")
        _model = VGG19(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
    elif model_name == "Xception":
        print(f"Loading pretrained Xception model")
        _model = Xception(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
    elif model_name == "InceptionV3":
        print(f"Loading pretrained InceptionV3 model")
        _model = InceptionV3(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
    elif model_name == "InceptionResNetV2":
        print(f"Loading pretrained InceptionResNetV2 model")
        _model = InceptionResNetV2(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
    elif model_name == "MobileNet":
        print(f"Loading pretrained MobileNet model")
        _model = MobileNet(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
    elif model_name == "MobileNetV2":
        print(f"Loading pretrained MobileNetV2 model")
        _model = MobileNetV2(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
    elif model_name == "DenseNet121":
        print(f"Loading pretrained DenseNet121 model")
        _model = DenseNet121(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
    elif model_name == "DenseNet169":
        print(f"Loading pretrained DenseNet169 model")
        _model = DenseNet169(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
    elif model_name == "DenseNet201":
        print(f"Loading pretrained DenseNet201 model")
        _model = DenseNet201(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
    elif model_name == "NASNetLarge":
        print(f"Loading pretrained NASNetLarge model")
        _model = NASNetLarge(include_top=False, weights='imagenet', input_shape=(331, 331, 3))
    elif model_name == "NASNetMobile":
        print(f"Loading pretrained NASNetMobile model")
        _model = NASNetMobile(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
    else:
        print(f"Unknown model name: {model_name}")
        raise ValueError(f"Unknown model name: {model_name}")
    return _model
