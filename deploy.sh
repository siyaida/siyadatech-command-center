#!/bin/bash
# Siyadatech Command Center — One-command deploy
set -e

VPS_USER="jicwashington"
VPS_HOST="62.171.171.112"
VPS_SRV="/home/jicwashington/projects"
SSH_KEY="/root/.openclaw/workspace/.ssh/vps_key"
SSH_OPTS="-i ${SSH_KEY} -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"

echo "[DEPLOY] Siyadatech Command Center → VPS"

# Ensure directory exists
ssh ${SSH_OPTS} ${VPS_USER}@${VPS_HOST} "mkdir -p ${VPS_SRV}/siyadatech"

# Sync files
scp ${SSH_OPTS} -r docs/* ${VPS_USER}@${VPS_HOST}:${VPS_SRV}/siyadatech/

echo "[DEPLOY] Done. Site: https://siyadatech.siyada-cybersecurity.com"
