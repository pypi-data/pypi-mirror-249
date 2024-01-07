#!/bin/bash
# to install any new requirements call with --update-requirements

echo "$ - running unit tests"

venv_path='./test-venv'

install_libs=false

for var in "$@"
do
    if [ "$var" = '--update-requirements' ]; then 
        install_libs=true 
    fi
done

if ! [ -d $venv_path ]; then
    echo "$ - venv not found, will generate one"
    python3.10 -m venv $venv_path
    install_libs=true
fi

source $venv_path/bin/activate
echo "$ - venv sourced, using: "$(which python3.10) 

if [ "$install_libs" = true ]; then
    echo "$ - installing requirements"
    python3.10 -m pip install -r ./test-requirements.txt 
    echo "$ - done"
fi

test_files=$(ls ./test/test_*.py 2>/dev/null)
test_file_count=$(echo $test_files | grep -o "\.py" | wc -l)

if [ $test_file_count -eq 0 ]; then
    echo "$ - WARNING - didn't not find any test files, nothing to do here"
else
    echo "$ - found" $test_file_count "test files, will run"
    PYTHONPATH=./test python3.10 -m pytest --cov-config .coveragerc --cov=src --cov-report html --verbose $test_files
    
    if [[ $? -ne 0 ]]; then
        echo "$ - ERROR: tests failed!"
        exit -1
    fi
    python3.10 -m coverage report
fi
