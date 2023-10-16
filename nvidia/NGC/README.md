## Setup NVIDIA-NGC on Ubuntu 18.04

### Pre Installation Steps
1. Execute following commands from the [link](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#pre-installation-actions) and validate if we have right hardware

### NGC Installation
1.  Install  [CUDA Driver](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=20.04&target_type=deb_local) driver for Ubuntu
    ```
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
    sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
    wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda-repo-ubuntu2004-11-8-local_11.8.0-520.61.05-1_amd64.deb
    sudo dpkg -i cuda-repo-ubuntu2004-11-8-local_11.8.0-520.61.05-1_amd64.deb
    sudo cp /var/cuda-repo-ubuntu2004-11-8-local/cuda-*-keyring.gpg /usr/share/keyrings/
    sudo apt-get update
    sudo apt-get -y install cuda
    ```

2. Install [docker](https://docs.docker.com/engine/install/ubuntu/#:~:text=from%20the%20repository.-,Set%20up%20the%20repository,-Update%20the%20apt) using repository
    ```
    sudo apt-get update
    sudo apt-get install ca-certificates curl gnupg lsb-release
    ```
    ```
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    ```

3. Install docker [engine](https://docs.docker.com/engine/install/ubuntu/#:~:text=list%20%3E%20/dev/null-,Install%20Docker%20Engine,-Update%20the%20apt)
    ```
    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io
    sudo docker run hello-world
    ```

4. Setting up [Nvidia Docker toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#:~:text=post%2Dinstall%20actions.-,Setting%20up%20NVIDIA%20Container%20Toolkit,%C2%B6,-Setup%20the%20stable)
    ```
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
      && curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | sudo apt-key add - \
      && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
    ```
    ```
    sudo apt-get update
    ```
    ```
    sudo apt-get install -y nvidia-docker2
    ```
    ```
    sudo systemctl restart docker
    ```
    ```
    sudo docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
    ```
    
5. Pull the latest version of Tensor flow from the [documentation](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/tensorflow)

6. Pull the image of tensor flow from the nvidia repo.
    ```
     docker pull nvcr.io/nvidia/tensorflow:22.03-tf1-py3
    ```
7. Run the tensfor flow image 
    ```
     docker run -it --gpus all -p 8888:8888 -v PWD:/projects --network=host nvcr.io/nvidia/tensorflow:22.03-tf1-py3
    ```
8. Install the jupyterlab and open a notebook
    ```
    pip install jupyterlab

    jupyter lab --ip=0.0.0.0 --port=8888 --allow-root
    ```
9. Navigate to the browser and open the jupyterlab link
    ```
    http://project-ngc:8888/lab?token=6fda2f2411afda3529bddcab167fe089fc3bd01f09c4db9c
    ```
    here project-ngc is the hostname
10. Run [Fashion MNIST](https://catalog.ngc.nvidia.com/orgs/nvidia/resources/fashion_mnist_tf_example/version/1.0/files/FashionMNIST%20Notebook.ipynb) in jupyterlab using tensor flow NGC container.
    - Download the notebook to the host machine by below command
        ```
        wget --content-disposition https://api.ngc.nvidia.com/v2/resources/nvidia/fashion_mnist_tf_example/versions/1.0/files/'FashionMNIST Notebook.ipynb'
        ```
    - check the notebook by doing 
        ```
        ls
        ```
    - Copy the notebook from host machine to container where jupyter lab is running.
        copy the path of container where jupyter is running.
            - ![](NGC/2022-03-15-15-17-35.png)
    - Get the container ID from the below command
        ``` 
        docker ps
        ```
        ![](NGC/2022-03-15-15-18-30.png)
    - Run the following command on the duplicate session of host machine as previous session is running jupyter lab. replace the container id with ID which is running the NGC container
        ```
        docker cp FashionMNIST+Notebook.ipynb < container id>:/workspace/Fashion_MNIST.ipynb
        ```
11. Copy the path of the jupyter lab and open in the browser. we can use any VM which is part of AI lab For example RDP into below address which is in same subnet mask.
    ```
    ip address: 10.10.160.138
    username: ailab\mlops2
    password: HP1nvent!
    ```
    http://hostname:8888/?token=4d7d5d4c2ff10f7ce78647c77509264632e352ee4bf54203
    ```
    replace the hostname with
    ```
    hostname
    ```
12. Run the Fashion_MNIST notebook.
    ![](NGC/2022-03-16-11-22-08.png)