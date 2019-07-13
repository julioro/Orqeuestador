#!/usr/bin/python3
from jinja2 import Template
import sys
import libvirt
import llenarTemplates as lT
import os
import subprocess

index = "001"
templatePath = "../Template/"
REP="/var/lib/libvirt/images"
img = "bionic-server-cloudimg-amd64"
print("Construyendo cloud-config ...")
userDataPath= templatePath + "user-data"
metaDataPath= templatePath + "meta-data"

os.system("mkdir -p ../Imagenes/{0}".format(index))
os.system("mkdir -p {0}/$INDEX/".format(REP))
os.system("rm -rf {0}/{1}/*".format(REP, index))

name = "vm"
sshKeyArray = ["ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDZRz8XJV0n/0/XBtHgDxL6v32Zpo47pxFs4TtK+M3fIX2i0vaEtIr/BgjjOMVBgQbniUB/+vSUA/ViWgmgXwyOBW/Z5MQmMEDIBtzE5H7BryCCIhGqDQ5m8bFZkV5uByCMjBtlQH7mhnjxs3sImGb8k2VjknoG8xVbX6UO+QWkPuoLqECxmiz3kWMixd8gMkO6J5moAr3CqzBXT3IrzcXYUZmtlL9Qv+zvqvmzbZ7J6zn3TFI+sleTKpq/EDyHWcEFQWVpeG8/bWEvyEBsQ6WmohcqVUDB/J+n7Ga1qCecldRiib/f495oT+XQo9J86NqSR+IiBr8yKZDT69/5dpfr juliorod@juliorod"]
fileArray = [{"encoding":"raw", "content":"Skrra este archivo gaa", "owner":"ubuntu", "path":"/", "permissions":"0777", "append":"true"}]
userArray = [{"name":name}]
udt, mdt = lT.cloudConfig(userDataPath, metaDataPath, index, name, sshKeyArray, fileArray, userArray)
f = open("../Imagenes/" + index + "/user-data", "w")
f.write(udt)
f.close()
f = open("../Imagenes/" + index + "/meta-data", "w")
f.write(mdt)
f.close()

print("Ejecutando sudo ../CloudInit/crearQcow.sh {0} {1} ...".format(img, index))
os.system("sudo bash ../CloudInit/crearQcow.sh {0} {1}".format(img, index))
#print(cloudConf)
print("Construyendo domainConfig.xml ...")
hwTemplatePath = templatePath + "domainConfig.xml"
name = "test"
mem = "1024"
cantCpu = "1"
disksArray = [{'type':'disk', 'path':"{0}/{1}/boot-disk.img".format(REP, index), 'hdType':'hdc'}, {'type':'cdrom', 'path':'{0}/{1}/seed.iso'.format(REP, index), 'hdType':'hda'}]
ifacesArray = [{'name':'enp2s0', 'type':'ethernet', 'mac':'26:c7:a9:96:a7:7a', 'targetDev':'tap0'}]
xmlConfig = lT.xmlConfig(hwTemplatePath, name, mem, cantCpu, disksArray, ifacesArray)
#print(xmlConfig)
print("END")
exit(0)


conn = libvirt.open('qemu:///system')
if conn == None:
    print('Failed to open connection to qemu:///system')
    exit(1)

dom = conn.createXML(xmlConfig, 0)
if dom == None:
    print('Failed to create a domain from an XML definition.')
    exit(1)

print('Guest', dom.name(), ' has booted')
exit(0)
