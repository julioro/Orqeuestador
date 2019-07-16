#!/bin/bash
name=$(virsh dominfo vm-$1 | grep "Name" | awk '{ print $2 }')
cpus=$(virsh dominfo vm-$1 | grep "CPU(s)" | awk '{ print $2 }')
mem=$(virsh dominfo vm-$1 | grep "Max memory: " | awk '{ print $3 " " $4 }')

echo $name $cpus $mem
