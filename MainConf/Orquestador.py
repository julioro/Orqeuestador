#!/usr/bin/python3

'''
1. Crear maquina virtual
    - Mem (MiB)
    - Cantidad CPUs
    - Direct Kernel Boot, Filesystem + Initrd, Imagen + Cloud Init
        - Image + Cloud Init:
            disk [imagePath.img cloudInit.iso]
            iface []
        - Direct Kernel Boot:
            kernelPath
            initrdPath
'''

import sys
import BootCloud as BC

dictVM = {}


def vmImgCloudInit(cant):
    mem = "1024"
    cpus = "1"
    imgOp = 1
    #mem = input('Espacio en memoria (MiB):\t')
    #cpus = input('Cantidad de CPUs:\t')
    for _ in range(cant):
        index = str(len(dictVM) + 1)  
        imgArr = ["bionic-server-cloudimg-amd64.img", "CentOS-7-x86_64-GenericCloud.qcow2"]
        print("Imagenes disponibles:")
        [print("{0}) {1}".format(i+1, imgArr[i])) for i in range (len(imgArr))]
        #imgOp = int(input("Opcion:\t"))
        flag = BC.bootImg(index, imgArr[imgOp-1], mem, cpus)
        if flag: dictVM[index] = "on"

vmImgCloudInit(4)