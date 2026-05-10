#!/bin/bash
# STC Cloud deployment script for Ragaban Clinics
# Prerequisites: STC Cloud CLI configured, Docker installed

set -e

PROJECT_ID="${STC_PROJECT_ID:-ragaban-healthcare}"
ZONE="${STC_ZONE:-me-central1-a}"
CLUSTER_NAME="${K8S_CLUSTER:-ragaban-k8s}"

echo "[STC Cloud] Deploying Ragaban Healthcare Platform"
echo "  Project: $PROJECT_ID"
echo "  Zone: $ZONE"

# Create VM instances for each service
echo "[STC Cloud] Creating compute instances..."

for service in api postgres redis kafka clickhouse openmrs superset; do
  INSTANCE_NAME="ragaban-$service"
  
  # Check if instance exists
  if gcloud compute instances describe "$INSTANCE_NAME" --zone="$ZONE" --project="$PROJECT_ID" 2>/dev/null; then
    echo "  $INSTANCE_NAME already exists, skipping..."
  else
    echo "  Creating $INSTANCE_NAME..."
    gcloud compute instances create "$INSTANCE_NAME" \
      --project="$PROJECT_ID" \
      --zone="$ZONE" \
      --machine-type="n1-standard-2" \
      --image-family="debian-12" \
      --image-project="debian-cloud" \
      --boot-disk-size="50GB" \
      --boot-disk-type="pd-ssd" \
      --tags="ragaban,healthcare" \
      --metadata-from-file startup-script=infra/stc-cloud/startup-$service.sh \
      --quiet
  fi
done

# Create firewall rules
echo "[STC Cloud] Configuring firewall..."
gcloud compute firewall-rules create ragaban-healthcare \
  --project="$PROJECT_ID" \
  --allow tcp:80,tcp:443,tcp:8000,tcp:8080,tcp:8088,tcp:3001 \
  --source-ranges="0.0.0.0/0" \
  --target-tags="ragaban" \
  --quiet 2>/dev/null || echo "Firewall rule already exists"

echo "[STC Cloud] Deployment complete!"
echo ""
echo "Next steps:"
echo "  1. SSH into instances: gcloud compute ssh ragaban-api --zone=$ZONE"
echo "  2. Deploy containers: docker compose up -d"
echo "  3. Run migrations: docker exec ragaban-api alembic upgrade head"
echo "  4. Verify health: curl https://ragaban.siyada-cybersecurity.com/health"
