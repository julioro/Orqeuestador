#!/usr/bin/python3
from jinja2 import Template
import sys
import libvirt
import llenarTemplates as lT
import os
import subprocess

templatePath = "../Template/"

hwTemplatePath = templatePath + "domainConfig.xml"
name = "vmach"
mem = "1024"
cantCpu = "1"
index = "001"
#REP ="/var/lib/libvirt/images"
REP="~/images"
img = "bionic-server-cloudimg-amd64"
print("Construyendo cloud-config ...")
userDataPath = templatePath + "user-data"
metaDataPath = templatePath + "meta-data"

os.system("clear")
os.system("mkdir -p ../Imagenes/{0}".format(index))
os.system("sudo rm -rf {0}/{1}/".format(REP, index))
os.system("sudo mkdir -p {0}/{1}/".format(REP, index))


sshKeyArray = [""]
fileArray = [{"encoding":"raw", "content":"Skrra este archivo se creo con cloud-init", "owner":"ubuntu", "path":"/", "permissions":"0777", "append":"true"}]
userArray = [{"name":name, "password": name}]
udt, mdt = lT.cloudConfig(userDataPath, metaDataPath, index, name, sshKeyArray, fileArray, userArray)
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

print("Ejecutando sudo ../CloudInit/crearQcow.sh {0} {1} ...".format(img, index))
os.system("sudo bash ../CloudInit/crearQcow.sh {0} {1}".format(img, index))

print("Construyendo domainConfig.xml ...")

disksArray = [{'device':'disk', 'path':"{0}/{1}/boot-disk.img".format(REP, index), 'hdType':'vda', 'driverType':'qcow2', 'bus': 'virtio'}, {'device':'cdrom', 'path':'{0}/{1}/seed.iso'.format(REP, index), 'hdType':'hda', 'driverType':'raw', 'bus': 'ide'}]
ifacesArray = [{'name': 'tap0', 'type':'network', 'mac':'52:55:00:d1:55:10', 'targetDev':'tap0', 'modelType':'rtl8139'}]

# Para el Direct Kernel Boot
kdb = False
kernelPath = "../Imagenes/{0}/vmlinuz".format(index)
initrdPath = "../Imagenes/{0}/initrd".format(index)

# Para PCI PassThrough
pciPassEx = False
pciPass = {'domain': '0x0000', 'bus': '0x03', 'slot': '0x00', 'function': '0x0'}

xmlConfig = lT.xmlConfig(hwTemplatePath, name, mem, cantCpu, disksArray, ifacesArray, kdb, kernelPath, initrdPath, pciPassEx, pciPass)

# Creacion de la interfaz tap
print("Creando interfaz tap")
os.system("sudo ip link del dev tap0")
os.system("sudo ip tuntap add dev tap0 mode tap")
os.system("sudo ip link set dev tap0 address 52:55:00:d1:55:01")
os.system("sudo ip link set dev tap0 up")
os.system("sudo ip link show tap0")

print("*"*70)
print("libvirt confiuration:")
print(xmlConfig)


conn = libvirt.open('qemu:///system')
if conn == None:
    print('Failed to open connection to qemu:///system')
    exit(1)

dom = conn.createXML(xmlConfig.replace("\n", ""), 0)
if dom == None:
    print('Failed to create a domain from an XML definition.')
    exit(1)

print('Guest', dom.name(), ' has booted')
exit(0)
