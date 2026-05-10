# Siyadatech Command Center

> KSA-native digital transformation engine for Ragaban Clinics — research-built, every provider validated.

## What This Is

A full-stack healthcare transformation platform for Jeddah's premier medical group. Built from the ground up for the Saudi market — not translated, born in context.

### Live URLs

- **Command Center**: https://siyadatech.siyada-cybersecurity.com
- **GitHub**: https://github.com/siyaida/siyadatech-command-center

## Architecture (4 Layers)

```
┌─────────────────────────────────────────┐
│  Layer 4: Presentation                  │
│  Next.js (RTL) · React Native · Tawk.to │
├─────────────────────────────────────────┤
│  Layer 3: Application                   │
│  FastAPI · SDAIA AI · Unifonic · AI    │
├─────────────────────────────────────────┤
│  Layer 2: Data                          │
│  OpenMRS · PostgreSQL · Kafka ·         │
├─────────────────────────────────────────┤
│  Layer 1: Infrastructure                │
│  STC Cloud · Docker · K8s · NCA         │
└─────────────────────────────────────────┘
```

## Quick Start

```bash
# 1. Clone
git clone https://github.com/siyaida/siyadatech-command-center.git
cd siyadatech-command-center

# 2. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 3. Build & start
make build
make up

# 4. Run migrations
make migrate

# 5. Verify
make health
```

## Services (Docker Compose)

| Service | Port | Purpose |
|---------|------|---------|
| Caddy | 80/443 | Reverse proxy + SSL |
| API | 8000 | FastAPI backend |
| PostgreSQL | 5432 | Main database |
| Redis | 6379 | Cache + sessions |
| Kafka | 9092 | Event streaming |
| ClickHouse | 8123 | Analytics DB |
| OpenMRS | 8080 | EHR system |
| Superset | 8088 | BI dashboards |
| Uptime Kuma | 3001 | Monitoring |

## API Endpoints

### Patients
- `POST /patients` — Register patient
- `GET /patients/{id}` — Get patient record

### Appointments
- `POST /appointments` — Book appointment + AI risk prediction
- Triggers Unifonic WhatsApp confirmation

### Payments
- `POST /payments` — Create Geidea payment session
- `POST /webhooks/geidea` — Payment callback

### Insurance (NPHIES)
- `GET /insurance/eligibility/{national_id}` — Check coverage
- `POST /insurance/claims` — Submit claim

### Analytics
- `GET /analytics/dashboard` — Clinic metrics
- `GET /analytics/no-show-prediction` — AI predictions

## Provider Catalog

| Provider | Purpose | API Key | Setup Time |
|----------|---------|---------|------------|
| Unifonic | SMS + WhatsApp | `UNIFONIC_API_KEY` | 1-2 days |
| NPHIES (CHI) | Insurance claims | `NPHIES_CLIENT_ID` | 2-4 weeks |
| Geidea | Payments (mada/V/MC) | `GEIDEA_API_KEY` | 3-5 days |
| STC Cloud | Hosting + residency | `STC_CLOUD_CREDENTIALS` | 1-2 days |
| Tawk.to | Live chat | `TAWK_PROPERTY_ID` | 30 min |
| OpenMRS | EHR | None | 2-3 days |
| Superset | Analytics | None | 1 day |
| SDAIA AI | AI models | `SDAIA_API_KEY` | 2-4 weeks |

## Development

```bash
# Backend tests
make test

# Lint code
make lint

# Format code
make format

# Database shell
make db-shell

# Redis CLI
make redis-cli
```

## Roadmap

- **Phase 1** (Weeks 1-4): Foundation — STC Cloud, OpenMRS, Unifonic WhatsApp
- **Phase 2** (Weeks 5-8): Intelligence — NPHIES, AI no-show prediction, Superset
- **Phase 3** (Weeks 9-12): Experience — Next.js portal, React Native app, AI chatbot
- **Phase 4** (Weeks 13-16): Scale — SDAIA AI imaging, predictive inventory

## License

MIT — Open source, forkable, KSA-native.
