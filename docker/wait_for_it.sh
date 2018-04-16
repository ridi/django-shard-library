#!/bin/bash

check_command="$1"
shift
command="$@"

while true; do
    $check_command &> /dev/null
    if [ $? -eq 0 ]; then
        break
    fi
    echo "Waiting."
    sleep 1
done

exec $command
