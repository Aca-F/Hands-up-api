#!/bin/bash

REPO_URL="https://github.com/Aca-F/Hands-up-api.git"
CLONE_DIR="Hands-up-api"
IMAGE_NAME="aleksandar-hands-up"
CONTAINER_NAME="aleksandar-hands-up-container"
HOST_PORT=8000
CONTAINER_PORT=8000

cleanup() {
    echo "Stopping and removing Docker container..."
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME

    echo "Removing Docker image..."
    docker rmi $IMAGE_NAME

    echo "Deleting cloned repository..."
    cd ..
    rm -rf $CLONE_DIR

    echo "Cleanup complete."
}


setup(){
    echo "Cloning repository..."
    git clone $REPO_URL $CLONE_DIR
    cd $CLONE_DIR
    echo "Building Docker image..."
    docker build -t $IMAGE_NAME .
}


run_container(){
    echo "Running Docker container..."
    docker run --name $CONTAINER_NAME -d -p $HOST_PORT:$CONTAINER_PORT $IMAGE_NAME
}

run_tests() {
    echo "Running tests..."
    docker run --rm $IMAGE_NAME pytest -v
}

trap cleanup EXIT

echo "Warning: This script will clone the repository and build a Docker image."
read -p "Do you want to continue? (yes/no): " choice
case "$choice" in
  yes|Yes|YES|y|Y )
    echo "Proceeding with the script..."
    ;;
  no|No|NO|n|N )
    echo "Exiting script."
    exit 1
    ;;
  * )
    echo "Invalid choice. Exiting script."
    exit 1
    ;;
esac

setup

PS3='Please enter your choice: '
options=("Run tests" "Run application" "Quit")
select opt in "${options[@]}"
do
    case $opt in
        "Run tests")
            run_tests
            ;;
        "Run application")
            run_container
            echo "Application is running. Press Ctrl+C to stop and clean up. Open http://localhost:8000/docs#/ for Swagger."
            while true; do
                sleep 1
            done
            ;;
        "Quit")
            break
            ;;
        *) echo "invalid option $REPLY";;
    esac
done


