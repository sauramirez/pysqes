#!/bin/bash
source ~/.bash_profile

echo "Running tests"
workon pysqes
tox
