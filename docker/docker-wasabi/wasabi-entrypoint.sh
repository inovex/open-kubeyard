#!/usr/bin/env sh

if [ "$1" = 'wasabi' ]; then
    cd /usr/local
    exec ./wasabi-main-latest-development/bin/run "$@"

elif [ "$1" = 'ui' ]; then
    cd /usr/local/wasabi-ui/
    exec grunt serve
fi

exec "$@"