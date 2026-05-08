## ✅ Python Installation Guide (Use **Python 3.11 ONLY**)

- **Install Python version: 3.11**
  - Versions **above 3.11** have limited ML library support
  - **Lower versions** may cause compatibility and dependency issues

---

### 🔗 Step 1: Open Official Python Download Page
Go to:
https://www.python.org/downloads/release/python-3127/

---

### 🪟 Step 2: Choose Correct Installer (Windows 64-bit)
- Scroll to the **Version section**
- Under **Windows**, download:
  - **Windows installer (64-bit)** → *Recommended*

---

### ⚙️ Step 3: Install Python
- Run the downloaded installer
- **IMPORTANT:**  
  ✔️ Tick **“Add Python to PATH environment variables”**  
- Continue installation with default settings

---

### 🧪 Step 4: Create Virtual Environment Using Python 3.11
Make sure your virtual environment is created using **Python 3.11**, not any other version.

This ensures:
- Proper ML library support  
- Fewer dependency issues  
- Stable development environment


---

## Dockerfile

You can **copy and paste it directly** into a file named `Dockerfile`.

```dockerfile
FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -e .

EXPOSE 5000

ENV FLASK_APP=application.py

CMD ["python" , "application.py"]
```
---
---
## Kubernetes Deployment Files

You can **copy and paste it directly** into a file named `k8s/deployment.yaml`.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: flask-app
  template:
    metadata:
      labels:
        app: flask-app
    spec:
      containers:
        - name: flask-container
          image: dataguru97/shared-test:latest
          ports:
            - containerPort: 5000

```
**Note** : Make Sure to Change the image path according to your image name and repo on DockerHub.
---

You can **copy and paste it directly** into a file named `k8s/service.yaml`.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-service
spec:
  type: NodePort
  selector:
    app: flask-app
  ports:
    - port: 5000
      targetPort: 5000
      nodePort: 30080

```

---
---

## Jenkins Shared Library Files

You can **copy and paste it directly** into a file named `vars/gitCheckout.groovy`.

```groovy
def call(String repoUrl, String branch, String credId) {
    echo "Checking out code from ${repoUrl}..."
    checkout([
        $class: 'GitSCM',
        branches: [[name: branch]],
        userRemoteConfigs: [[credentialsId: credId, url: repoUrl]]
    ])
}
```
---
You can **copy and paste it directly** into a file named `vars/dockerBuildAndPush.groovy`.

```groovy
def call(String imageName, String registryCredId) {
    echo "Building Docker image ${imageName}..."
    def dockerImage = docker.build("${imageName}:latest")
    
    echo "Pushing Docker image to DockerHub..."
    docker.withRegistry('https://registry.hub.docker.com', registryCredId) {
        dockerImage.push('latest')
    }
}
```
---
You can **copy and paste it directly** into a file named `vars/installKubectl.groovy`.

```groovy
def call() {
    sh '''
    echo 'Installing kubectl...'
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    chmod +x kubectl
    mv kubectl /usr/local/bin/kubectl
    kubectl version --client
    '''
}

```
---
You can **copy and paste it directly** into a file named `vars/k8sDeploy.groovy`.

```groovy
def call(String kubeconfigCredId, String manifestsPath = "k8s") {
    echo "Deploying to Kubernetes..."
    kubeconfig(credentialsId: kubeconfigCredId, serverUrl: "") {
        sh """
        kubectl apply -f ${manifestsPath}/deployment.yaml
        kubectl apply -f ${manifestsPath}/service.yaml
        """
    }
}
```
---
---

## Jenkinsfile Code 

You can **copy and paste it directly** into a file named `vars/gitCheckout.groovy`.

