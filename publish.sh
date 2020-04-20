#!/bin/bash

export PRE_COMMIT_ALLOW_NO_CONFIG=1

cp .nojekyll /tmp/site
cd /tmp/site
git add .
git commit -sm "Update site $(date +'%Y%m%d-%H%M')"
git push
