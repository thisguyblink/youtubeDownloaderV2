#!/bin/bash

fileDirectory="downloadedFiles"
for file in "$fileDirectory"/*; do
  extension="${file: -3}"
  if [[ "$extension" == "m4a" ]]; then
    rm -f "$file"
  fi
done