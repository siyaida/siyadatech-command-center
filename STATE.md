# STATE.md — Siyadatech Command Center

## Project
- **Name**: Siyadatech Command Center
- **Client**: Ragaban Clinics (Dr. Majed Aljudaibi, CEO)
- **Partner**: Siyadatech (Mohamed Ali Belajouza, Business & Innovation Director)
- **Status**: 🟢 PHASE 0 COMPLETE — Ready for Phase 1
- **Start Date**: May 2026
- **Target Completion**: 16 weeks (4 phases)

## Vision
Transform Ragaban Clinics from a traditional multi-location medical group into a data-driven, AI-assisted healthcare platform — fully compliant with NPHIES, PDPL, and Vision 2030 digital health mandates.

## Architecture (4 Layers)
1. **Infrastructure**: STC Cloud + Docker/K8s + NCA Security
2. **Data**: OpenMRS EHR + PostgreSQL + Kafka + ClickHouse
3. **Application**: FastAPI + SDAIA AI + Unifonic + AI Scheduler
4. **Presentation**: Next.js (RTL) + React Native + Tawk.to + Superset

## Providers Selected (KSA-Native)
| # | Provider | Purpose | Cost | API Key | Setup Time |
|---|----------|---------|------|---------|------------|
| 1 | Unifonic | SMS + WhatsApp | SAR 0.04-0.15/SMS | UNIFONIC_API_KEY | 1-2 days |
| 2 | NPHIES (CHI) | Insurance claims | Free (gov) | NPHIES_CLIENT_ID | 2-4 weeks |
| 3 | Geidea | Payments (mada/V/MC) | 2.5-3.5%/tx | GEIDEA_API_KEY | 3-5 days |
| 4 | STC Cloud | Hosting + residency | SAR 500-2000/mo | STC_CLOUD_CREDENTIALS | 1-2 days |
| 5 | Tawk.to | Live chat | Free | TAWK_PROPERTY_ID | 30 min |
| 6 | OpenMRS | EHR (open source) | Free | None | 2-3 days |
| 7 | Superset | Analytics | Free | None | 1 day |
| 8 | SDAIA AI | AI models | Usage-based | SDAIA_API_KEY | 2-4 weeks |

## Roadmap
- **Phase 1** (Weeks 1-4): Foundation — STC Cloud, OpenMRS, Unifonic WhatsApp, Odoo sync
- **Phase 2** (Weeks 5-8): Intelligence — NPHIES, AI no-show prediction, Superset, Geidea
- **Phase 3** (Weeks 9-12): Experience — Next.js portal, React Native app, AI chatbot, Tawk.to
- **Phase 4** (Weeks 13-16): Scale — SDAIA AI imaging, predictive inventory, marketing automation

## Current Sprint (Sprint #0)
- [x] Read all 4 Ragaban/Siyadatech documents
- [x] KSA healthcare tech ecosystem research
- [x] Provider selection and API mapping
- [x] Architecture blueprint v1.0
- [x] Command Center website build
- [x] Deploy to VPS
- [ ] Collect API keys from Dali
- [ ] Begin Phase 1 execution

## Blockers
1. NPHIES provider registration (need CHI approval)
2. SDAIA AI developer portal access (need to research process)
3. Geidea merchant account (need trade license)
4. STC Cloud account (need business registration)

## Next Actions (Requires Dali Input)
1. **Apply for NPHIES provider registration** at CHI.gov.sa
2. **Sign Unifonic WhatsApp Business API** contract (upgrade from basic SMS)
3. **Create STC Cloud account** with Ragaban business credentials
4. **Apply for Geidea merchant account** with trade license
5. **Confirm budget** for Phase 1-2 (estimate: SAR 50K-80K for infrastructure + dev)

## Links
- Live Site: https://siyadatech.siyada-cybersecurity.com
- GitHub: https://github.com/siyaida/siyadatech-command-center
- Docs: See live site Provider Catalog for all API details

## Notes
- All providers validated against KSA market conditions (May 2026 research)
- NPHIES FHIR R4 APIs: Patient/$summary, Coverage/$eligibility, Claim/$submit
- PDPL compliance required for all patient data handling
- NCA cybersecurity framework applies to all infrastructure
