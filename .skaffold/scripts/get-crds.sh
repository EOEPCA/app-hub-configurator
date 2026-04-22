#!/bin/bash
set -euo pipefail

# Base URL for CRDs
BASE_URL="https://raw.githubusercontent.com/crossplane/crossplane/v2.2.0/cluster/crds"

# List of CRDs in the Crossplane repository
CRDS=(
  "apiextensions.crossplane.io_compositeresourcedefinitions.yaml"
  "apiextensions.crossplane.io_compositionrevisions.yaml"
  "apiextensions.crossplane.io_compositions.yaml"
  "apiextensions.crossplane.io_environmentconfigs.yaml"
  "apiextensions.crossplane.io_managedresourceactivationpolicies.yaml"
  "apiextensions.crossplane.io_managedresourcedefinitions.yaml"
  "apiextensions.crossplane.io_usages.yaml"
  "ops.crossplane.io_cronoperations.yaml"
  "ops.crossplane.io_operations.yaml"
  "ops.crossplane.io_watchoperations.yaml"
  "pkg.crossplane.io_configurationrevisions.yaml"
  "pkg.crossplane.io_configurations.yaml"
  "pkg.crossplane.io_deploymentruntimeconfigs.yaml"
  "pkg.crossplane.io_functionrevisions.yaml"
  "pkg.crossplane.io_functions.yaml"
  "pkg.crossplane.io_imageconfigs.yaml"
  "pkg.crossplane.io_locks.yaml"
  "pkg.crossplane.io_providerrevisions.yaml"
  "pkg.crossplane.io_providers.yaml"
  "protection.crossplane.io_clusterusages.yaml"
  "protection.crossplane.io_usages.yaml"
)

# Apply each CRD 
echo "Installing Crossplane CRDs..."
for CRD in "${CRDS[@]}"; do
    kubectl apply --server-side -f "$BASE_URL/$CRD"
done

echo "CRD installation script completed."
