#!/usr/bin/python3
from jinja2 import Template
import sys

def xmlConfig(templatePath, name, mem, cantCpu, disksArray, ifacesArray):
    with open(templatePath, 'r') as f:
        xmlConf = f.read()
        template = Template(xmlConf)
        return template.render(name=name, mem=mem, cantCpu=cantCpu, disksArray=disksArray, ifacesArray=ifacesArray)

def cloudConfig(userDataPath, metaDataPath, index, name, sshKeyArray, fileArray, userArray):
    with open(userDataPath, 'r') as f:
        userData = f.read()
        templateUserData = Template(userData)
        udt = templateUserData.render(index=index, name=name, sshKeyArray=sshKeyArray, fileArray=fileArray, userArray=userArray)

    with open(metaDataPath, 'r') as f:
        metaData = f.read()
        templateMetaData = Template(metaData)
        mdt = templateMetaData.render(index=index, name=name)

    return udt, mdt


def ga():
    print(2)
