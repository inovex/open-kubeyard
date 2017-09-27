#!/bin/bash

# Script to build all docker images and push them in the docker reg
# 
# 21.04.17
# drohatschek



function build {
     echo -e "\e[1;34m[INFO] \e[21m\e[39mBuild image $1"
    docker build -t registry.inovex.de:4567/inovex-kubeyard/"$1" "./$1"
    let result=$?
    local isSuccessfull
    if [ $result -eq 0 ]; then
        echo -e "\e[1;32m[OK] \e[21m\e[39mBuilding $1 successfull "
        let isSuccessfull=0
    else 
        echo -e "\e[1;31m[ERR] \e[21m\e[39m Building $1 failed "
        while true; do
            read -p "Continue with next image? (y/n)" yn
            case $yn in
                [Yy]* ) let isSuccessfull=1; break;;
                [Nn]* ) exit;;
                * ) echo "Please answer yes or no.";;
            esac
        done
    fi
    return $isSuccessfull
}

function push {
    echo -e "\e[1;34m[INFO] \e[21m\e[39mPush image $1"
    docker push registry.inovex.de:4567/inovex-kubeyard/"$1"
    let result=$?
    local isSuccessfull
    if [ $result -eq 0 ]; then
        echo -e "\e[1;32m[OK] \e[21m\e[39mPushing $1 successfull "
        else 
        echo -e "\e[1;31m[ERR] \e[21m\e[39mPush $1 failed "
        while true; do
            read -p "Continue with next image? (y/n)" yn
            case $yn in
                [Yy]* ) break;;
                [Nn]* ) exit;;
                * ) echo "Please answer yes or no.";;
            esac
        done
    fi
}

while test $# -gt 0; do
    case "$1" in 
        -h|--help)
            echo "buildImages.sh [options]"
            echo "-u [user]"
            echo "-t [token]"
            echo "-i [image]"
            exit 0
            ;;
        -u)
            shift
            if test $# -gt 0; then
                export user=$1
            else
                echo "no user defined"
                exit 1
            fi
            shift
            ;;
        -t)
            shift
                if test $# -gt 0; then
                    export token=$1
                else
                    echo "no token defined"
                    exit 1
                fi
            shift
            ;;
        -i)
            shift
                if test $# -gt 0; then
                    export image=$1
                else
                    echo "no user defined"
                    exit 1
                fi
            shift
            ;;
        *)
            break
            ;;
    esac
done

# Login to docker registry
if [ ! -z "$user" ] && [ ! -z "$token" ]; then
    echo "Login to Docker Registry"
    docker login -u "$user" -p "$token" registry.inovex.de:4567
fi

echo -e "\e[1;34m[INFO] \e[21m\e[39mBuilding images."

# Loop through subdirectories and build images

if [ ! -z "$image" ]; then
    build $image
    if [ "$?" -eq 0 ]; then
        push $image
    fi
else 
    for file in docker-*
    do
        build $file
        if [ "$?" -eq 0 ]; then
            push $file
        fi
    done
fi



