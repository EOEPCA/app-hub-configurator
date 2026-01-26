#!/bin/bash

# function to check if provider is healthy
check_provider_health() {
    local provider=$1
    local timeout=$2
    local interval=$3
    local start_time=$(date +%s)
    
    echo "Waiting for provider-$provider to have status True where type is Healthy..."
    
    # Loop until the condition is met or timeout
    while true; do
        # Get the status of the "Healthy" condition
        status=$(kubectl get provider.pkg.crossplane.io/provider-$provider -o jsonpath='{.status.conditions[?(@.type=="Healthy")].status}')
        
        # If the status is True, exit the loop
        if [[ "$status" == "True" ]]; then
            echo "Provider $provider is Healthy."
            break
        fi
        
        # Check if the timeout has been reached
        current_time=$(date +%s)
        elapsed_time=$((current_time - start_time))
        
        if (( elapsed_time >= timeout )); then
            echo "Timeout reached. Provider $provider did not become Healthy in time."
            exit 2
        fi
        
        # Sleep for the interval before checking again
        sleep $interval
    done
}

# function to check if CRD is established
check_crd_established() {
    local crd=$1
    local timeout=$2
    
    echo "Waiting for CRD $crd to be established..."
    
    kubectl wait --for=condition=established crd/$crd --timeout=${timeout}s
}

# Timeout duration
TIMEOUT=180
# Check interval in seconds
INTERVAL=5
# Start time
START_TIME=$(date +%s)

# helm provider
echo "Applying Helm provider configuration..."
kubectl apply -f provider/helm.yaml || exit 1

# invoke function to check if provider is healthy
check_provider_health helm $TIMEOUT $INTERVAL || exit 2

check_crd_established providerconfigs.helm.crossplane.io $TIMEOUT || exit 2

echo "Applying helm-provider-config.yaml..."
kubectl apply -f provider-config/helm.yaml || exit 3

# kubernetes provider
echo "Applying Kubernetes provider configuration..."
kubectl apply -f provider/kubernetes.yaml || exit 4

check_provider_health kubernetes $TIMEOUT $INTERVAL

check_crd_established providerconfigs.kubernetes.crossplane.io $TIMEOUT || exit 5

echo "Applying kubernetes-provider-config.yaml..."
kubectl apply -f provider-config/kubernetes.yaml || exit 6