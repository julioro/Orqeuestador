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
import xml.etree.ElementTree as ET
import xml.dom.minidom
from bs4 import BeautifulSoup as BS

def vmImgCloudInit():
    #mem = "1024"
    #cpus = "1"
    #imgOp = 1
    cant = int(str(input("\tCantidad de máquinas virtuales: ")))
    memInp = input('\tEspacio en memoria (default MiB): ')

    if len(memInp.split(" ")) == 1:
        mem = [memInp, "MiB"]
    else:
        mem = memInp.split(" ")

    cpus = input('\tCantidad de CPUs: ')

    for _ in range(cant):
        index = str(len(dictVM) + 1)
        alreadyExist = True
        while alreadyExist:
            alreadyExist = "vm-" + index in dictVM
            if alreadyExist: index = str(int(index)+1)

        imgArr = [{"name": "Ubuntu", "defUser":"ubuntu", "img":"bionic-server-cloudimg-amd64.img", "kernel":"vmlinuz-ubuntu", "initrd":"initrd-ubuntu"}, {"name": "CentOS", "defUser":"centos", "img":"CentOS-7-x86_64-GenericCloud.qcow2", "kernel":"vmlinuz-centos", "initrd":"initrd-centos"}]
        print("\tImagenes disponibles:")
        [print("\t\t{0}) {1}".format(i+1, imgArr[i]["name"])) for i in range (len(imgArr))]
        imgOp = int(input("Opcion:\t"))

        # Direct Kernel Boot
        kdbInput = input("Implementar mediante Direct Kernel Boot (S/n): ").upper()
        kdb = kdbInput in ["S", "Y", "SI", "YES"]
        # PCI Passtrough
        #pciPassExInput = input("Implementar PCI Passtrough (S/n): ")
        #pciPassEx = pciPassExInput in ["S", "Y", "SI", "YES"]

        # SRI-OV
        sriovInput = input("Implementar SRI-OV (S/n): ").upper()
        sriov = sriovInput in ["S", "Y", "SI", "YES"]
        ifSRIOV = ""
        if sriov:
            ifSRIOV = listaSRIOV.pop()

        flag = BC.bootImg(index, repDir, imgArr[imgOp-1], mem, cpus, kdb, sriov, ifSRIOV)
        if flag: dictVM[index] = flag
    pass


def listarVm():
    frmt = "{:>5}|{:>5}|{:>12}|"
    print(frmt.format("NAME", "CPUs", "MEM"))
    for key in dictVM.keys():
        vm = dictVM[key]
        print(frmt.format(vm["name"], vm["cantCpus"], vm["mem"][0]+ " " +  vm["mem"][1]))
    # name = virsh dominfo vm-1 | grep "Name" | awk '{ print $2 }'
    # cpus = virsh dominfo vm-1 | grep "CPU(s)" | awk '{ print $2 }'
    # mem = virsh dominfo vm-1 | grep "Max memory: " | awk '{ print $3 " " $4 }'
    # ifaces = virsh domifaddr vm-1
    pass


def cambiarRepDir():
    repDir = input("Repository directory (default: " + defRepDir + "):\t")
    if repDir == "": repDir = defRepDir
    return repDir

def terminarPrograma():
    print("*" * 70 )
    return exit(0)

def getNodeText(node):

    nodelist = node.childNodes
    result = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            result.append(node.data)
    return ''.join(result)

def sacarXmlSriov(index):
    xmlConf = subprocess.check_output("virsh dumpxml vm-" + index, shell=True).decode("utf-8").replace("\n", " ")
    pars = BS(xmlConf, features="xml")
    try:
        flag = pars.domain.devices.hostdev.source.address
        domain = str(flag["domain"][2:])
        bus = str(flag["bus"][2:])
        slot = str(flag["slot"][2:])
        function  = str(flag["function"][2:])
        ga = ':'.join([domain, bus, slot])
        ga = ga + "." + function
    except (TypeError, KeyError, AttributeError) as e:
        return ""
    return ga

def leerVmExistentes():
    vmExistentes = subprocess.check_output("virsh list | awk ' NR > 2 { print $2 }'", shell=True).decode("utf-8")[:-2]
    vmList = vmExistentes.split("\n")
    for vm in vmList:
        if "vm-" in vm:
            index = vm.split("vm-")[1]
            info = subprocess.check_output("bash leerVmExistente.sh " + index, shell=True).decode("utf-8")[:-1].split(" ")
            infoSriov=sacarXmlSriov(index)
            print(infoSriov)
            if infoSriov in listaSRIOV:
                listaSRIOV.pop(listaSRIOV.index(infoSriov))
            print(listaSRIOV)
            name = info[0]
            cantCpus = info[1]
            memQ = info[2]
            memUnits = info[3]
            mem = [memQ, memUnits]


            #disksArray =
            #ifaces =
            dictVM[index] = {"name": name, "mem": mem, "cantCpus": cantCpus}

    return True

def leerTarjetasSRIOV():
    listaSRIOV = subprocess.check_output("bash sacarTarjetasSRIOV.sh", shell=True)
    listaDecode = listaSRIOV.decode("utf-8")[:-1]
    return listaDecode.split(" ")

if __name__ == "__main__":
    dictVM = {} # nombre, memoria, cpus, imagen
    repDir = ""
    listaSRIOV = leerTarjetasSRIOV()
    leerVmExistentes()

    defRepDir = "/home/scabrera/images"
    repDir=cambiarRepDir()

    if repDir == "": repDir = defRepDir

    print("*"*70)
    while True:
        options = [("Crear máquina virtual", vmImgCloudInit) , ("Listar máquinas virtuales", listarVm), ("Cambiar ubicación de imagenes", cambiarRepDir), ("Salir", terminarPrograma)]
        for i  in range(len(options)):
            print("[{0}] {1}".format( i+1, options[i][0] ))
        try:
            op = int(input("Opcion:\t"))
            options[op-1][1]()
        except (IndexError, ValueError) as e:
            print("Opción inválida...\n")
        finally:
            print("\n")
