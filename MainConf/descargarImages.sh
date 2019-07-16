#!/bin/bash
if [ "$#" -ne 1 ]; then
	echo "Especificar home del usuario"
fi

# Se crea la carpeta donde se guardara todo
mkdir -p $1/images
cd $1/images

# Se descarga las imagenes de Ubuntu y CentOS
wget https://cloud-images.ubuntu.com/bionic/current/bionic-server-cloudimg-amd64.img -O bionic-server-cloudimg-amd64.img
wget https://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud.qcow2 -O CentOS-7-x86_64-GenericCloud.qcow2

# Se descarga el kernel y initrd de CentOS y Ubuntu

# Ubuntu
cp $1/Orquestador/Kernel/vmlinuz-ubuntu $1/images/vmlinuz-ubuntu
cp $1/Orquestador/Kernel/initrd-ubuntu $1/images/initrd-ubuntu

# CentOS
cp $1/Orquestador/Kernel/vmlinuz-centos $1/images/vmlinuz-centos
cp $1/Orquestador/Kernel/initrd-centos $1/images/initrd-centos
