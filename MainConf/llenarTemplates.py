#!/usr/bin/python3
from jinja2 import Template
import sys

def xmlConfig(templatePath, name, mem, cantCpu, disksArray, ifacesArray):
    with open(templatePath, 'r') as f:
        xmlConf = f.read()
        template = Template(xmlConf)
        return template.render(name=name, mem=mem, cantCpu=cantCpu, disksArray=disksArray, ifacesArray=ifacesArray)

def cloudConfig(templatePath, index, name, sshPubKey, content):
    with open(templatePath, 'r') as f:
        cloudConf = f.read()
        template = Template(cloudConf)
        return template.render(index=index, name=name, sshPubKey=sshPubKey, content=content)

def ga():
    print(2)
