# NA-AI-dremio
![](/deltalake/2022-06-14-12-50-07.png)

## Set up the dremio  using docker
- Using [Docker](https://www.dremio.com/resources/tutorials/python-dremio-and-kubernetes/)
    - Execute the container using docker
        ```
        docker run -p 9047:9047 -p 31010:31010 -p 45678:45678 dremio/dremio-oss
        ```
    - once pull and run is complete. Press `ctr + c` it will exit the terminal.
    - start the docker container
        ```
        docker ps -a
        ```
        ```
        docker start <container id>
        ```
    - Navigate to the
        - http://10.10.160.126:9047
    
- [Install using Kubernetes](https://www.dremio.com/resources/tutorials/python-dremio-and-kubernetes/)
    - Install helm
        ```
        curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get > get_helm.sh
        chmod 700 get_helm.sh
        ./get_helm.sh
        ```
    - Upgrade helm to install Tiller
        ```
        helm init
        helm init --upgrade
        ```
## Login the tibco spotfire
- Login to the jump server
    - 10.10.160.103
    - username: ailab\mlops2
    - password: HP1nvent!
- Tibco login
    - https://account.cloud.tibco.com/manage/home
    - username: saurabh.sharma@hpe.com
    - password: HP1nvent!
- Driver download
    - https://hpe.sharepoint.com/:f:/t/NAPNAI/EkUPo2-R3p1Kki_fcJZ162IB10L32XtQATc4LbwWX8cppQ?e=Ns9VtE
## 