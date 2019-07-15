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


def vmImgCloudInit():
    mem = input('Espacio en memoria (MiB)')
    cpus = input('Cantidad de CPUs: ')
    print("Imagenes disponibles:")
    imgAv
