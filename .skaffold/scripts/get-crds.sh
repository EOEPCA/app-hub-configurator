#!/bin/bash

# Base URL for CRDs
BASE_URL="https://raw.githubusercontent.com/crossplane/crossplane/refs/tags/v1.18.2/cluster/crds"

# List of CRDs in the Crossplane repository
CRDS=(
  "apiextensions.crossplane.io_compositeresourcedefinitions.yaml"
  "apiextensions.crossplane.io_compositions.yaml"
  "apiextensions.crossplane.io_compositionrevisions.yaml"
  "pkg.crossplane.io_configurations.yaml"
  "pkg.crossplane.io_locks.yaml"
  "pkg.crossplane.io_providers.yaml"
  "pkg.crossplane.io_configurationrevisions.yaml"
  "pkg.crossplane.io_controllerconfigs.yaml"
  "pkg.crossplane.io_deploymentruntimeconfigs.yaml"
  "apiextensions.crossplane.io_environmentconfigs.yaml"
  "pkg.crossplane.io_functionrevisions.yaml"
  "pkg.crossplane.io_functions.yaml"
  "pkg.crossplane.io_imageconfigs.yaml"
  "pkg.crossplane.io_providerrevisions.yaml"
  "secrets.crossplane.io_storeconfigs.yaml"
  "apiextensions.crossplane.io_usages.yaml"
)

# Apply each CRD 
echo "Installing Crossplane CRDs..."
for CRD in "${CRDS[@]}"; do
    kubectl apply -f "$BASE_URL/$CRD" --server-side
done

echo "CRD installation script completed."
