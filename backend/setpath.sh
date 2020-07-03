#!/bin/bash
echo $PYTHONPATH
echo 'setting module to python path...'
export PYTHONPATH=$PYTHONPATH:.:${PWD}/batch:${PWD}/daemon:${PWD}/pubsub:${PWD}/integration:${PWD}/test:${PWD}/../common
echo $PYTHONPATH

