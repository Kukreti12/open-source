### Postgres using docker
1. [Setup Postgres using docker + Pgadmin4](https://medium.com/@basit26374/how-to-run-postgresql-in-docker-container-with-volume-bound-c141f94e4c5a)
    1. Create a datafabric volume from MSC and add the path to the docker mount location. For example
    `mnt/mapr_nfs/df5node/data/postgres` is the mount location
    ```
    docker run  --restart always --name postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -v /mnt/mapr_nfs/df5node/data/postgres:/var/lib/postgresql/data -d postgres
    ```
    2. Setup pgadmin4
    ```
    #
    # Setup the repository
    #

    # Install the public key for the repository (if not done previously):
    curl -fsS https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo gpg --dearmor -o /usr/share/keyrings/packages-pgadmin-org.gpg

    # Create the repository configuration file:
    sudo sh -c 'echo "deb [signed-by=/usr/share/keyrings/packages-pgadmin-org.gpg] https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$(lsb_release -cs) pgadmin4 main" > /etc/apt/sources.list.d/pgadmin4.list && apt update'

    #
    # Install pgAdmin
    #

    # Install for both desktop and web modes:
    sudo apt install pgadmin4

    # Install for desktop mode only:
    sudo apt install pgadmin4-desktop

    # Install for web mode only: 
    sudo apt install pgadmin4-web 

    # Configure the webserver, if you installed pgadmin4-web:
    sudo /usr/pgadmin4/bin/setup-web.sh
    ```
    3. Add the server details in PGadmin4
        - host- 10.10.162.136
        - username- postgres
        - password- mysecretpassword
        - database- postgres

### Potgres using Helm

1. Helm chart  installation 
https://adamtheautomator.com/postgres-to-kubernetes/
1. Add the bitnami repo
    ```
    helm repo add bitnami https://charts.bitnami.com/bitnami
    ```
2. Update your local repo
    ```
    helm repo update
    ```
3. Please make sure you have CSI storage class created
    - Create PVC
        ```
        kubectl create -f postgres-pvc.yaml
        ```
4. Create value.yaml where we provide the db credentials and the pvc name

5. Install postgress using helm
    ```
    helm install postgresql-dev -f values.yaml bitnami/postgresql
    ```
6. Below is the screen we see after successful installation.
    ```
    ** Please be patient while the chart is being deployed **

PostgreSQL can be accessed via port 5432 on the following DNS names from within your cluster:

    postgresql-dev.default.svc.cluster.local - Read/Write connection

To get the password for "postgres" run:

    export POSTGRES_ADMIN_PASSWORD=$(kubectl get secret --namespace default postgresql-dev -o jsonpath="{.data.postgres-password}" | base64 -d)

To get the password for "app1" run:

    export POSTGRES_PASSWORD=$(kubectl get secret --namespace default postgresql-dev -o jsonpath="{.data.password}" | base64 -d)

To connect to your database run the following command:

    kubectl run postgresql-dev-client --rm --tty -i --restart='Never' --namespace default --image docker.io/bitnami/postgresql:15.1.0-debian-11-r31 --env="PGPASSWORD=$POSTGRES_PASSWORD" \
      --command -- psql --host postgresql-dev -U app1 -d app_db -p 5432

    > NOTE: If you access the container using bash, make sure that you execute "/opt/bitnami/scripts/postgresql/entrypoint.sh /bin/bash" in order to avoid the error "psql: local user with ID 1001} does not exist"

To connect to your database from outside the cluster execute the following commands:

    kubectl port-forward --namespace default svc/postgresql-dev 5432:5432 &
    PGPASSWORD="$POSTGRES_PASSWORD" psql --host 127.0.0.1 -U app1 -d app_db -p 5432
    ```

6.  Create table and insert values. Execute the container as postgres client
    - Create DDL
        ```
        CREATE TABLE links (
            id SERIAL PRIMARY KEY,
            url VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            description VARCHAR (255),
                last_update DATE
        );
        ````
    - Insert Values
        ```
        INSERT INTO links (url, name)
        VALUES('https://www.postgresqltutorial.com','PostgreSQL Tutorial');
        ```
    - Get the result
        ```
        SELECT	* FROM links;
        ```
7. Problem which I am facing is to expose the postgres service outside the cluster. 