#!/bin/sh
set -eu

check_provider_health() {
    provider=$1
    timeout=$2
    interval=$3
    start_time=$(date +%s)

    echo "Waiting for provider-$provider to have status True where type is Healthy..."

    while true; do
        status=$(kubectl get "provider.pkg.crossplane.io/provider-$provider" -o jsonpath='{.status.conditions[?(@.type=="Healthy")].status}')
        echo "Current status of provider $provider: $status"
        if [ "$status" = "True" ]; then
            echo "Provider $provider is Healthy."
            break
        fi

        current_time=$(date +%s)
        elapsed_time=$((current_time - start_time))

        if [ "$elapsed_time" -ge "$timeout" ]; then
            echo "Timeout reached. Provider $provider did not become Healthy in time."
            exit 2
        fi

        sleep "$interval"
    done
}

check_crd_established() {
    crd=$1
    timeout=$2

    echo "Waiting for CRD $crd to be established..."
    kubectl wait --for=condition=established "crd/$crd" --timeout="${timeout}s"
}

check_provider_config_crds() {
    timeout=$1
    shift

    for crd in "$@"; do
        check_crd_established "$crd" "$timeout"
    done
}

TIMEOUT=180
INTERVAL=5

echo "Applying Helm provider configuration..."
kubectl apply -f .skaffold/provider/helm.yaml || exit 1

check_provider_health helm "$TIMEOUT" "$INTERVAL" || exit 2

check_provider_config_crds "$TIMEOUT" \
    providerconfigs.helm.crossplane.io \
    providerconfigs.helm.m.crossplane.io || exit 2

echo "Applying helm-provider-config.yaml..."
kubectl apply -f .skaffold/provider-config/helm.yaml || exit 3

echo "Applying Kubernetes provider configuration..."
kubectl apply -f .skaffold/provider/kubernetes.yaml || exit 4

check_provider_health kubernetes "$TIMEOUT" "$INTERVAL" || exit 4

check_provider_config_crds "$TIMEOUT" \
    providerconfigs.kubernetes.crossplane.io \
    providerconfigs.kubernetes.m.crossplane.io || exit 5

echo "Applying kubernetes-provider-config.yaml..."
kubectl apply -f .skaffold/provider-config/kubernetes.yaml || exit 6
