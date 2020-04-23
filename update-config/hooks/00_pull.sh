#!/bin/bash

cd /config
git fetch
git diff --name-only master origin/master > changes.txt
git pull