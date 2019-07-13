#!/usr/bin/python3
from jinja2 import Template
import sys
import libvirt
import llenarTemplates as lT
import os
import subprocess

index = "001"
templatePath = "../Template/"
img = "bionic-server-cloudimg-amd64"

print("Construyendo cloud-config ...")
cloudTemplatePath= templatePath + "cloud-config.txt"
name = "virtualmachine"
sshPubKey = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC7A60783+AFL3qTcfN5U8OcC1hHL+V1kQHbR5ZDxhedYKb/9aTiib7C9/6yh9XdwQRkknhcvNQnAjkSFNxNj9MZ/CIQvnYtg0aYVElpTsvssYfFsrqvhmWr/f5a8T5Y62KfdNSmCjLMhqMyHeVfOozQskq30OVE8SWWgPCYhv+/kZzBmBt0dW65kdsq63JoTSfTf3epo0rZY610QLkrSWdlF/vhK1AwEuxszj2YOQMN8DnIuG/hew2LfNevPkxDS8hL9ooIXnxiyd8lzR2TWZhhhNM0h6KyXfcVW85kfEcosH/5srTaqD24pl50yO0s/agC4zjtZ+gutUp6/6c/AHD labtel@192.168.35.127"
content = "skrrrraaaa"
cloudConfig = lT.cloudConfig(cloudTemplatePath, index, name, sshPubKey, content)
f = open("../Imagenes/" + index + "-cloud-config.txt", "w")
f.write(cloudConfig)
f.close()

print("Ejecutando sudo ../CloudInit/crearQcow.sh {0} {1} ...".format(img, index))
#subprocess.call(["bash", "../CloudInit/crearQcow.sh", img, index], shell=True)
os.system("sudo bash ../CloudInit/crearQcow.sh {0} {1}".format(img, index))
os.system("sleep 2")



#print(cloudConfig)
print("Construyendo domainConfig.xml ...")
hwTemplatePath = templatePath + "domainConfig.xml"
name = "test"
mem = "1024"
cantCpu = "1"
disksArray = [{'type':'disk', 'path':'/var/lib/libvirt/images/{0}-{1}-DISK.img'.format(index,img), 'hdType':'hdc'}, {'type':'cdrom', 'path':'/var/lib/libvirt/images/{0}-{1}-CLOUD.iso'.format(index, img), 'hdType':'hdc'}]

#disksArray = [{'type':'cdrom', 'path':'/var/lib/libvirt/images/{0}-{1}-DISK.img'.format(index,img), 'hdType':'hdc'}]



ifacesArray = [{'name':'enp2s0', 'type':'ethernet', 'mac':'26:c7:a9:96:a7:7a', 'targetDev':'tap0'}]

xmlConfig = lT.xmlConfig(hwTemplatePath, name, mem, cantCpu, disksArray, ifacesArray)
#print(xmlConfig)

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
