1. api


```bash
git clone git@github.com:SuCicada/amis-admin-editor.git temp/amis-editor
git clone --no-hardlinks temp/amis-editor amis-editor
git subtree add --prefix amis-editor temp/amis-editor master
mkdir amis-editor


#https://harttle.land/2016/03/22/purge-large-files-in-gitrepo.html
# show big history
git rev-list --objects --all | grep "$(git verify-pack -v .git/objects/pack/*.idx | sort -k 3 -n | tail -5 | awk '{print$1}')"
# remove big history

git filter-branch -f --prune-empty \
  --index-filter 'git rm -rf --cached --ignore-unmatch amis-editor/gh-pages/* amis-editor/public/* amis-editor/demo* ' \
  --tag-name-filter cat -- --all
  
#git filter-branch -f --prune-empty \
#  --index-filter 'git rm -rf --cached --ignore-unmatch amis-editor/gh-pages/* amis-editor/public/* amis-editor/demo* ' \
#  --tag-name-filter cat -- --all
```

