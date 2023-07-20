import numpy as np

import cv2
from pathlib import Path

import torch
import torch.nn as nn
from torch import nn
from torchvision.models import resnet18, efficientnet_b0, mobilenet_v2, efficientnet_v2_s

from albumentations import Compose, Normalize, Resize

if torch.cuda.is_available():
    device = 'cuda:0'
    torch.set_default_tensor_type('torch.cuda.FloatTensor')
else:
    device = 'cpu'

Res18_config= {'network': 'resnet18', 'num_classes': 5} 
ENb0_config= {'network': 'efficientnet-b0', 'num_classes': 5}

preprocess= Compose([
    Resize(224, 224),
    Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225], p=1)
])

def TrafficClassifier(cfg, load_path=None):
    if load_path:
        try:
            print('[*] Attempting to load model from:', load_path)
            model = _TrafficClassifier(cfg)
            model.load_state_dict(torch.load(load_path)['state_dict'])
        except: 
            print('[*] Model does not exist or is corrupted. Creating new model...')
            return _TrafficClassifier(cfg)

        # check whether `model` is an _TrafficClassifier instance
        if model.__class__.__name__ == '_TrafficClassifier':
            return model
        else:
            raise ValueError('The loaded tensor is not an instance of _TrafficClassifier.')
    else:
        print('[*] Creating model...')
        return _TrafficClassifier(cfg)

class _TrafficClassifier(nn.Module):
    def __init__(self, cfg):
        super(_TrafficClassifier, self).__init__()
        self.num_classes= cfg['num_classes']
        self.network= cfg['network']

        if cfg['network'] == "resnet18":
           self.initialize_resnet18()

        if cfg['network'] == "efficientnet-b0":
            self.initialize_enb0()
        
        if cfg['network'] == "mobilenet_v2":
            self.initialize_mnv2()

        if cfg['network'] == "efficientnet_v2_s":
            self.initialize_en_v2()

    def forward(self, x):
        return self.encoder(x)
    
    def freeze_all_layers(self):
        for param in self.encoder.parameters():
            param.requires_grad = False

    def freeze_middle_layers(self):
        self.freeze_all_layers()
        if self.network == "resnet18":
            for param in self.encoder.conv1.parameters():
                param.requires_grad = True
                
            for param in self.encoder.fc.parameters():
                param.requires_grad = True

        elif self.network == "efficientnet-b0" or self.network == "mobilenet_v2" or self.network == "efficientnet_v2_s":
            for param in self.encoder.features[0][0].parameters():
                param.requires_grad = True

            for param in self.encoder.classifier.parameters():
                param.requires_grad = True

        else:
            raise ValueError("Something went wrong! Model is not defined")

    def unfreeze_all_layers(self):
        for param in self.encoder.parameters():
            param.requires_grad = True

    def initialize_resnet18(self):
        print('[*] Initializing new resnet18 network...')
        self.encoder = resnet18(pretrained=True).to(device)

        self.encoder.fc = nn.Linear(512, self.num_classes, bias= True)

    def initialize_enb0(self):
        print('[*] Initializing new efficientnet-b0 network...')
        self.encoder = efficientnet_b0(pretrained=True).to(device)
        
        self.encoder.classifier[1]= nn.Linear(1280, self.num_classes, bias= True)

    def initialize_mnv2(self):
        print('[*] Initializing new mobilenet_v2 network...')
        self.encoder = mobilenet_v2(pretrained=True).to(device)
        
        self.encoder.classifier[1]= nn.Linear(1280, self.num_classes, bias= True)

    def initialize_en_v2(self):
        print('[*] Initializing new efficientnet-v2 network...')
        self.encoder = efficientnet_v2_s(pretrained=True).to(device)
        
        self.encoder.classifier[1]= nn.Linear(1280, self.num_classes, bias= True)
  
    def _get_index_of_matched_value(self, dictionary, value):

        for idx, val in dictionary.items():
            if val == value:
                return idx

        return None
    
    def test_model(self, test_loader):
        pass

    def inference(self, img_path):
        self.eval()
        img= cv2.imread(str(img_path))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img= preprocess(image= img) # resizing is important
        _img= np.expand_dims(img['image'], axis= 0)
        _img= np.transpose(_img, (0, 3, 1, 2))
        _img= torch.tensor(_img)
        _img.to(device)
        with torch.no_grad():
            y_pred = self.encoder(_img)
            out= torch.argmax(y_pred, dim= 1)
            
        label_encoder= {'Empty': 0, 'High': 1, 'Low': 2, 'Medium': 3, 'Traffic Jam': 4}
        output= self._get_index_of_matched_value(label_encoder, out)
        return output


def ResNet18():
    """
    >>>model= ResNet18() # model has to be in ../models_run/resnet18/resnet.pth
    >>>pred= model.inference(path/to/img)
    """
    repository_root = Path(__file__).parent.parent.parent.parent.parent
    save_dir= repository_root / "myanmar-weather-forecasting" / "src" / "traffic" / "models" / "models_runs"
    load_path= save_dir / "resnet18" / "resnet18.pth"
    loaded_model= TrafficClassifier(load_path= load_path, cfg=Res18_config)
    return loaded_model

def ENb0():
    """
    >>>model= ENb0() # model has to be in ../models_run/efficientnet-b0/efficientnet-b0.pth
    >>>pred= model.inference(path/to/img)
    """
    repository_root = Path(__file__).parent.parent.parent.parent.parent
    save_dir= repository_root / "myanmar-weather-forecasting" / "src" / "traffic" / "models" / "models_runs"
    load_path= save_dir / "efficientnet-b0" / "efficientnet-b0.pth"
    loaded_model= TrafficClassifier(load_path= load_path, cfg=ENb0_config)
    return loaded_model

def load_model(model_path, model_cfg):
    """
    Use it to load the model from any directory

    Args:
        model_path: the path to the model to be loaded (Resnet/ENb0)
        model_cfg: dictionary containing the configurations to build the classifier

    Example:
        >>> ENb0_config= {'network': 'efficientnet-b0', 'num_classes': 5}
        >>> ENb0_model= load_model(path/to/ENb0.pth, ENb0_config)
        >>> pred= ENb0_model.inference(path/to/img)
    """
    loaded_model= TrafficClassifier(load_path= model_path, cfg=model_cfg)
    return loaded_model
    