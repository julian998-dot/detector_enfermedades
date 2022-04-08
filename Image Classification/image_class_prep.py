#pip install python-resize-image
import cv2
import pathlib
import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
import re
from os import path
import random
import errno

class Dataset:
    
    #Altura_deseada = 180
    #Achura_deseada = 180
    altura = 0
    anchura = 0
    p_train = 0 
    dir_a = ' '
    dir_b = 'Dataset_final'
    
    def mezclar_lista(lista_original):
        lista = lista_original[:]
        longitud_lista = len(lista)
        for i in range(longitud_lista):
            indice_aleatorio = random.randint(0, longitud_lista - 1)
            temporal = lista[i]
            lista[i] = lista[indice_aleatorio]
            lista[indice_aleatorio] = temporal
        # Regresarla
        return lista
    
    def __init__(self):
        print('Codigo hecho por: Julian Cortes para la tesis de ingeniero en mecatronica 2022  ***')
        pass
    def set_pTrain(porcentaje):
        Dataset.p_train = porcentaje
    def set_dir(dir1):
        Dataset.dir_a = dir1
    def set_imgDim(Alto,Ancho):
        Dataset.altura = Alto
        Dataset.anchura = Ancho
    def iniciar():
        try:
            os.mkdir(Dataset.dir_b)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        dirname = os.path.join(os.getcwd(), Dataset.dir_a)
        imgpath = dirname + os.sep 
        images = []
        directories = []
        names = []
        dircount = []
        prevRoot=''
        cant=0
        #Cargar imagen
        for root, dirnames, filenames in os.walk(imgpath):
            for filename in filenames:
                if re.search("\.(jpg|jpeg|png|bmp|tiff|JPG)$", filename):
                    cant=cant+1
                    filepath = os.path.join(root, filename)
                    image = plt.imread(filepath)
                    b,g,r = cv2.split(image)
                    merged = cv2.merge([r,g,b])
                    images.append(merged)
                    b = "Leyendo..." + str(cant)
                    print (b, end="\r")
                    directories.append(root.replace(Dataset.dir_a,Dataset.dir_b))
                    names.append(filename)
                    if prevRoot !=root:
                        #print(root, cant)
                        prevRoot=root
                        dircount.append(cant)
                        cant=0
        dircount.append(cant)
        dircount = dircount[1:]
        dircount[0] =dircount[0]+1
        print('Directorios leidos:',len(directories))
        #print(directories)
        print("Imagenes en cada directorio", dircount)
        print('suma Total de imagenes en subdirs:',sum(dircount))
        imagenes_full = []
        for k in range(len(images)):
            redimensionar = cv2.resize(images[k], (Dataset.altura,Dataset.anchura))
            imagenes_full.append([redimensionar,os.path.basename(os.path.normpath(directories[k]))])
            #if(not(path.exists(directories[k]))):
                #os.mkdir(directories[k])
            #cv2.imwrite(directories[k]+"\\"+str(k)+".jpeg",redimensionar)
        print('Va a empezar la separacion para dataset...')
        new_lista = Dataset.mezclar_lista(imagenes_full)

        num_mtrain = (len(new_lista)*Dataset.p_train)-1
        if(not(path.exists('.\\Dataset_final\\data'))):
                os.mkdir('.\\Dataset_final\\data')

        if(not(path.exists('.\\Dataset_final\\data\\val'))):
                os.mkdir('.\\Dataset_final\\data\\val')
        if(not(path.exists('.\\Dataset_final\\data\\train'))):
                os.mkdir('.\\Dataset_final\\data\\train')
        if(not(path.exists('.\\Dataset_final\\data\\test'))):
                os.mkdir('.\\Dataset_final\\data\\test')

        for j in range(len(new_lista)):
            if j<=num_mtrain:
                if(not(path.exists('.\\Dataset_final\\data\\train'+"\\"+str(new_lista[j][1])))):
                        os.mkdir('.\\Dataset_final\\data\\train'+"\\"+str(new_lista[j][1]))
                cv2.imwrite('.\\Dataset_final\\data\\train'+"\\"+str(new_lista[j][1])+'\{cont}.jpeg'.format(cont=j),new_lista[j][0])
                tee = "Separando para training..."+str(j)
                print(tee,end="\r")

            if j>num_mtrain and j<(((len(new_lista)-num_mtrain)/2)+num_mtrain):
                if(not(path.exists('.\\Dataset_final\\data\\val'+"\\"+str(new_lista[j][1])))):
                        os.mkdir('.\\Dataset_final\\data\\val'+"\\"+str(new_lista[j][1]))
                cv2.imwrite('.\\Dataset_final\\data\\val'+"\\"+str(new_lista[j][1])+'\{cont}.jpeg'.format(cont=j),new_lista[j][0])
                tee = "Separando para validacion..."+str(j)
                print(tee,end="\r")

            if j>=(((len(new_lista)-num_mtrain)/2)+num_mtrain):
                if(not(path.exists('.\\Dataset_final\\data\\test'+"\\"+str(new_lista[j][1])))):
                        os.mkdir('.\\Dataset_final\\data\\test'+"\\"+str(new_lista[j][1]))
                cv2.imwrite('.\\Dataset_final\\data\\test'+"\\"+str(new_lista[j][1])+'\{cont}.jpeg'.format(cont=j),new_lista[j][0])
                tee ="Separando para test..."+str(j)
                print(tee,end="\r")
        print('***************  TERMINO LA PREPARACION DEL DATASET  ***************\n')

