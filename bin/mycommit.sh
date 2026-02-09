#!/bin/bash
m=${1:-""}
d=`date '+%d-%m-%y (%H:%M)'`
msg="${d} ${m}"
echo $msg
git add -A
git commit -m "${msg}"
