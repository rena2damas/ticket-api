#!/usr/bin/env bash

set -euo pipefail

if ! kubectl get deployment --selector app=ticket-api ||
  ! kubectl get pod --selector app=ticket-bridge; then
  echo "--- :boom: Missing resources"
  exit 1
else
  # base location for services
  basedir=".kustomization/components"
  newImage="${REGISTRY}/${REGISTRY_REPOSITORY}/${IMAGE_NAME}:${IMAGE_TAG}"
  (cd "${basedir}/" && kustomize edit set image "$newImage")

  # restart api service
  kustomize build "${basedir}/api/deployment.yaml" | kubectl apply -f -
  kubectl logs --selector app=ticket-api --follow &
  kubectl wait --for condition=running --timeout=300s pods/ticket-api

  # restart bridge service
  kustomize build "${basedir}/bridge/pod.yaml" | kubectl apply -f -
  kubectl logs --selector app=ticket-bridge --follow &
  kubectl wait --for condition=running --timeout=300s pods/ticket-bridge
fi
