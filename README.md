# *UNIVERSIDAD MILITAR NUEVA GRANADA*
# **Tesis de grado del programa de ingenieria en mecatronica.**

- Bajo el uso de una tarjeta NVIDIA Jetson TX1 4GB se hara una deteccion y clasificacion de enfermades en plantas de papa.
- El modelo sera mediante SDD optimizado con TensorRT [TRT]
- Una vez detectada la enfermedad usando ROS (Robot Operating System) se enviaran señales para mover los actuadores y aspersores para tratar la planta.
## Dataset
El dataset se tomo en 
## En la JetsonTX1
Inicialmente haciendo uso de `jetson.inference.detectNet()` como se muestra en el repositorio de HelloAI mediante comandos de linux.
Pero para tener maor control del sistema se implementa de la siguiente manera:

- Instanciando la red:
```
NETWORK = [f'--model={model_dir}',f'--labels={labels_dir}','--input-blob=input_0',
            '--output-cvg=scores','--output-bbox=boxes']
```
- Llamandola con `argv`:
```
net = jetson.inference.detectNet(argv=NETWORK)
```
