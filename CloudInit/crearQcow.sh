#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
#REP="/var/lib/libvirt/images"
REP="/home/labtel/images"
IMG=$1
INDEX=$2

sudo qemu-img create -f qcow2 -b $REP/$IMG $REP/$INDEX/boot-disk.img
sudo echo -e "Creado disco:\t$REP/$INDEX/boot-disk.img"
sudo genisoimage -output $REP/$INDEX/seed.iso -volid cidata -joliet -rock $DIR/../Imagenes/$INDEX/meta-data $DIR/../Imagenes/$INDEX/user-data
sudo echo -e "Creado iso:\t$DIR/../Imagenes/$INDEX/meta-data & user-data"
