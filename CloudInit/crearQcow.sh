#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
IMG=$1
INDEX=$2
rm -rf $DIR/../Imagenes/$INDEX-$IMG.img
#rm -rf $DIR/../Imagenes/$INDEX-cloud-config.img 
cp $DIR/../Imagenes/000-$IMG.img $DIR/../Imagenes/$INDEX-$IMG.img
qemu-img create -f qcow2 -b $DIR/../Imagenes/$INDEX-$IMG.img /var/lib/libvirt/images/$INDEX-$IMG-DISK.img
echo "Creado /var/lib/libvirt/images/$INDEX-$IMG-DISK.img"
cloud-localds /var/lib/libvirt/images/$INDEX-$IMG-CLOUD.iso $DIR/../Imagenes/$INDEX-cloud-config.txt
echo "Creado /var/lib/libvirt/images/$INDEX-$IMG-CLOUD.iso"
