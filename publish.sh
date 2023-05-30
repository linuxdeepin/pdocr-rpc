#!/bin/bash
rm -rf ./dist
rm -rf ./pdocr_rpc.egg-info

python3 -m build
twine upload dist/*