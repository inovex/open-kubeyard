#!/bin/bash

set -eu

[ -d /var/lib/druid/tmp ] || mkdir /var/lib/druid/tmp

exec "$@"
