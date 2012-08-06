#!/bin/bash

echo "Setting up dotfiles: ..."
LINK_DIR=`cd $(dirname "$0"); pwd`
echo "Linking from: $LINK_DIR"
echo "Linking to: $HOME"

for file in $LINK_DIR/*
do
    echo "ln -ns $file ~/.$(basename $file)"
    ln -ns $file ~/.$(basename $file)
done