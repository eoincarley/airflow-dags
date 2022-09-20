# <span style="color:#728FCE;">Airflow on Kubernetes (on WSL).</span>

The minio_dag.py file here implements a number of tasks to make a bucket in Minio and add songs to this bucket.
It then adds song information to the MySQL database (not yet implemented). A number of things need to be set
up first for Airflow to run.

<span style="color:#728FCE;">Helm and Kubernetes (on WSL).</span>

Firstly install Airflow on your machine using the instructions found here. 

```
helm repo add apache-airflow https://airflow.apache.org
helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace

```

You can extract the values.yaml used to update the airflow delpoyments.

```
helm show values apache-airflow/airflow > values.yaml
```
Once updated run

```
helm upgrade --install airflow apache-airflow/airflow -n airflow -f values.yaml --debug
```

Once everything is up and running perform port forwarding

```
kubectl port-forward svc/airflow-webserver 8080:8080 --namespace airflow
```
Then visit localhost:8080 to see the airflow console. The username and password should be admin and admin.

## <span style="color:#728FCE;">Linking your GitHub</span>

In order to sync a github repository such that your custom DAGs appear on the Airflow dashboard you first need to create a GitHub repo and upload your python scripts to it via 'Settings > Deploy Keys'. Then you need to add a public SSH key to this repo, e.g. the key in ~/.ssh/id_rsa.pub. You will need to make a Kubernetes secret with this key in the airflow namespace.

```
kubectl create secret generic my-secret --from-file=ssh-privatekey=/path/to/.ssh/id_rsa --from-file=ssh-publickey=/path/to/.ssh/id_rsa.pub -n airflow
```

Then add the repo and Kubernetes secret information to values.yaml

```
  gitSync:
    enabled: true
    repo: git@github.com:eoincarley/airflow-dags.git
    branch: main
    rev: HEAD
    #root: ""
    #dest: "repo"
    depth: 1
    subPath: ""
    credentialsSecret: git-credentials
    sshKeySecret: my-secret
```

Once saved upgrade your helm again. 
```
kubectl delete statefulset --all -n airflow
```

After a few seconds, and if everything is running correctly, the codes in your github repo should be viewable in your Airflow console on localhost:8080.

## <span style="color:#728FCE;">Customising the airflow image</span>

IF you need to add custom Python packages to the airflow image you will need to create a custom image using a Dockerfile first

```
FROM apache/airflow:2.3.4
RUN pip install --no-cache-dir Minio==7.1.11
```

Build an image from this Dockerfile

```
docker build -t my_image:my_tag .
```

Make sure this image then exists using the 'docker images' command. Then underneath images you need to provide this new image name.

```
# Images
images:
  airflow: 
    repository: my_image
    tag: my_tag
    pullPolicy: IfNotPresent
    
```

Note I needed to delete the statefulsets and deployments and then perform another helm upgrade.

## <span style="color:#728FCE;">Mounted volumes on Kubernetes WSL.</pan>

If persistent storage is required you can employ a mounted volume, or also make a persistentVolume and persistetnVolumeClaim. If using WSL to run Kubernetes there is only one trick. Any mounted volume on the host machine should be in /mnt/wsl/somevolumename/, but the hostPath you provide to kubernetes is /run/desktop/mnt/host/wsl/somevoumename/ (see here for this suggestion: https://microplatforms.de/17154038/use-k8s-hostpath-volumes-in-docker-desktop-on-wsl2#/). Other than this solution, I could not get mounted volumes to work in WSL. In the values.yaml you can implemented mounted volumes as: 

```
workers:
# Mount additional volumes into worker.
  extraVolumeMounts:                                                                                                                                        
    - name: volname
      mountPath: /mnt/somevolume  # location in the container it will put the directory mentioned below.

  extraVolumes: # this will create the volume from the directory
    - name: volname
      hostPath:
        path: /run/desktop/mnt/host/wsl/somevolume  # This is actually /mnt/wsl/somevolume on your local machine.
```

