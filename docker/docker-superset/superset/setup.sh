echo "Get Superset Pod Name"
export SUPERSET_POD=$(kubectl get pods --namespace=kubeyard | grep superset- | sed 's/ .*//')
echo $SUPERSET_POD

echo "Create Admin User"
kubectl exec $SUPERSET_POD --namespace=kubeyard -it -- fabmanager create-admin --app superset --username=user --firstname=max --lastname=mustermann --email=user@fab.org --password=user

echo "Upgrade Database"
kubectl exec $SUPERSET_POD --namespace=kubeyard -it -- superset db upgrade

echo "Init"
kubectl exec $SUPERSET_POD --namespace=kubeyard -it -- superset init