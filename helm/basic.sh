## Install the tomcat server

helm install tomcat bitnami/tomcat

cat <<EOF > value.yaml
tomcatPassword: fkqxiqDEeT
service:
  type: NodePort
  nodePorts:
    http: 30007
EOF

helm upgrade tomcat --values  value.yaml 

helm delete tomcat


## get the values which we have passed explicitly
helm get values tomcat

# Get all the values
helm get values tomcat --all

# get the history
helm history <release name>

#delete
helm delete <release name>
