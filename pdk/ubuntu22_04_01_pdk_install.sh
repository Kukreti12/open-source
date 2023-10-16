#! /usr/bin/bash
## Do not run as script## Need to manually edit the script.##

echo ..one step at a time installer for pdk stack on Ubuntu 22.04.1LTS
echo install order is
echo       docker
echo       cri-docker
echo       kubernetes
echo       metallb
echo       helm
echo       pachyderm
echo       determined
echo .
echo install is to local disk
echo VM needed is >8 cores, 32GB RAM and 300 GiB disk
echo you must be loggedin is regular user with sudo privileges
echo this help shell script was created with user 'hpadmin'

echo ------ part I ------ os configs ------
cd ~
pwd
lsmod | grep br_netfilter 
sudo modprobe br_netfilter
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF
sudo modprobe overlay
sudo modprobe br_netfilter
# sysctl params required by setup, params persist across reboots
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF
# Apply sysctl params without reboot
sudo sysctl --system

echo ------ docker ------
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker hpadmin
sudo service docker start
sudo docker run hello-world

echo ------ take vm snap shot --- after docker ------

echo ------ cri-docker ---------
git clone https://github.com/Mirantis/cri-dockerd.git
wget https://storage.googleapis.com/golang/getgo/installer_linux
chmod +x ./installer_linux
./installer_linux
source ~/.bash_profile
cd cri-dockerd
mkdir bin
go build -o bin/cri-dockerd
sudo mkdir -p /usr/local/bin
sudo install -o root -g root -m 0755 bin/cri-dockerd /usr/local/bin/cri-dockerd
sudo cp -a packaging/systemd/* /etc/systemd/system
sudo sed -i -e 's,/usr/bin/cri-dockerd,/usr/local/bin/cri-dockerd,' /etc/systemd/system/cri-docker.service
sudo systemctl daemon-reload
sudo systemctl enable cri-docker.service
sudo systemctl enable --now cri-docker.socket
sudo swapoff -a 
sudo nano /etc/fstab


echo ------- take vm snap shot ----- after cri-docker ------

echo ----- installing k8s -----
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
sudo apt-get install -y kubelet=1.22.0-00 kubeadm=1.22.0-00 kubectl=1.22.0-00
sudo apt-mark hold kubelet kubeadm kubectl
sudo kubeadm init --upload-certs
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
echo note down node name and edit commands below
kubectl get nodes
kubectl describe node pradeep1
echo copy node-role Taints here: node-role.kubernetes.io/master:NoSchedule & modify untaint command to match up
echo look for taint starting with node-role, it has shown up differently in different installs
kubectl taint node pradeep1 node-role.kubernetes.io/master:NoSchedule-
echo copy and fix the above command and run in a separate terminal session
kubectl apply -f https://github.com/weaveworks/weave/releases/download/v2.8.1/weave-daemonset-k8s.yaml
kubectl get ns


echo ------- take vm snap shot ----- after k8s ------



echo ---------- metallb install ----------
cd ~
mkdir yamls
cd yamls
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.13.9/config/manifests/metallb-native.yaml
echo create metallb_ip_pool.yaml ; fix IP range
cat <<EOF | tee ./metallb_ip_pool.yaml
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: hug-local
  namespace: metallb-system
spec:
  addresses:
  - 10.10.162.246-10.10.162.249
EOF
nano metallb_ip_pool.yaml
kubectl apply -f metallb_ip_pool.yaml
echo create metallb_ip_advertisement.yaml
cat <<EOF | tee ./metallb_ip_advertisement.yaml
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: hug-network
  namespace: metallb-system
spec:
  ipAddressPools:
  - hug-local
EOF
nano metallb_ip_advertisement.yaml
kubectl apply -f metallb_ip_advertisement.yaml



echo ---- take VM snapshot after metallb -----



echo -------- helm install ----
cd ~
curl https://get.helm.sh/helm-v3.9.2-linux-amd64.tar.gz  --output helm-v3.9.2-linux-amd64.tar.gz 
tar -zxvf helm-v3.9.2-linux-amd64.tar.gz 
sudo mv linux-amd64/helm /usr/local/bin/helm
helm help

echo ------ take VM snapshot after helm ----



echo ------ part II ------ Pachyderm ------
cd ~/yamls
echo create my_pachyderm_values.yaml
mkdir /home/hpadmin/pachyderm
cat <<EOF | tee ./my_pachyderm_values.yaml
# SPDX-FileCopyrightText: Pachyderm, Inc. <info@pachyderm.com>
# SPDX-License-Identifier: Apache-2.0

deployTarget: CUSTOM

pachd:
  storage:
    backend: LOCAL
    local:
      # hostPath indicates the path on the host where the PFS metadata
      # will be stored.  It must end in /.  It is analogous to the
      # --host-path argument to pachctl deploy.
      hostPath: "/home/hpadmin/pachyderm"
      requireRoot: true
  externalService:
    enabled: true

console:
  service:
    type: LoadBalancer

etcd:
  storageClass: manual
  size: 10Gi

postgresql:
  persistence:
    storageClass: manual
    size: 10Gi
EOF
nano my_pachyderm_values.yaml
echo we will use this file later
echo create sc.yaml - 'manual' storageclass
cat <<EOF | tee ./sc.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: manual
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
EOF
nano sc.yaml
kubectl apply -f sc.yaml
kubectl patch storageclass manual -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
echo create pv.yaml - need 3 x 10GiB PV for pachyderm
echo fix the path as needed
cat <<EOF | tee ./pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: task-1
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/home/hpadmin/pachyderm"
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: task-2
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/home/hpadmin/pachyderm"
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: task-3
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/home/hpadmin/pachyderm"
EOF
nano pv.yaml
kubectl apply -f pv.yaml
echo helm client tool
cd ~
curl -o /tmp/pachctl.deb -L https://github.com/pachyderm/pachyderm/releases/download/v2.4.2/pachctl_2.4.2_amd64.deb && sudo dpkg -i /tmp/pachctl.deb  
pachctl version --client-only 
helm repo add pach https://helm.pachyderm.com
helm repo update
echo edit to check my_pachyderm_values.yaml
cd ~/yamls
nano my_pachyderm_values
helm install pachd -f my_pachyderm_values.yaml pach/pachyderm
echo wait till pachyderm containers ready
kubectl get pv
kubectl get pvc
kubectl get pods -A
echo verify metallb and pachyderm svcs
kubectl get svc
echo note down IP & portno to pacyderm lb svc in the next line
echo also notedown metallb console IP & portno
kubectl get services | grep pachd-lb | awk '{print $4}'
kubectl get services | grep pachd-lb 
echo '{"pachd_address":"grpc://10.10.162.247:30650"}' | pachctl config set context pachd --overwrite && pachctl config set active-context pachd
pachctl version
echo go to metallb console via browser to ip & portno

echo ------- take vm snapshot after pachyderm ----


echo ----- kserve ------
cd ~
curl -s "https://raw.githubusercontent.com/kserve/kserve/release-0.10/hack/quick_install.sh" | bash
echo check & make sure good with svcs & podcs - knative & istio added this step
kubectl get ns
kubectl get pods -A


echo ------ install determined -------
mkdir ~/determined
echo create pv-determined.yaml for 30GiB pv
cd ~/yamls
cat <<EOF | tee ./pv-determined.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: task-d
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 30Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/home/hpadmin/pachyderm"
EOF
nano pv-determined.yaml
cat pv-determined.yaml
kubectl apply -f pv-determined.yaml
kubectl get pv
cd ~
curl https://docs.determined.ai/latest/_downloads/389266101877e29ab82805a88a6fc4a6/determined-latest.tgz --output determined-latest.tgz
tar -xvzf determined-latest.tgz
cd ~/determined
echo change maxslots=1 and host sharedfs path
nano values.yaml
less values.yaml
echo test via IP:port user determined no pswd
echo launch a notebook from gui
kubectl create ns determined
kubectl get ns
helm install determined ./ -n determined
kubectl get pods -n determined
kubectl get svc
kubectl get svc -n determined

echo ----- install miniconda for client tools ----
cd ~
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
bash
pip install determined
echo check & get info on our det svc
helm status determined -n determined
kubectl get svc -n determined
export DET_MASTER=10.10.162.249:8080
det experiment list
