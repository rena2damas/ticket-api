#!/usr/bin/env bash

set -euo pipefail

if ! kubectl get deployment --selector app=ticket-api ||
  ! kubectl get pod --selector app=ticket-bridge; then
  echo "--- :boom: Missing resources"
  exit 1

# create kustomization context
cwd=$(pwd)
ctx=$(mktemp -dt tmp.deploy.XXXXXX)
cd $ctx

basedir=".kustomization/components"
newImage="${REGISTRY}/${REGISTRY_REPOSITORY}/${IMAGE_NAME}:${IMAGE_TAG}"

# set kustomization file used to restart services
kustomize create
kustomize edit add resource "${cwd}/${basedir}/api/deployment.yaml"
kustomize edit add resource "${cwd}/${basedir}/bridge/pod.yaml"
kustomize edit set image "$newImage"

# restart api & bridge service
kustomize build . | kubectl replace -f -
kubectl logs --selector app=ticket-api --follow &
kubectl logs --selector app=ticket-bridge --follow &

# wait service conclusion
kubectl wait --for condition=running --timeout=300s pods/ticket-api
kubectl wait --for condition=running --timeout=300s pods/ticket-bridge

# cleanup
rm -rf -- "$tmpdir"
