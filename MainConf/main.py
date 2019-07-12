#!/usr/bin/python3
from jinja2 import Template
import sys
import libvirt
import llenarTemplates as lT
import os
import subprocess

index = "01
templatePath = "../Template/"
img = "bionic-server-cloudimg-amd64.img"
subprocess.call(["bash", "../CloudInit/crearQcow.sh", img, index])
os.system("sleep 5")

cloudTemplatePath= templatePath + "cloud-config.txt"
name = "virtualmachine"
sshPubKey =
content = "skrrrraaaa"
cloudConfig = lT.cloudConfig(index, name, sshPubKey, content)
f = open("../Imagenes/" + index + "-cloud-config.txt, "a")
f.write(cloudConfig)
f.close()

print(cloudConfig)

hwTemplatePath = templatePath + "domainConfig.xml"
name = "test"
mem = 1024
cantCpu = 1
disksArray = [{'type':'cdrom', 'path':'/var/lib/libvirt/images/bionicleIso.img', 'hdType':'hdc'}, {'type':'cdrom', 'path':'/var/lib/libvirt/images/bionicleCloud.iso', 'hdType':'hdc'}]
ifacesArray = [{'name':'enp2s0', 'type':'ethernet', 'mac':'26:c7:a9:96:a7:7a', 'targetDev':'tap1'}]

xmlConfig = lT.xmlConfig(hwTemplatePath, name, mem, cantCpu, disksArray, ifacesArray)
print(xmlConfig)

conn = libvirt.open('qemu:///system')
if conn == None:
    print('Failed to open connection to qemu:///system', file=sys.stderr)
    exit(1)

dom = conn.createXML(xmlConfig, 0)
if dom == None:
    print('Failed to create a domain from an XML definition.', file=sys.stderr)
    exit(1)

print('Guest', dom.name(), ' has booted', file=sys.stderr)
exit(0)
