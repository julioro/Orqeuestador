#!/bin/bash
tarjetas=$(lspci -Dnn | grep "Ethernet .* Virtual Function" | awk '{print $1}')
echo $tarjetas
