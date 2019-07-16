#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
#REP="/var/lib/libvirt/images"
IMG=$1
INDEX=$2
REP=$3

sudo qemu-img create -f qcow2 -b $REP/$IMG $REP/$INDEX/boot-disk.img
echo -e "Creado disco:\t$REP/$INDEX/boot-disk.img"
sudo genisoimage -output $REP/$INDEX/seed.iso -volid cidata -joliet -rock $DIR/../Imagenes/$INDEX/meta-data $DIR/../Imagenes/$INDEX/user-data
echo -e "Creado iso:\t$DIR/../Imagenes/$INDEX/meta-data & user-data"
