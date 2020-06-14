#!/bin/bash
echo 'removing lock & shrinkwrap file'
rm -f package-lock.json
rm -f npm-shrinkwrap.json
echo 'removing node_modules dir'
rm -rf node_modules
echo 'running uninstall'
npm uninstall
echo 'cp npm-shringwrap.json'
cp npm-shrinkwrap-json.bak npm-shrinkwrap.json
