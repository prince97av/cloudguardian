#!/bin/bash

function install_cloudguardian {
    echo "Installing CloudGuardian"
    setup_develop $CLOUDGUARDIAN_DIR
}

function start_cloudguardian {
    echo "Starting CloudGuardian"
    run_process cloudguardian "python3 $CLOUDGUARDIAN_DIR/cloudguardian/app.py"
}

function stop_cloudguardian {
    echo "Stopping CloudGuardian"
}

function cleanup_cloudguardian {
    echo "Cleaning CloudGuardian"
}

if [[ "$1" == "stack" && "$2" == "install" ]]; then
    install_cloudguardian
elif [[ "$1" == "stack" && "$2" == "extra" ]]; then
    start_cloudguardian
elif [[ "$1" == "unstack" ]]; then
    stop_cloudguardian
elif [[ "$1" == "clean" ]]; then
    cleanup_cloudguardian
fi
