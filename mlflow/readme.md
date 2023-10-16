### MLFLOW
1. MLflow is a versatile, expandable, open source platform for managing worflows and artifacts across the machine learning lifecycle
    1. Manage all stage of the machine learning workflow
    2. Provide tools and functionality to help ML engineers track experiments and manage and deploy models
2. MLflow components
    1. Tracking
        1. Run- 1 run is 1 model run with set of configuration parameter and its gets track in the tracking server. 
        2. Experiment- Logical grouping of runs. 
    2. Models
    3. Register
    4. Projects
    5. Recipes




1. [Add the repo](https://artifacthub.io/packages/helm/larribas/mlflow)
    ```
    helm repo add larribas https://larribas.me/helm-charts
    ```
2. Install the mlflow
    ```
    helm install my-mlflow larribas/mlflow --version 1.0.1
    ```
3. Navigate to the IP:port to access Mlflow
    ```
    http://10.10.162.136:30087/#/experiments/1
    ```
4. Integrate the mlflow with the postgress db