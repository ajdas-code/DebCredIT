#!/bin/bash
echo $PYTHONPATH
echo 'setting module to python path...'
export PYTHONPATH=$PYTHONPATH:.:$PYTHONPATH/models:$PYTHONPATH/config:$PYTHONPATH/test
echo $PYTHONPATH
cd ./test
