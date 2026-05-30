#!/bin/bash
# Run this once on a fresh Ubuntu 22.04 EC2 instance
set -e

echo "==> Installing Docker..."
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

echo "==> Installing Docker Compose plugin..."
sudo apt-get install -y docker-compose-plugin

echo "==> Installing Git..."
sudo apt-get install -y git

echo "==> Done. Log out and back in for Docker permissions to apply."
echo "    Then run: git clone <your-repo-url> && cd cleo && cp .env.example .env"
echo "    Fill in .env with your keys, then run: docker compose -f docker-compose.prod.yml up -d --build"
