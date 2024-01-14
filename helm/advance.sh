## Generated name for tomcat
helm install bitnami/tomcat --generate-name
## Dry run: it includes non yaml commands. It validates with k8s
helm install bitnami/tomcat --generate-name --dry-run
## Templates. It differs when compare to the dry run. It doesnt have the release information, just have the yaml commands. Doesnt need k8 serves to generate the templates
helm template bitnami/tomcat
## Get release notes
helm get notes <release name>
## Release records
kubectl get secrets <secret name of helm>
