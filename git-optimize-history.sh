#!/bin/bash
cd ./temp/amis-editor/

git rev-list --objects --all | grep "$(git verify-pack -v .git/objects/pack/*.idx | sort -k 3 -n | tail -5 | awk '{print$1}')"

git filter-branch -f --prune-empty \
  --index-filter 'git rm -rf --cached --ignore-unmatch gh-pages/* public/* demo* icons/* n/* pkg/* ' \
  --tag-name-filter cat -- --all


cd -
