#!/usr/bin/env bash
# This script deploys the built site to the prod-pages branch of the same repo.
git config --global user.email $GH_EMAIL
git config --global user.name $GH_NAME

# CircleCI will identify the SSH key with a "Host" of gh-prod. In order to tell
# Git to use this key, we need to hack the SSH key:
sed -i -e 's/Host gh-stg/Host gh-stg\n  HostName github.com/g' ~/.ssh/config
git clone git@gh-stg:$GH_ORG_STG/$CIRCLE_PROJECT_REPONAME.git out

cd out
git checkout prod-pages || git checkout --orphan prod-pages
git rm -rfq .
cd ..

# The fully built site is already available at /tmp/build.
cp -a /tmp/build/_site/. out/.

mkdir -p out/.circleci && cp -a .circleci/. out/.circleci/.
cd out

git add -A
git commit -m "Automated deployment to GitHub Pages: ${CIRCLE_SHA1}" --allow-empty

git push origin prod-pages