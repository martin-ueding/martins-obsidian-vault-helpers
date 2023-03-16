#!/bin/bash

set -e
set -u

shopt -s globstar

for image in ./**/*.png; do
    echo "$image"
    convert "$image" -trim +repage "$image"
done
