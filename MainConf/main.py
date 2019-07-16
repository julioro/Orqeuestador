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
import subprocess


def vmImgCloudInit():
    #mem = "1024"
    #cpus = "1"
    #imgOp = 1
    cant = int(str(input("\tCantidad de máquinas virtuales: ")))
    mem = input('\tEspacio en memoria (default MiB): ')
    if len(mem.split(" ")) == 1: mem = [mem, "MiB"]
    cpus = input('\tCantidad de CPUs: ')

    for _ in range(cant):
        index = str(len(dictVM) + 1)
        imgArr = [{"defUser":"ubuntu", "img":"bionic-server-cloudimg-amd64.img"}, {"defUser":"centos", "img":"CentOS-7-x86_64-GenericCloud.qcow2"}]
        print("Imagenes disponibles:")
        [print("\t{0}) {1}".format(i+1, imgArr[i]["img"])) for i in range (len(imgArr))]
        imgOp = int(input("Opcion:\t"))

        # Direct Kernel Boot
        kdbInput = input("Implementar mediante Direct Kernel Boot (S/n): ")
        kdb = kdbInput in ["S", "Y", "SI", "YES"]
        # PCI Passtrough
        #pciPassExInput = input("Implementar PCI Passtrough (S/n): ")
        #pciPassEx = pciPassExInput in ["S", "Y", "SI", "YES"]

        # SRI-OV
        sriovInput = input("Implementar SRI-OV (S/n): ")
        sriov = sriovInput in ["S", "Y", "SI", "YES"]
        if sriov:
            ifSRIOV = listSRIOV.pop()

        flag = BC.bootImg(index, repDir, imgArr[imgOp-1], mem, cpus, kdb, sriov, ifSRIOV)
        if flag: dictVM[index] = flag
    pass

def listarVm():
    print("listarVm")
    pass
    # name = virsh dominfo vm-1 | grep "Name" | awk '{ print $2 }'
    # cpus = virsh dominfo vm-1 | grep "CPU(s)" | awk '{ print $2 }'
    # mem = virsh dominfo vm-1 | grep "Max memory: " | awk '{ print $3 " " $4 }'
    # ifaces = virsh domifaddr vm-1



    pass

def terminarPrograma():
    exit(0)
    pass

def leerVmExistentes():
    pass

def leerTarjetasSRIOV():
    listaSRIOV = subprocess.check_output("bash sacarTarjetasSRIOV.sh", shell=True)
    listaDecode = listaSRIOV.decode("utf-8")[:-1]
    return listaDecode.split(" ")

if __name__ == "__main__":
    dictVM = {} # nombre, memoria, cpus, imagen
    repDir = ""
    listaSRIOV = leerTarjetasSRIOV()
    leerVmExistentes()

    #defRepDir = "/var/lib/libvirt/images"
    defRepDir = "/home/labtel/images"
    repDir = input("Repository directory (" + defRepDir + "):\t")
    if repDir == "": repDir = defRepDir

    print("*"*70)
    while True:
        options = [("Crear máquina virtual", vmImgCloudInit) , ("Listar máquinas virtuales", listarVm), ("Salir", terminarPrograma)]
        for i  in range(len(options)):
            print("[{0}] {1}".format( i+1, options[i][0] ))
        try:
            op = int(input("Opcion:\t"))
            options[op-1][1]()
        except (IndexError, ValueError) as e:
            print("Opción inválida...\n")
