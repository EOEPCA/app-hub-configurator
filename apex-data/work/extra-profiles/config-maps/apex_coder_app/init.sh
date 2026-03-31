#!/bin/bash
set -x 

cd /workspace

# -------------------------
# Clone repositories
# -------------------------
rm -rf eoap openeo
mkdir -p eoap
cd eoap
git clone https://github.com/eoap/cwl-eoap.git
git clone https://github.com/eoap/stac-eoap.git
git clone https://github.com/eoap/quickwin.git

cd /workspace
mkdir -p openeo
cd openeo
git clone --no-checkout https://github.com/Open-EO/openeo-community-examples.git
cd openeo-community-examples
git sparse-checkout init --cone
git sparse-checkout set \
  "python/1. GettingStarted/GettingStarted.ipynb" \
  "python/LoadStac/load-stac-item-example.ipynb" \
  "python/BioPAR/biopar_service.ipynb"
git checkout main
git checkout 738d1710918ad937c2d79c49436c6e7ca2abd3dd -- \
  python/BioPAR/biopar_service.ipynb

# -------------------------
# VS Code extensions
# -------------------------
# Install VS Code Extensions
code-server --install-extension ms-python.python 
code-server --install-extension redhat.vscode-yaml
code-server --install-extension sbg-rabix.benten-cwl
code-server --install-extension ms-toolsai.jupyter
ln -s /workspace/.local/share/code-server/extensions /workspace/extensions

# Setup user settings
mkdir -p /workspace/User/
echo '{"workbench.colorTheme": "Visual Studio Dark"}' > /workspace/User/settings.json
echo '[
            {
                "key": "ctrl+c",
                "command": "workbench.action.terminal.copySelection",
                "when": "terminalFocus && terminalTextSelected"
            },
            {
                "key": "ctrl+v",
                "command": "workbench.action.terminal.paste",
                "when": "terminalFocus"
            }
            ]' > /workspace/User/keybindings.json

# -------------------------
# Python virtual environment
# -------------------------
python -m venv /workspace/.venv
. /workspace/.venv/bin/activate

# Upgrade pip and install minimal packages
chmod -R 777 /workspace/.ipython
/workspace/.venv/bin/python -m pip install --upgrade pip
python -m pip install --no-cache-dir \
  openeo \
  click \
  asyncclick \
  click-logging \
  requests \
  numpy \
  tqdm \
  tabulate \
  ipython \
  ipykernel \
  loguru \
  shapely \
  pyproj \
  rasterio \
  scikit-image \
  pystac \
  pystac-client \
  stactools \
  stactools-sentinel2 \
  stac-asset \
  rio-stac \
  boto3 \
  graphviz \
  yq \
  cwl-utils \
  cwl-loader \
  eoap-cwlwrap \
  mkdocs-material \
  mkdocs-mermaid2-plugin \
  anyio \
  matplotlib
/workspace/.venv/bin/python -m pip install --no-cache-dir cwltool==3.1.20241112140730 

# -------------------------
# Register Jupyter kernel
# -------------------------

/workspace/.venv/bin/python -m ipykernel install --name openeo-env --display-name "OpenEO" --sys-prefix
# -------------------------
# Permissions (safe)
# -------------------------
mkdir -p /workspace/.podman
chmod -R 777 /workspace/.local /workspace/.venv /workspace/User \
    /workspace/eoap /workspace/openeo /workspace/.podman

## AWS environment variables
export SEAWEEDFS_S3_ENDPOINT=http://seaweedfs-s3:8333
export AWS_ACCESS_KEY_ID=s3
export AWS_SECRET_ACCESS_KEY=s3
export AWS_DEFAULT_REGION=us-east-1
export AWS_ENDPOINT_URL=${SEAWEEDFS_S3_ENDPOINT}

aws s3 mb s3://results --endpoint-url=${AWS_ENDPOINT_URL} || true
