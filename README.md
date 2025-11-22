# 🌲 CrystalPine: Private Generative AI Platform

![Status](https://img.shields.io/badge/Status-Production-success)
![Endpoint](https://img.shields.io/badge/API-https%3A%2F%2Fcrystalpine.dev-blue)
![Infrastructure](https://img.shields.io/badge/Oracle_Cloud-ARM_A1-orange)

## 📖 Project Overview
CrystalPine is a production-grade **DevSecOps portfolio project** demonstrating a complete "Code-to-Cloud" AI pipeline. 

It leverages the **Oracle Cloud Always Free** tier (Ampere A1 ARM architecture) to host a self-managed Large Language Model (LLM) capable of **Retrieval-Augmented Generation (RAG)**. The system is fully automated via Terraform and Ansible, and secured behind a rigorous network defense layer.

## 🏗 Architecture
**Live Endpoint:** `https://crystalpine.dev`

```mermaid
graph LR
    User((Client)) -->|HTTPS/443| CF[Cloudflare Proxy]
    CF -->|Strict SSL| OCI[Oracle Cloud Firewall]
    OCI -->|Ingress| Nginx[Nginx Reverse Proxy]
    Nginx -->|Internal Network| API[FastAPI Wrapper]
    API -->|Query| Chroma[ChromaDB Vector Store]
    API -->|Inference| Ollama[Ollama (Llama 3.1)]

## 🏗 Architecture
**Live Endpoint:** `https://crystalpine.dev`
**Infrastructure:** Oracle Cloud Always Free (Ampere A1 - 4 OCPU, 24GB RAM).
**Security:** SSL/TLS via Let's Encrypt, Nginx Reverse Proxy, IP Whitelisting.

<img width="496" height="570" alt="image" src="https://github.com/user-attachments/assets/bce55e48-d84c-45d3-90b0-29830c9404f2" />


## 🛠 Tech Stack
IaC: Terraform (OCI Provider)

Config Management: Ansible (Security Hardening, Docker installation)

Containerization: Docker Compose (Multi-architecture ARM64 builds)

AI Engine: Ollama (Llama 3.1 8B Model)

Backend: Python FastAPI

Database: ChromaDB (Vector Store)


## 🚀 Deployment Guide
1. Infrastructure Provisioning
Uses Terraform to spin up the Oracle Ampere instance and configure VCN/Firewalls.

```Bash

cd infrastructure
terraform init
terraform apply
```
## 2. Configuration
Uses Ansible to harden the server, install Docker, and set up WireGuard.

```Bash

cd configuration
ansible-playbook -i inventory site.yml
```
## 3. Application Deployment
Deploys the AI Stack (Ollama + API + Nginx).

```Bash

cd app
docker compose up -d --build
```
## 🔌 API Usage
The API is secured via HTTPS.

1. Teach the AI (RAG)

```Bash

curl -X POST [https://crystalpine.dev/learn](https://crystalpine.dev/learn) \
     -H "Content-Type: application/json" \
     -d '{"text": "CrystalPine runs on Oracle ARM.", "source": "system_docs"}'
```
2. Ask the AI

```Bash

curl -X POST [https://crystalpine.dev/ask](https://crystalpine.dev/ask) \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Explain the benefits of IaC."}'
```

## ⚖️ License
MIT
