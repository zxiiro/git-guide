#!/bin/bash

cp .nojekyll site
cd site
git add .
git commit -sm "Update site $(date +'%Y%m%d-%H%M')"
git push