```groovy
@Library('jenkins-shared') _

pipeline {
    agent any
    environment {

    }
    stages {
        stage('Checkout') {
            steps {

            }
        }

        stage('Build & Push Image') {
            steps {
                
            }
        }

        stage('Install Kubectl') {
            steps {
               
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                
            }
        }
    }
}

```
**Note**: The **@Library('jenkins-shared')** name should match the name when you configure them on Jenkins server later on project. Make sure to use the same name..

---
---

## GCP Cloud Setup


### 1. Create a VM Instance on Google Cloud

1. Go to **Compute Engine → VM Instances**
2. Click **Create Instance**

**Basic Configuration**

* **Name:** `Whatever you want to name`
* **Machine Type:**

  * Series: **E2**
  * Preset: **Standard**
  * Memory: **16 GB RAM**
* **Boot Disk:**

  * Size: **150 GB**
  * Image: **Ubuntu 24.04 LTS**
* **Networking:**

  * Enable **HTTP** and **HTTPS** traffic and **Port Forwarding** turned on

Click **Create** to launch the instance.

---

### 2. Connect to the VM

* Use the **SSH** button in the Google Cloud Console to connect to the VM directly from the browser.

---

### 3. Install Docker

1. Open a browser and search for **“Install Docker on Ubuntu”**
2. Open the **official Docker documentation** (`docs.docker.com`)
3. Copy and paste the **first command block** into the VM terminal
4. Copy and paste the **second command block**
5. Test the Docker installation:

```bash
docker run hello-world
```

---

### 4. Run Docker Without `sudo`

From the same Docker documentation page, scroll to **Post-installation steps for Linux** and run **all four commands** one by one.

The last command is used to verify Docker works without `sudo`.

---

### 5. Enable Docker to Start on Boot

From the section **Configure Docker to start on boot**, run:

```bash
sudo systemctl enable docker.service
sudo systemctl enable containerd.service
```

---

### 6. Verify Docker Setup

```bash
systemctl status docker
docker ps
docker ps -a
```

Expected results:

* Docker service shows **active (running)**
* No running containers
* `hello-world` container appears in exited state

---

### 7. Configure Minikube Inside the VM

#### Install Minikube

1. Search for **Install Minikube**
2. Open the official website: `minikube.sigs.k8s.io`
3. Select:

   * **OS:** Linux
   * **Architecture:** x86
   * **Installation Type:** Binary

Copy and run the installation commands provided on the website.

---

#### Start the Minikube Cluster

```bash
minikube start
```

Minikube uses **Docker internally**, which is why Docker was installed first.

---


---

### 8. Verify Kubernetes & Minikube Setup

```bash
minikube status
minikubr kubectl get nodes
minikube kubectl cluster-info
docker ps
```

Expected results:

* All Minikube components are running
* A single `minikube` node is visible
* Kubernetes cluster information is accessible
* Minikube container is running in Docker

---

### 9. Install kubectl

 - Search: `Install kubectl`
  - Instead of installing manually, go to the **Snap section** (below on the same page)

  ```bash
  sudo snap install kubectl --classic
  ```

  - Verify installation:

    ```bash
    kubectl version --client
    ```

### 10. Configure GCP Firewall (If Needed)

If Jenkins does not load, create a firewall rule:

* **Name:** `allow-apps`
* **Description:** Allow all traffic (for Jenkins demo)
* **Logs:** Off
* **Network:** default
* **Direction:** Ingress
* **Action:** Allow
* **Targets:** All instances
* **Source IP ranges:** `0.0.0.0/0`
* **Allowed protocols and ports:** All

---
---

## Jenkins Installation and Setup

### 1. Run Jenkins in Docker (DIND Mode)

#### Check Existing Docker Networks

Ensure Jenkins runs on the **same Docker network as Minikube**.

```bash
docker network ls
```

---

#### Run Jenkins Container

```bash
docker run -d --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(which docker):/usr/bin/docker \
  -u root \
  -e DOCKER_GID=$(getent group docker | cut -d: -f3) \
  --network minikube \
  jenkins/jenkins:lts
```

---

### 2. Verify Jenkins Container

