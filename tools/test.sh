#!/bin/bash

TESTS='/home/victor/coding/projects/yaps/tests'
PY_ENV='/home/victor/coding/projects/yaps/env'

VIRTUAL_ENV=$PY_ENV
export VIRTUAL_ENV

PATH="$VIRTUAL_ENV/bin:$PATH"
export PATH

for file in $(ls $TESTS) ;  do
	python ${TESTS}/$file
done
