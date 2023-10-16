
```
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.13.9/config/manifests/metallb-native.yaml
cat <<EOF | tee ./metallb_ip_pool.yaml
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: ailab
  namespace: metallb-system
spec:
  addresses:
  - 10.10.162.122-10.10.162.126
EOF

kubectl apply -f metallb_ip_pool.yaml
echo create metallb_ip_advertisement.yaml
cat <<EOF | tee ./metallb_ip_advertisement.yaml
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: ailab-network
  namespace: metallb-system
spec:
  ipAddressPools:
  - ailab
EOF
nano metallb_ip_advertisement.yaml
kubectl apply -f metallb_ip_advertisement.yaml
```