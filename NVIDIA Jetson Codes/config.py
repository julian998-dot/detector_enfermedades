

THRESHOLD = 0.75 # PORCENTAJE DE ACEPTACION EN LA DETECCION

model_dir = '../models/papa_net1/ssd-mobilenet.onnx'
labels_dir = '../models/papa_net1/labels.txt'

NETWORK = [f'--model={model_dir}',f'--labels={labels_dir}','--input-blob=input_0',
            '--output-cvg=scores','--output-bbox=boxes']

ANCHO = 1280
LARGO = 720

RES_CAMARA = 1080 # 1080 O 720
FPS_CAMARA = 30

OVERLAY = "box,labels,conf"

