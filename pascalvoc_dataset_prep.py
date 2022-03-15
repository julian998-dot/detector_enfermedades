import os
import re
import glob
import pathlib
import errno
import random
import numpy as np
import shutil
#############################################################
# def mezclar_lista(array):
#         lista = array[:][:]
#         longitud_array = len(lista[1][:])
#         for i in range(longitud_array):
#             indice_aleatorio = random.randint(0, longitud_array - 1)
#             temporal = lista[0:1][i]
#             lista[0:1][i] = lista[0:1][indice_aleatorio]
#             lista[0:1][indice_aleatorio] = temporal
#         # Regresarla
#         return lista
############################################################
try:
    os.mkdir('./data/mi_dataset')
except OSError as e:
    if e.errno != errno.EEXIST:
        raise


trainval_percent = 0.7
train_percent = 0.7
#######################################################################
class_names = ['sano', 'epitrix']    
label_file = open('./data/mi_dataset/labels.txt',"w")
for k in range(len(class_names)):
    label_file.write(class_names[k] + '\n')
label_file.close()


dir_original = './data/dataset' 
dir_name = os.path.join(os.getcwd(),dir_original)
print(dir_name)
path = dir_original + os.sep
print(path)
xml_names= []
jpg_nm = []
xml_nm = []

images_names = []
cant_xml = 0
cant_imags = 0
prevRoot=''

for root, direnames, filenames in os.walk(path):
    for filename in filenames:
        if re.search("\.(jpg|jpeg|png|bmp|tiff|JPG)$",filename):
            cant_imags = cant_imags + 1
            filepath = os.path.join(root, filename)
            jpg_nm.append(filename)
            images_names.append(filepath)
            if prevRoot !=root:
                        #print(root, cant)
                        prevRoot=root
        if re.search("\.(xml)$",filename):
            cant_xml = cant_xml + 1
            filepath = os.path.join(root, filename)
            xml_nm.append(filename)
            xml_names.append(filepath)
            if prevRoot !=root:
                        #print(root, cant)
                        prevRoot=root
        b = "Leyendo...   ->" + str(cant_imags) + " imagenes y " + str(cant_xml) + " anotaciones."
        print (b, end="\r")
print('Se leyó un total de: ',str(cant_imags),' imagenes y ',str(cant_xml),' anotaciones.')

annotation_dir = os.path.join('data','mi_dataset','Annotations')
imageset_dir = os.path.join('data','mi_dataset','ImageSets','Main')
jpegimages_dir = os.path.join('data','mi_dataset','JPGImages')

voc_dir = []
voc_dir.append(annotation_dir)
voc_dir.append(imageset_dir)
voc_dir.append(jpegimages_dir)

for i in range(len(voc_dir)):
    if not os.path.exists(voc_dir[i]):
        os.makedirs(voc_dir[i])

voc_ds = [images_names,xml_names]
voc_dataset = np.array(voc_ds)
#print(voc_dataset[0][1],'\n',voc_dataset[1][1])
#print(voc_dataset.shape)
#print(xml_nm[0])
for k in range(len(xml_names)):
    shutil.copy(xml_names[k],annotation_dir+'/'+f'{xml_nm[k]}')
    b = "Copiando...   -> " + f'{k}' + ' archivos xml'
    print (b, end="\r")
for k in range(len(xml_names)):
    shutil.copy(images_names[k],jpegimages_dir+'/'+f'{jpg_nm[k]}')
    b = "Copiando...   -> " + f'{k}' + ' archivos JPG'
    print (b, end="\r")

###############################################
num=len(xml_names)
list=range(num)
tv=int(num*trainval_percent)
tr=int(tv*train_percent)
trainval= random.sample(list,tv)
train=random.sample(trainval,tr)
ftrainval = open(imageset_dir+'/'+'trainval.txt', 'w')
ftest = open(imageset_dir+'/'+'test.txt', 'w')
ftrain = open(imageset_dir+'/'+'train.txt', 'w')
fval = open(imageset_dir+'/'+'val.txt', 'w')

for i in list:
    name=os.path.basename(xml_names[i])[:-4]+'\n'
    if i in trainval:
        ftrainval.write(name)
        if i in train:
            ftrain.write(name)
        else:
            fval.write(name)
    else:
        ftest.write(name)
    b = "GENERANDO DATOS...   -> " + f'{i+1}' + ' datos'
    print (b, end="\r")

ftrainval.close()
ftrain.close()
fval.close()
ftest.close()



