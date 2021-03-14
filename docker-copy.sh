#!/usr/bin/env bash

eval $(ssh-agent -s)
ssh-add - <<< "$(cat /build/.ssh/id_rsa)"
scp -oStrictHostKeyChecking=no ${1} ${2}:~