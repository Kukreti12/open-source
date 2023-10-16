### Install super set using docker-compose
1. Clone superset repo
    ```
    git clone https://github.com/apache/superset.git
    ```
2. Navigate to the folder
    ```
    cd superset
    ```
3. Run the following commands. If you want to change the port of superset then `vi docker-compose-non-dev.yml pul` and update the port from 8088 to your preferred port.
    ```
    docker-compose -f docker-compose-non-dev.yml pull
    docker-compose -f docker-compose-non-dev.yml up
    ```
4. Navigate to the localhost:8089. As I have updated the port to `8089`
5. Login credentials
    ```
    username :admin
    password: admin
6. [There are several other way to setup superset](https://superset.apache.org/docs/installation/installing-superset-using-docker-compose#installing-superset-locally-using-docker-compose)