```bash
docker ps
docker logs jenkins
```

* Jenkins container should be running
* Copy the **initial admin password** from the logs

---

### 3. Access Jenkins Web UI

1. Go to your **GCP VM dashboard**
2. Copy the **External IP**
3. Open the following URL in your browser:

```
http://<EXTERNAL_IP>:8080
```
**Note**: Make sure you have the Firewall Rule otherwise you will not be able to acces the Jenkins.
---

###  4. Jenkins Initial Setup

1. Paste the **initial admin password**
2. Click **Install Suggested Plugins**
3. Create an **Admin User**
4. Skip the **agent security warning** (for now)

---

### 5. Install Required Jenkins Plugins

Navigate to:

**Manage Jenkins → Plugins**

Install the following plugins:

* Docker
* Docker Pipeline
* Kubernetes

Restart Jenkins after installation:

```bash
docker restart jenkins
```

Log in again once Jenkins restarts.

---


✅ **Jenkins is now fully set up and ready to use!**

---

# GitHub and DockerHub Configuration with Jenkins Shared Library

## Store the Github Credentials

1. Go to:
   **GitHub → Settings → Developer Settings → Personal access tokens**
2. Click **Generate new token**
3. Select **Classic Token**
4. Grant the following permissions:

* `admin:org`
* `admin:org_hook`
* `admin:public_key`
* `admin:repo_hook`
* `repo`
* `workflow`

#### Add GitHub Credentials to Jenkins

1. Go to:
   **Manage Jenkins → Credentials → Global → Add Credentials**
2. Fill in the details:

   * **Kind:** Username with password
   * **Username:** Your GitHub username
   * **Password:** GitHub Personal Access Token
   * **ID:** `github-token`
   * **Description:** `github-token`
3. Click **Save**

**Note**: Make sure your ID matches with the name on the JenkinsFile for Github Credentials.
---

---

## Store the DockerHub Credntials

