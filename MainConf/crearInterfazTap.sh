#!/bin/bash
sudo ip link del dev tap$1
sudo ip tuntap add dev tap$1 mode tap
sudo ip link set dev tap$1 address $2
sudo ip link set dev tap$1 up
sudo ip link show tap$1