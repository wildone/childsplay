#!/usr/bin/env bash

eval $(ssh-agent -s)
ssh-add - <<< "$(cat /build/.ssh/id_rsa)"
ssh -oStrictHostKeyChecking=no $1