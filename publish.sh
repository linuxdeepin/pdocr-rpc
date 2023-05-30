#!/bin/bash
mkdocs gh-deploy
rm -rf ./site

rm -rf ./dist
rm -rf ./pdocr_rpc.egg-info

python3 -m build
twine upload dist/*