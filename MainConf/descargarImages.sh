#!/bin/bash

# Se crea la carpeta donde se guardara todo
mkdir -p $1
cd $1

# Se descarga las imagenes de Ubuntu y CentOS
wget https://cloud-images.ubuntu.com/bionic/current/bionic-server-cloudimg-amd64.img -O bionic-server-cloudimg-amd64.img
wget https://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud.qcow2 -O CentOS-7-x86_64-GenericCloud.qcow2

# Se descarga el kernel y initrd de CentOS y Ubuntu

# Ubuntu
wget https://cloud-images.ubuntu.com/bionic/current/unpacked/bionic-server-cloudimg-amd64-vmlinuz-generic -O vmlinuz-ubuntu
wget https://cloud-images.ubuntu.com/bionic/current/unpacked/bionic-server-cloudimg-amd64-initrd-generic -O initrd-ubuntu

# CentOS
wget http://mirror.centos.org/centos/7/os/x86_64/images/pxeboot/vmlinuz -O vmlinuz-centos
wget http://mirror.centos.org/centos/7/os/x86_64/images/pxeboot/initrd.img -O initrd-centos
