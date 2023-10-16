### ASR using RIVA

1.  [Download the RIVA quick start script](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/riva/resources/riva_quickstart)
    ```
    ngc registry resource download-version "nvidia/riva/riva_quickstart:2.12.1"
    ```
2.  navigate to the downloaded directory
    ```
    cd riva_quickstart_v2.12.0
    ```
3. Initialize and start RIVA
    ```
    bash riva_init.sh
    bash riva_start.sh
    ```

4. [Run through Git hub tutorials](https://github.com/nvidia-riva/tutorials)
    - [Setup instruction](https://github.com/nvidia-riva/tutorials#requirements-and-setup)
        - Install the jupyter notebook and Riva client
    - [Offline transaltion of speech to text](https://github.com/nvidia-riva/tutorials/blob/main/asr-basics.ipynb)
    - Streaming translation
5. [Python-client tutorial](https://github.com/nvidia-riva/python-clients)
### Nemo
1. [Nemo Introduction](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/nemo)
2. Installation
    ```
    docker pull nvcr.io/nvidia/nemo:23.06

    docker run --runtime=nvidia --gpus all --ipc=host -it --rm -v --shm-size=64g -p 8888:8888 -p 6006:6006 --ulimit memlock=-1 --ulimit stack=67108864 nvcr.io/nvidia/nemo:23.06
    ```

3. [ASR models in NeMo](https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/stable/asr/models.html)
4. [ASR notebook](https://github.com/nvidia-riva/tutorials/blob/release/2.11.0/asr-finetune-conformer-ctc-nemo.ipynb)

## Tao

1. [TAO Toolkit](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/tao/resources/tao-getting-started)
    - [Intro video](https://www.nvidia.com/en-us/on-demand/session/other2022-tao/)
    - [TAO Toolkit API helm](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/tao/helm-charts/tao-toolkit-api)
2. [End to End workflow for speech to text training with TAO Toolkit and deployment using Riva.](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/tao/resources/speechtotext_notebook)