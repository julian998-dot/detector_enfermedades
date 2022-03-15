import cv2
import jetson.inference
import jetson.utils
from jetson.utils import cudaFromNumpy as cfn, saveImageRGBA
import pyzed.sl as sl
import sys
import cv2
#################
from zed_config import camara_zed
from config import NETWORK, ANCHO, LARGO, OVERLAY, RES_CAMARA, FPS_CAMARA
############################################################################3

zed = camara_zed(RES_CAMARA, FPS_CAMARA) # inicia la camara
net = jetson.inference.detectNet(argv=NETWORK)
image_zed = sl.Mat()
width = ANCHO
height = LARGO
font = jetson.utils.cudaFont()
display = jetson.utils.glDisplay()

while display.IsOpen():
    zed.grab()
    zed.retrieve_image(image_zed, sl.VIEW.LEFT)
    image_data = image_zed.get_data()
    image_data = cv2.cvtColor(image_data, cv2.COLOR_BGR2RGBA)
    cuda_mem = cfn(image_data)

    detections = net.Detect(cuda_mem, width, height, OVERLAY)

	# print the detections
    print("detected {:d} objects in image".format(len(detections)))

    for detection in detections:
        print(detection)
    # render the image
    display.RenderOnce(cuda_mem, width, height)
	# update the title bar
    display.SetTitle("{:s} | Network {:.0f} FPS".format('TESIS_CERES', net.GetNetworkFPS()))

	# print out performance info
    net.PrintProfilerTimes()
    

