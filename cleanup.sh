#!/bin/bash

folder=$1
type=$2
removeType=$([[ "$2" == "m4a" ]] && echo "mp3" || echo "m4a")
rm -f "$1"/*.$removeType