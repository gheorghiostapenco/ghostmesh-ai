# 👻 GhostMesh AI: Secure Private RAG API on Oracle Cloud

![Status](https://img.shields.io/badge/Status-Live-success)
![Tech](https://img.shields.io/badge/Stack-Terraform%20%7C%20Ansible%20%7C%20Docker%20%7C%20FastAPI-blue)
![Infrastructure](https://img.shields.io/badge/Infra-Oracle%20Cloud%20ARM-orange)

## 📖 Project Overview
GhostMesh AI is a self-hosted, privacy-focused GenAI platform. Unlike commercial APIs (OpenAI/Claude), this system runs entirely on a private cloud instance, ensuring zero data leakage.

It features a **Retrieval-Augmented Generation (RAG)** pipeline, allowing the AI to "learn" from private documents via a Vector Database (ChromaDB) and expose that knowledge via a secure REST API.

## 🏗 Architecture
**Infrastructure:** Oracle Cloud Always Free (Ampere A1 - 4 OCPU, 24GB RAM).
**Security:** SSL/TLS via Let's Encrypt, Nginx Reverse Proxy, IP Whitelisting.

```mermaid
graph LR
    Client[User/Script] -- HTTPS (443) --> Nginx[Nginx Gateway]
    Nginx -- IP Filter --> API[FastAPI Wrapper]
    API -- Query --> Chroma[ChromaDB Vector Store]
    API -- Inference --> Ollama[Ollama (Llama 3.1)]


🛠 Tech Stack
IaC: Terraform (OCI Provider)

Config Management: Ansible (Security Hardening, Docker installation)

Containerization: Docker Compose (Multi-architecture ARM64 builds)

AI Engine: Ollama (Llama 3.1 8B Model)

Backend: Python FastAPI

Database: ChromaDB (Vector Store)

🚀 Deployment Guide
1. Infrastructure Provisioning
Uses Terraform to spin up the Oracle Ampere instance and configure VCN/Firewalls.

cd infrastructure
terraform init
terraform apply

2. Configuration
Uses Ansible to harden the server, install Docker, and set up WireGuard.

cd configuration
ansible-playbook -i inventory site.yml

3. Application Deployment
Deploys the AI Stack (Ollama + API + Nginx).

cd app
docker compose up -d --build


API Usage
The API is secured via HTTPS.

1. Teach the AI (RAG)

curl -X POST [https://ghostmesh-ai.duckdns.org/learn](https://ghostmesh-ai.duckdns.org/learn) \
     -H "Content-Type: application/json" \
     -d '{"text": "GhostMesh was built by George.", "source": "manual"}'

2. Ask the AI

curl -X POST [https://ghostmesh-ai.duckdns.org/ask](https://ghostmesh-ai.duckdns.org/ask) \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Who built GhostMesh?"}'

License
MIT