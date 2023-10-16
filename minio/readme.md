1. https://min.io/docs/minio/linux/operations/install-deploy-manage/deploy-minio-single-node-single-drive.html#minio-snsd

##credentials
1. S3-API: `http://10.10.162.201:9000`
2. Console `http://10.10.162.201:43681` 
    - username: minioadmin
    - password: minioadmin

### Install using helm chart
1. Install using helm
    ```
    helm repo remove minio
    helm repo add minio https://charts.min.io/
    helm install --namespace minio --set rootUser=rootuser,rootPassword=rootpass123 --generate-name minio/minio
    ```
