#!/bin/bash
# FIRST EXPORT $HELM_REPO with the path to the local directory which helm serves on
# SECOND Make sure you have a local repo running
# helm serve --repo-path $HELM_REPO

: "${HELM_REPO:?You need to set environment variable HELM_REPO}"

# change into helm directory
mkdir -p $HELM_REPO
cd $HELM_REPO
cd ..

# delete all 'charts' directories
find . -name charts -type d -exec rm -r {} +

mkdir charts

helm serve --repo-path $HELM_REPO &
helm repo add charts http://127.0.0.1:8879/charts &

if [ ! -z $1 ] ; then
    echo -e "\e[1;34m[INFO] \e[21m\e[39m Update dependecies of $1"
    helm dep update "$1/"
    echo -e "\e[1;34m[INFO] \e[21m\e[39m Package $1"
    helm package $1
    mv *.tgz $HELM_REPO
else
    numberhelmchartslastiteration="-1"

    cd charts
    numberhelmcharts="0"
    cd ..

    while [ $numberhelmchartslastiteration -lt $numberhelmcharts ]
    #if the number of helmcharts did not change since the last iteration
    #then all the (buildable) recursive dependencies have been added
    do
        numberhelmchartslastiteration=$numberhelmcharts

        #for each helm folder execute packageing
        for file in helm-*
        do
            echo -e "\e[1;34m[INFO] \e[21m\e[39m Update dependecies of $file"
            helm dep update "$file/"
            echo -e "\e[1;34m[INFO] \e[21m\e[39m Package $file"
            helm package $file
        done
        mv *.tgz $HELM_REPO

        #update the repository index so that just build dependencies can be found
        helm repo index $HELM_REPO

        #see how many helmcharts are in the charts folder
        cd charts
        numberhelmcharts="$( ls -d helm-* | wc -l)"
        cd ..

    done
fi

# Test if all charts have been packaged by comparing number of charts with number of packages
no_of_charts="$(ls | grep "helm" | wc -l)"
no_of_packaged_charts="$(ls $HELM_REPO | grep "helm" | wc -l)"

if [ $no_of_charts -ne $no_of_packaged_charts ]; then
    echo "Packaging Failed"
    exit 1
else
    echo "Packaging Succeeded"
fi
