#!/bin/bash
echo $PYTHONPATH
echo 'setting module to python path...'
export PYTHONPATH=$PYTHONPATH:.:${PWD}:${PWD}/util:${PWD}/test:${PWD}/version_1:${PWD}/version_1/resources
echo $PYTHONPATH

