# *UNIVERSIDAD MILITAR NUEVA GRANADA*
# **Tesis de grado del programa de ingenieria en mecatronica.**

- Bajo el uso de una tarjeta NVIDIA Jetson TX1 4GB se hara una deteccion y clasificacion de enfermades en plantas de papa.
- El modelo sera mediante SDD optimizado con NVIDIA TensorRT [TRT]
- Una vez detectada la enfermedad usando ROS (Robot Operating System) se enviaran señales para mover los actuadores y aspersores para tratar la planta en el robot CERES.
## Dataset
El dataset se tomo en el campus de la universidad, con ayuda de docentes de horticultura se planto una parcela de 24x24 plantas indivuduales de papa, estas separadas de tal forma que el robot pueda entrar y mirar de a dos lineas de cultivo al tiempo.

Con la toma de datos se obtuvieron un total de 422 imagenes, siguiendo la pipeline de la genracion de un modelo de inteligencia artificial para deteccion de objetos(OD), se colocó labels([usando labelimg](https://tzutalin.github.io/labelImg/)) a todas estas imagenes de esta manera:
![Image text](https://github.com/julian998-dot/detector_enfermedades/blob/main/ignore/labeling_sample.jpeg)
Teniendo en cuenta que todo el formato de labeling esta en *PascalVOC*, lo que no es mas que un archivo .xml con la informacion de los BBOXES.
## En la JetsonTX1

Antes que nada revisaar la documentacion de dusty_nv para las [NVIDIA JETSON](https://github.com/dusty-nv/jetson-inference) para [transfer learning en SSD Mobilenet.](https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-ssd.md)

Se optó por entrenar la red en la JETSON, usando el comando:
```
$ python3 train_ssd.py --dataset-type=voc --data=data/plantas/ --model-dir=models/plantas/ --batch-size=2 --workers=1 --epochs=50
```
Despues de este entrenamiento ejeceutaremos:
```
$ python3 onnx_export.py --model-dir=models/plantas/
```
Finalmente haciendo uso de `jetson.inference.detectNet()` como se muestra en el repositorio de [HelloAI](https://github.com/dusty-nv/jetson-inference) mediante comandos de linux.
Pero para tener mayor control del sistema se implementa de la siguiente manera:

- Instanciando la red:
```
NETWORK = [f'--model={model_dir}',f'--labels={labels_dir}','--input-blob=input_0',
            '--output-cvg=scores','--output-bbox=boxes']
```
- Llamandola con `argv`:
```
net = jetson.inference.detectNet(argv=NETWORK)
```
Como se muestra en la carpeta en este repositorio de codigos de la jetson.
