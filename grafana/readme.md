### Setup the Grafana

1. Setup the default storage class using csi operator in k8. 
2. Get the storage class name
    ```
    kubectl get sc
    ```
3. [Create Grafana Kubernetes manifest `grafana.yaml` which will create PVC,deployment and service objects in kubernetes.](https://grafana.com/docs/grafana/latest/setup-grafana/installation/kubernetes/)
4. execute the yaml
    ```
    kubectl apply -f grafana.yaml
    ```
5. Open tmux
    ```
    tmux
    ```
6. Forward the service port to the local host
    ```
    kubectl port-forward service/grafana 3000:3000
    ```
7. Navigate to the `localhost:3000`
8. Login with `admin` as username and password