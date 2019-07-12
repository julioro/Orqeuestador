#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
IMG=$1
INDEX=$2
rm $DIR/../Imagenes/$INDEX-$IMG.img
cp $DIR/../Imagenes/00-IMG.img $DIR/../Imagenes/$INDEX-$IMG.img
qemu-img create -f qcow2 -b $DIR/../Imagenes/$INDEX-$IMG.img /var/lib/libvirt/images/$INDEX-$IMG-QCOW.img
cloud-localds /var/lib/libvirt/images/$INDEX-$IMG-CLOUD.iso $DIR/../Imagenes/$INDEX-cloud-config.txt
