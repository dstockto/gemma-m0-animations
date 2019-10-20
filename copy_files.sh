#!/bin/bash

function usage() {
  echo "Usage:"
  echo "------------------------"
  echo
  echo "$0 CIRCUITPY"
  echo
  echo "Argument should be the name of your Gemma drive."
  echo 'Check to make sure Gemma is plugged in to USB and turned on.'
  echo
}

if [ $# -eq 0 ]; then
  echo
  echo "Need name of Gemma"
  echo
  usage
  exit
fi

cp main.py /Volumes/$1/main.py
cp -R lib/ /Volumes/$1/lib
