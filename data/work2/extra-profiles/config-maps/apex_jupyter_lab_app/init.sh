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


cd /workspace
# -------------------------
# Python virtual environment
# -------------------------
python -m venv /workspace/.venv
. /workspace/.venv/bin/activate

/workspace/.venv/bin/python -m pip install --no-cache-dir \
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

/workspace/.venv/bin/python -m pip install --no-cache-dir cwltool==3.1.20241112140730 ipykernel 
# -------------------------
# Register Jupyter kernel
# -------------------------
/workspace/.venv/bin/python -m ipykernel install \
    --prefix=/workspace/.local \
    --name OpenEO \
    --display-name "OpenEO"


# -------------------------
# Env
# -------------------------
chmod -R 777 /workspace/.local
chmod -R 777 /workspace/eoap/
chmod -R 777 /workspace/openeo/
mkdir -p /workspace/.podman
chmod -R 777 /workspace/.venv/
chown -R 1001:100 /workspace/.podman
chmod -R 775 /workspace/.podman

export PATH=$PATH:/workspace/.venv/bin
## AWS environment variables
export SEAWEEDFS_S3_ENDPOINT=http://seaweedfs-s3:8333
export AWS_ACCESS_KEY_ID=s3
export AWS_SECRET_ACCESS_KEY=s3
export AWS_DEFAULT_REGION=us-east-1
export AWS_ENDPOINT_URL=${SEAWEEDFS_S3_ENDPOINT}

aws s3 mb s3://results --endpoint-url=${AWS_ENDPOINT_URL} || true