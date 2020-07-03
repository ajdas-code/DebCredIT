#!/bin/bash
echo $PYTHONPATH
echo 'setting module to python path...'
export PYTHONPATH=$PYTHONPATH:.:${PWD}:${PWD}/models:${PWD}/config:${PWD}/test
echo $PYTHONPATH
cd ${PWD}/test
