# 🚀 Django Docker CI/CD Deployment on AWS EC2

This project demonstrates how to containerize a Django application using Docker and set up a full CI/CD pipeline using **GitHub Actions**, deploying to an AWS EC2 instance.

---

## 🧱 Project Overview

- **Framework**: Django (Python)
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Hosting**: AWS EC2 (Ubuntu)
- **Ports Used**: `8000` (Django), with optional `80`/`443` for production

---

### 📂 Project Structure

```
django-docker-ec2/
├── manage.py                # Django entry point
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker image configuration
├── docker-compose.yml       # Multi-container Docker configuration

├── myproject/               # Main Django project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py

├── core/                    # Django app (example)
│   ├── __init__.py
│   ├── views.py
│   ├── urls.py
│   └── models.py

└── .github/
    └── workflows/
        └── deploy.yml       # GitHub Actions CI/CD pipeline
```

## 🧰 Prerequisites

### 🔒 GitHub Secrets
Set the following secrets in your GitHub repository:

| Name        | Description                         |
|-------------|-------------------------------------|
| `EC2_HOST`  | Public IP of your EC2 instance      |
| `EC2_USER`  | EC2 username (e.g., `ubuntu`)       |
| `EC2_KEY`   | Private SSH key (raw content)       |
| `EC2_PORT`  | 22                                  |

---

## 🛠️ Setup Guide

### 1️⃣ Launch EC2 Instance
- **OS**: Ubuntu 20.04 (or similar)
- **Security Group**: Configure the following inbound rules:

#### 🔐 Inbound Rules (Security Group)
| Port | Protocol | Purpose                     | Source         |
|------|----------|-----------------------------|----------------|
| 22   | TCP      | SSH access                  | Your IP only   |
| 8000 | TCP      | Django dev server           | 0.0.0.0/0      |
| 80   | TCP      | HTTP (optional, production) | 0.0.0.0/0      |
| 443  | TCP      | HTTPS (optional, production)| 0.0.0.0/0      |

> **Note:** Restrict port 22 (SSH) to your IP address only for enhanced security.

**Connect to the instance:**

```bash
ssh -i your-key.pem ubuntu@<EC2-IP>
```

**Install Docker & Docker Compose:**

```bash
sudo apt update
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker $USER
newgrp docker  # or log out and back in
```

---

### 2️⃣ Dockerize Your Django App

**Dockerfile**

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
```

**docker-compose.yml**

```yaml
version: '3'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
```

---

### 3️⃣ GitHub Actions Workflow

Create a workflow file at `.github/workflows/deploy.yml`:

```yaml
name: Deploy to EC2 on Dev Branch Push

on:
  push:
    branches:
      - dev

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up SSH key
      run: |
        mkdir -p ~/.ssh
        echo "${{ secrets.EC2_KEY }}" > ~/.ssh/id_rsa
        chmod 600 ~/.ssh/id_rsa

    - name: Add EC2 host to known hosts
      run: |
        ssh-keyscan -H ${{ secrets.EC2_HOST }} >> ~/.ssh/known_hosts

    - name: SSH and deploy to EC2
      run: |
        ssh -i ~/.ssh/id_rsa -o StrictHostKeyChecking=no ${{ secrets.EC2_USER }}@${{ secrets.EC2_HOST }} << 'EOF'
          cd ~/django-docker-ec2 || git clone https://github.com/harshadakhorgade/django-docker-ec2.git ~/django-docker-ec2 && cd ~/django-docker-ec2
          git pull origin dev
          docker-compose down
          docker-compose build
          docker-compose up -d
        EOF
```

---

### 4️⃣ Test the Pipeline

Make a change and push to the `dev` branch:

```bash
git add .
git commit -m "Trigger CI/CD"
git push origin dev
```

Then, go to GitHub > **Actions** and monitor the deployment. Once successful, visit:  
`http://<your-ec2-ip>:8000`

---

## ✅ Optional Improvements

- **HTTPS**: Use NGINX + Certbot to secure your app with SSL.
- **Custom Domain**: Configure Route 53 or another registrar.
- **Django Commands**: Automatically run database migrations and collectstatic.
- **Notifications**: Integrate Slack or Discord notifications on deploy.

---

## 🌳 Branch Strategy

| Branch | Purpose                     |
|--------|-----------------------------|
| `main` | Production-ready code       |
| `test` | Staging environment         |
| `dev`  | Active development          |

> **Tip:** Protect `main` and `test` branches with branch protection rules.

---

## 🤝 Contributions

Feel free to fork this repository and send pull requests for improvements or fixes.

---

## 📜 License

This project is licensed under the MIT License.