1. Go to **[https://hub.docker.com](https://hub.docker.com)**
2. Create a new repository
   Example: `dataguru97/testing`

---

### Generate DockerHub Access Token

1. Go to **DockerHub → Account Settings → Security**
2. Click **New Access Token**
3. Provide:

   * A meaningful **name**
   * **Read/Write** permission
4. Copy and securely store the generated token ( Keep this tab open )

---

### Add DockerHub Credentials to Jenkins

1. Go to **Jenkins → Manage Jenkins → Credentials → Global → Add Credentials**
2. Fill in the details:

   * **Kind:** Username with password
   * **Username:** DockerHub username (e.g., `dataguru97`)
   * **Password:** DockerHub access token
   * **ID:** `dockerhub-token`
   * **Description:** `DockerHub Access Token`
3. Click **Save**

**Note**: Make sure your ID matches with the name on the JenkinsFile for DockerHub Credentials and Repo name.
---
---

## Jenkins Shared Library— Configure Global Pipeline Library

Navigate to:  
**Manage Jenkins → Configure System → Global Pipeline Libraries**

### Verify the Following Settings:

| Field            | Value                         |
|-----------------|--------------------------------|
| **Name**         | `jenkins-shared`               |
| **Default Version** | `main`                     |
| **SCM**          | `Git`                          |
| **Repo URL**     | `your shared lib repo`         |
| **Credentials**  | *(if private repository)*      |

**Note**: Make sure the name is jenkins-shared same as you have given at top of your Jenkinsfile..
---
---

## Create a New Jenkins Pipeline Job

1. Go to **Jenkins Dashboard → New Item**
2. Enter the job name: **`gitops`**  ## Whatver name you want to give
3. Select **Pipeline** and click **OK**
4. Scroll to the **Pipeline** section and configure:

   * **Definition:** Pipeline from SCM
   * **SCM:** Git
   * **Repository URL:** Your GitHub repository URL
   * **Credentials:** Select `github-token`
   * **Branch:** `main`

Save the job configuration.

---

# Kubernetes Configuration with Jenkins Shared Library

### Locate Kubernetes Config File

```bash
cd ~
ls -la
ls -la .kube/
cat .kube/config
```

Copy the entire content of `.kube/config` for backup and editing.

---

### Convert Certificate Files to Base64

Run the following commands one by one:

```bash
cat /home/gyrogodnon/.minikube/ca.crt | base64 -w 0; echo
cat /home/gyrogodnon/.minikube/profiles/minikube/client.crt | base64 -w 0; echo
cat /home/gyrogodnon/.minikube/profiles/minikube/client.key | base64 -w 0; echo
```


Change **gyrogodnon** with your own VM name
Replace:

* `certificate-authority-data`
* `client-certificate-data`
* `client-key-data`

inside your kubeconfig file with these Base64 values.
Do this all on NotePad
After done Copy all content at once..

---

### Save Edited kubeconfig File

- Open GiT Bash 

```bash
cd ~/Downloads
vi config
```

Paste the edited kubeconfig content and save:

```text
Esc → :wq! → Enter
```

---

### Add kubeconfig as Jenkins Secret

1. Go to **Jenkins Dashboard → Manage Jenkins → Credentials**
2. Select **Global → Add Credentials**
3. Configure:

   * **Kind:** Secret file
   * **File:** Upload edited kubeconfig
   * **ID:** `kubeconfig`
   * **Description:** `kubeconfig`
4. Click **Save**

**Note**: Make sure ID of kubeconfig file matches with name in Jenkinsfile last stage.
---

---

# Full CI-CD Deployment using Jenkins and WebHooks

### Trigger the Pipeline on the Jenkins

### Once Completed, go to your VM and write the following command:

```bash
kubectl get pods
```

- **You will see your application running there**
- **You can also check DockerHub for the stored Docker images**
- **It means deployment was succesfull**

### To see your App on the Internet we have to do port-forwarding:
```bash
kubectl port-forward deployment/flask-deployment 5000:5000 --address 0.0.0.0
```
- Go to VM_IP:5000 on intenet and you willsee your app running..

## GitHub Webhooks for Complete Automation


This section enables **fully automated CI/CD** by triggering the Jenkins pipeline **automatically on every GitHub push** using webhooks.

---

### Step 1: Add Webhook in GitHub Repository

1. Go to your **GitHub Repository → Settings → Webhooks**
2. Click **Add webhook**
3. Fill in the details:

* **Payload URL:**

  ```
  http://<JENKINS_PUBLIC_IP>:8080/github-webhook/
  ```

  Replace `<JENKINS_PUBLIC_IP>` with your Jenkins VM public IP.
  * example :http://34.72.5.170:8080/github-webhook/

* **Content type:** `application/json`

* **Secret:** Leave blank

* **SSL verification:** Enable only if Jenkins is using HTTPS

4. Under **Which events would you like to trigger this webhook?**

   * Select **Just the push event**

5. Click **Add webhook**

This ensures the pipeline triggers on **every push to the repository**.

---

### Step 2: Configure Jenkins to Receive Webhook

1. Open **Jenkins Dashboard**
2. Go to your **Pipeline Job**
3. Click **Configure**
4. Scroll to **Build Triggers**
5. Enable:

   * ✅ **GitHub hook trigger for GITScm polling**
6. Click **Apply** and **Save**

Your Jenkins job is now ready to receive webhook events.

---

### Step 3: Test Webhook Automation

1. Open **VS Code**
2. Make a small change in the `Jenkinsfile`
   (for example, add or modify an `echo` statement)
3. Commit and push the changes:

```bash
git add .
git commit -m "Test webhook trigger"
git push origin main
```

4. Go to the **Jenkins Dashboard**

✅ You should see the pipeline **automatically triggered** without clicking **Build Now**.

---

🎉 **Automation Complete!**