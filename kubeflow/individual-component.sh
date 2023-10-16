
for i in 1 2
do 
	kustomize build common/cert-manager/cert-manager/base | kubectl apply -f -
	sleep 10s
	kubectl wait --for=condition=ready pod -l 'app in (cert-manager,webhook)' --timeout=180s -n cert-manager
	sleep 10s
	kustomize build common/cert-manager/kubeflow-issuer/base | kubectl apply -f -
	sleep 10s
	kustomize build common/istio-1-16/istio-crds/base | kubectl apply -f -
	sleep 10s
	kustomize build common/istio-1-16/istio-namespace/base | kubectl apply -f -
	sleep 10s
	kustomize build common/istio-1-16/istio-install/base | kubectl apply -f -
	sleep 10s
	kustomize build common/dex/overlays/istio | kubectl apply -f -
	sleep 10s
	kustomize build common/oidc-authservice/base | kubectl apply -f -
	sleep 10s
	kustomize build common/knative/knative-serving/overlays/gateways | kubectl apply -f -
	sleep 10s
	kustomize build common/istio-1-16/cluster-local-gateway/base | kubectl apply -f -
	sleep 10s
	kustomize build common/knative/knative-eventing/base | kubectl apply -f -
	sleep 10s
	kustomize build common/kubeflow-namespace/base | kubectl apply -f -
	sleep 10s
	kustomize build common/kubeflow-roles/base | kubectl apply -f -
	sleep 10s
	kustomize build common/istio-1-16/kubeflow-istio-resources/base | kubectl apply -f -
	sleep 10s
	kustomize build apps/pipeline/upstream/env/cert-manager/platform-agnostic-multi-user | kubectl apply -f -
	sleep 10s
	kustomize build contrib/kserve/kserve | kubectl apply -f -
	sleep 10s
	kustomize build contrib/kserve/models-web-app/overlays/kubeflow | kubectl apply -f -
	sleep 10s
	kustomize build apps/katib/upstream/installs/katib-with-kubeflow | kubectl apply -f -
	sleep 10s
	kustomize build apps/centraldashboard/upstream/overlays/kserve | kubectl apply -f -
	sleep 10s
	kustomize build apps/admission-webhook/upstream/overlays/cert-manager | kubectl apply -f -
	sleep 10s
	kustomize build apps/jupyter/notebook-controller/upstream/overlays/kubeflow | kubectl apply -f -
	sleep 10s
	kustomize build apps/jupyter/jupyter-web-app/upstream/overlays/istio | kubectl apply -f -
	sleep 10s
	kustomize build apps/profiles/upstream/overlays/kubeflow | kubectl apply -f -
	sleep 10s
	kustomize build apps/volumes-web-app/upstream/overlays/istio | kubectl apply -f -
	sleep 10s
	kustomize build apps/tensorboard/tensorboards-web-app/upstream/overlays/istio | kubectl apply -f -
	sleep 10s
	kustomize build apps/training-operator/upstream/overlays/kubeflow | kubectl apply -f -
	sleep 10s
	kustomize build common/user-namespace/base | kubectl apply -f -
	sleep 10s
done