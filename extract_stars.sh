#!/bin/zsh

tail -n +3 $1 | tr -s ' ' | cut -d ' ' -f 1,2,4,5 | awk -F ' ' '/1/ {printf "Star(%f, %f, %f, %f),\n", $3, $4, $1, $2}'