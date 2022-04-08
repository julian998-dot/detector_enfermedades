import jetson.inference
import jetson.utils
import sys

model1__dir = '/home/tx1/Desktop/img_clasif/models/papaR18/resnet18.onnx'
model2__dir = '/home/tx1/Desktop/img_clasif/models/papaGnet/googlenet.onnx'
model3__dir = '/home/tx1/Desktop/img_clasif/models/papaDN121/densenet121.onnx.onnx'
model4__dir = '/home/tx1/Desktop/img_clasif/models/papaR101/resnet101.onnx'
models_dir = [model1__dir,model2__dir,model3__dir,model4__dir]
###############3

num_model = 1 
"""
1.ResNet18 
2.GoogleNet 
3.DenseNet121
4.ResNet101
-----------------------------------------------------------------------------------------
"""
net_name = ''
if num_model==1:
    net_name = 'ResNet18-UMNG'
if num_model==2:
    net_name = 'GoogleNet-UMNG'
if num_model==3:
    net_name = 'DenseNet121-UMNG'
if num_model==4:
    net_name = 'ResNet101-UMNG'

net_config = [f'--model={models_dir[num_model-1]}',
'--input_blob=input_0',
'--output_blob=output_0',
'--labels=/home/tx1/Desktop/img_clasif/setpapa/labels.txt']

is_headless = ["--headless"] if sys.argv[0].find('console.py') != -1 else [""]
input = jetson.utils.videoSource('/dev/video1')
output = jetson.utils.videoOutput(argv=sys.argv+is_headless)
font = jetson.utils.cudaFont()
net = jetson.inference.imageNet(argv=net_config)

while True:
    # capture the next image
    img = input.Capture()

    # classify the image
    class_id, confidence = net.Classify(img)

    # find the object description
    class_desc = net.GetClassDesc(class_id)


    # overlay the result on the image	
    font.OverlayText(img, img.width, img.height, "{:05.2f}% {:s}".format(confidence * 100, class_desc), 5, 5, font.White, font.Gray40)

    # render the image
    output.Render(img)

    # update the title bar
    output.SetStatus("{:s} | Network {:.0f} FPS".format(net_name, net.GetNetworkFPS()))

    # print out performance info
    net.PrintProfilerTimes()

    if class_desc=='tizon' or class_desc=='epitrix':
        print('Ta enfermo y se hace algo')
    else:
        print('Ta sano')
    # exit on input/output EOS
    if not input.IsStreaming() or not output.IsStreaming():
        break
