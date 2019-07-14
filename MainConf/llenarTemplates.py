#!/usr/bin/python3
from jinja2 import Template
import sys

def xmlConfig(templatePath, name, mem, cantCpu, disksArray, ifacesArray, kdb, kernelPath, initrdPath):
    with open(templatePath, 'r') as f:
        xmlConf = f.read()
        template = Template(xmlConf)
        return template.render(name=name, mem=mem, cantCpu=cantCpu, disksArray=disksArray, ifacesArray=ifacesArray, kdb=kdb, kernelPath=kernelPath, initrdPath=initrdPath)

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

def pruebaLlenado():
    templatePath = './../Template/domainConfig.xml'
    name = 'test'
    mem = 1024
    cantCpu = 2
    disksArray = [{'type': 'test', 'path': 'test', 'hdType': 'test'}]
    ifacesArray = [{'type': 'test', 'name': 'test', 'mac': 'test', 'targetDev': 'test'}]
    kdb = False
    kernelPath = 'test'
    initrdPath = 'test'

    print(xmlConfig(templatePath, name, mem, cantCpu, disksArray, ifacesArray, kdb, kernelPath, initrdPath))
