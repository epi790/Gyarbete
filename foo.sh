#!/bin/bash

counter=0

while true
do
  echo $counter
  qr $counter > qr.img
  counter=$((counter+1))
  sleep 5
done
