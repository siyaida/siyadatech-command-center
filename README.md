# Siyadatech Command Center

> KSA-native digital transformation engine for Ragaban Clinics — research-built, every provider validated.

## What This Is

A single-page command center that serves as:
- **Presentation Center** — for showing Dr. Majed and Siyadatech stakeholders
- **Vision Statement** — the AI transformation strategy for Ragaban
- **Provider Catalog** — every KSA-native provider with API key requirements
- **Sprint Tracker** — live Kanban for development progress
- **Architecture Blueprint** — 4-layer technical design

## Live URL

🔗 `https://siyadatech.siyada-cybersecurity.com` (deployed to VPS)

## Stack

- Pure HTML/CSS/JS (no build step)
- Dark, premium, engineering-focused aesthetic
- Responsive, Arabic-ready (RTL support prepared)
- MIT License

## Structure

```
├── docs/
│   └── index.html          ← The Command Center (single file, ~45KB)
├── README.md               ← This file
└── STATE.md                ← Live project dashboard
```

## Quick Deploy

```bash
./deploy.sh
```

Or manually:
```bash
scp -i ~/.ssh/vps_key docs/index.html jicwashington@62.171.171.112:/home/jicwashington/projects/siyadatech/
```

## API Keys Needed (from Dali)

See the **Provider Catalog** section in the live site for full details. Summary:

| Provider | Key | Status |
|----------|-----|--------|
| Unifonic | `UNIFONIC_API_KEY` | ✅ Have |
| NPHIES | `NPHIES_CLIENT_ID` | ⏳ Need to apply |
| Geidea | `GEIDEA_API_KEY` | ⏳ Need to apply |
| STC Cloud | `STC_CLOUD_CREDENTIALS` | ⏳ Need to apply |
| Tawk.to | `TAWK_PROPERTY_ID` | ✅ Free, instant |
| SDAIA AI | `SDAIA_API_KEY` | ⏳ Need to research access |

## Status

🟢 **Phase 0 Complete** — Research, architecture, and command center delivered.

Ready for Phase 1 execution pending API key collection.

## License

MIT — Open source, forkable, KSA-native.
