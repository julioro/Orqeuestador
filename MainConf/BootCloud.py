#!/usr/bin/python3
from jinja2 import Template
import sys
import libvirt
import llenarTemplates as lT
import os
import subprocess

# Variables globales
templatePath = "../Template"
hwTemplatePath = templatePath + "/domainConfig.xml"
userDataPath = templatePath + "/user-data"
metaDataPath = templatePath + "/meta-data"
sshPath = "../SshFolder"
#REP ="/var/lib/libvirt/images"
REP="/home/labtel/images"
MacBase = "52:55:00:d1:55:00"

def bootImg(index, img, mem=1024, cantCpu=1, kdb=False, pciPassEx=False):
    defUser = img["defUser"]
    imgOp = img["img"]
    # Define variables
    name = "vm-" + index
    print("NAME", name)
    imgPath = "{0}/{1}".format(REP, imgOp)
    
    # Define user-data y meta-data
    print("Construyendo cloud-config ...")
    os.system("rm -rf ../Imagenes/{0}; mkdir -p ../Imagenes/{0}; rm -rf {1}/{0}/ ; mkdir -p {1}/{0}".format(index, REP))
    sshKeyArray = []
    for file in os.listdir(sshPath):
        with open(sshPath + '/' + file, 'r') as f:
            sshKeyArray.append(f.read())

    fileArray = []
    userArray=[{"name": name, "password":"root"}]
    udt, mdt = lT.cloudConfig(userDataPath, metaDataPath, index, name, sshKeyArray, fileArray, userArray, defUser)
    f = open("../Imagenes/" + index + "/user-data", "w")
    f.write(udt)
    f.close()
    f = open("../Imagenes/" + index + "/meta-data", "w")
    f.write(mdt)
    f.close()
    # Visualizacion de user-data y meta-data
    print("User-data")
    print(udt)
    print("Meta-data")
    print(mdt)
    print("Ejecutando bash ../CloudInit/crearQcow.sh {0} {1} {2}...".format(imgOp, index, REP))
    os.system("bash ../CloudInit/crearQcow.sh {0} {1} {2}".format(imgOp, index, REP))

    #Define domainConfig.xml
    print("Construyendo domainConfig.xml ...")
    # Funciona para direct-kernel boot y boot por volumen
    disksArray = [{'device':'disk', 'path':"{0}/{1}/boot-disk.img".format(REP, index), 'hdType':'vda', 'driverType':'qcow2', 'bus': 'virtio'}, {'device':'cdrom', 'path':'{0}/{1}/seed.iso'.format(REP, index), 'hdType':'hda', 'driverType':'raw', 'bus': 'ide'}]
    
    # Creacion de la interfaz tap
    mac = nextMac(index)
    os.system("bash crearInterfazTap.sh {0} {1}".format(index, mac))
    tapInt = "tap" + index

    ifacesArray = [{'name': tapInt, 'type':'network', 'mac':mac, 'targetDev':tapInt, 'modelType':'virtio'}]
    
    # Para el Direct Kernel Boot
    kernelPath = "../Imagenes/{0}/vmlinuz".format(index)
    initrdPath = "../Imagenes/{0}/initrd".format(index)

    # Para PCI PassThrough
    pciPassEx = False
    pciPass = {}
    #pciPass = {'domain': '0x0000', 'bus': '0x03', 'slot': '0x00', 'function': '0x0'}
    
    xmlConfig = lT.xmlConfig(hwTemplatePath, name, mem, cantCpu, disksArray, ifacesArray, kdb, kernelPath, initrdPath, pciPassEx, pciPass)

    # Mostar toda la configuracion para una maquina virtual.
    print("*"*70)
    print("libvirt confiuration:")
    print(xmlConfig)

    # Levantar la maquina mediante libvirt.
    conn = libvirt.open('qemu:///system')
    if conn == None:
        print('Failed to open connection to qemu:///system')
        return False

    dom = conn.createXML(xmlConfig.replace("\n", ""), 0)
    if dom == None:
        print('Failed to create a domain from an XML definition.')
        return False

    print('Guest', dom.name(), ' has booted')
    return True


def nextMac(index):
    MacBaseStr = MacBase.replace(':', '')
    MacBaseStrInteger = int(MacBaseStr, 16) + int(index)
    h = str(hex( MacBaseStrInteger ))[2:]
    nextmac = ':'.join(h[i:i+2] for i in range(0,12,2))
    return nextmac
