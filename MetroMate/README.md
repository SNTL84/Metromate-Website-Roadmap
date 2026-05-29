# 🏙️ MetroMate — Trade Generation Platform

> **One Call. All Solutions.** — A full-spectrum B2B & B2C trade generation, lead intelligence, and supplier onboarding platform powered by SNTL 84.

[![Platform](https://img.shields.io/badge/Platform-MetroMate-gold?style=for-the-badge)](https://desidevioper.com)
[![Status](https://img.shields.io/badge/Status-Active%20Development-brightgreen?style=for-the-badge)]()
[![Stack](https://img.shields.io/badge/Stack-HTML%20%7C%20CSS%20%7C%20JS%20%7C%20n8n-blue?style=for-the-badge)]()
[![License](https://img.shields.io/badge/License-Private-red?style=for-the-badge)]()

---

## 🔍 What Is MetroMate?

**MetroMate** is the **trade generation and supplier activation engine** of the Tragad Soni ecosystem. It connects **suppliers, vendors, and service providers** with hyper-local and regional B2B/B2C demand — powered by structured onboarding, smart location matching, and AI-driven lead routing.

MetroMate is built to serve businesses across:
- **Gujarat** (Surat, Ahmedabad, Vadodara, Rajkot)
- **Pan India** coverage
- **International** trade connections

> **For Developers:** This folder contains the supplier-facing onboarding module, service specs, integration configs, and automation blueprints. Every file here is production-relevant — read before you build.

---

## 🚀 Platform Purpose

MetroMate solves three core trade problems:

| Problem | MetroMate Solution |
|---|---|
| Suppliers can't find qualified buyers | Smart B2B lead matching by category + zone |
| Buyers can't find verified local vendors | Curated trade directory with placement services |
| Manual follow-up kills conversion | AI automation workflows (n8n) for lead nurturing |

---

## 🗂️ Module Structure

```
MetroMate/
├── README.md                                   ← You are here — start reading
├── MetroMate_Supplier_Registration_Form.html   ← Live supplier onboarding form (dark UI)
├── services/
│   ├── B2B-Lead-Generation.md                  ← B2B lead service spec & delivery rules
│   └── B2C-Lead-Generation.md                  ← B2C consumer lead pipeline spec
└── config/
    └── location-trigger-rules.json             ← Location → service routing logic
```

---

## 📋 Supplier Registration Form

**File:** `MetroMate_Supplier_Registration_Form.html`

A production-ready, fully responsive **dark-mode HTML form** for onboarding suppliers and service providers into the MetroMate trade network.

### Form Sections & Fields

| Section | Fields Captured | Purpose |
|---|---|---|
| **Business Owner Info** | Full Name, Firm Name, Primary Contact, Phone, Alt Contact, Email | Identity & communication |
| **Business Details** | Address, Google Maps Link, Social Links | Location & digital presence |
| **Category Selection** | Primary Category (dropdown), Other description | Lead routing by trade type |
| **Business Description** | Rich text description | Profile quality, SEO indexing |
| **Service Coverage Area** | Surat / Ahmedabad / Vadodara / Rajkot / Gujarat / Pan India / International | Geographic lead targeting |
| **Lead Generation Intent** | Yes / No radio | Opt-in for lead pipeline activation |
| **Additional Services** | Lead Gen, Digital Marketing, SEO, Meta Ads, AI Automation, Web Dev, Software Dev, Trade Directory, Placement, Fulfillment, Business Consulting | Upsell + service activation |
| **Comments / Notes** | Free-text | Supplier-specific requirements |
| **Declaration** | Checkbox agreement | Legal consent for SNTL 84 partnership |

### Tech Stack — Form

```
Frontend:   HTML5, CSS3 (custom design tokens, dark theme)
Fonts:      Syne (display) + DM Sans (body) via Google Fonts
Theme:      Deep navy (#070b14) + Gold accent (#f5a623) + Blue CTAs (#1a8cff)
UX:         Responsive (mobile-first), animated modal confirmation, character counters
State:      Pure JS — no framework dependency, no localStorage (sandbox-safe)
Images:     Base64-encoded hero banners (no external CDN dependency)
```

### ⚠️ Backend Integration — TODO for Developers

The form currently shows a **client-side success modal** only. The following backend connections are **pending implementation**:

```
[ ] POST handler → Google Sheets (via Apps Script webhook or n8n HTTP node)
[ ] Email notification → Supplier welcome email (SMTP / SendGrid / Resend)
[ ] CRM entry → Airtable / Notion / custom DB
[ ] Lead engine trigger → Auto-enroll in MetroMate lead pipeline
[ ] WhatsApp confirmation → wa.me API or Wati integration
[ ] Admin dashboard alert → Internal Slack/WhatsApp webhook
```

**Recommended integration pattern (n8n):**
```
Form Submit → n8n Webhook → [Google Sheets write] + [Email send] + [WhatsApp notify] + [CRM entry]
```

> **Backend Dev Note:** Look for the `<form>` element and attach your `action` endpoint or use `fetch()` in the existing JS submit handler. The form data is structured with named inputs — all field `id` values match the data schema below.

### Form Field Schema (for API / DB mapping)

```json
{
  "full_name":         "string",
  "firm_name":         "string",
  "primary_contact":   "string",
  "business_phone":    "string (tel)",
  "alt_contact":       "string",
  "email":             "string (email)",
  "biz_address":       "string",
  "map_link":          "string (URL)",
  "social_links":      "string",
  "primary_category":  "string (dropdown)",
  "others_desc":       "string",
  "biz_desc":          "string (textarea, max 600 chars)",
  "coverage_areas":    ["Surat","Ahmedabad","Vadodara","Rajkot","Gujarat","Pan India","International","Other"],
  "wants_leads":       "boolean (yes/no radio)",
  "services_selected": ["Lead Generation","Digital Marketing","SEO","Meta Ads","AI Automation","Website Development","Software Development","Trade Directory Listing","Placement Services","Fulfillment Services","Business Consulting"],
  "comments":          "string (textarea, max 400 chars)",
  "declaration":       "boolean (checkbox)"
}
```

---

## 🏗️ Services Architecture

### B2B Lead Generation
- **Target:** Business owners, wholesalers, distributors, manufacturers
- **Trigger:** On supplier registration with business category + coverage area selected
- **Delivery:** Matched leads pushed via dashboard / WhatsApp / email
- **Spec file:** `services/B2B-Lead-Generation.md`

### B2C Lead Generation
- **Target:** End consumers, families, individual buyers
- **Trigger:** On member registration with location pin
- **Delivery:** Filtered consumer demand routed to relevant suppliers by category
- **Spec file:** `services/B2C-Lead-Generation.md`

### Additional Trade Services

| Service | Description | Dev Integration |
|---|---|---|
| **Digital Marketing** | Social media management, content, growth | External agency API / CRM flag |
| **SEO** | On-page + local SEO for supplier listings | Google Search Console integration |
| **Meta Ads** | Facebook/Instagram paid lead campaigns | Meta Business API |
| **AI Automation** | n8n workflows for follow-up, routing, notifications | n8n webhook endpoint |
| **Website Development** | Supplier microsite or portfolio page | GitHub repo trigger / Vercel deploy |
| **Software Development** | Custom tools, portals, dashboards | Project scoping form |
| **Trade Directory Listing** | Verified business listing in MetroMate directory | DB entry + public profile URL |
| **Placement Services** | Job/vendor placement within the SNTL 84 network | Separate placement pipeline |
| **Fulfillment Services** | Order fulfillment, logistics, last-mile | Logistics API integration |
| **Business Consulting** | Strategy, market entry, growth planning | Calendar booking integration |

---

## 🔁 Location-Based Lead Routing

MetroMate's core intelligence is **geographic lead matching**. The routing config lives in `config/location-trigger-rules.json`.

**How it works:**
```
Supplier registers → Coverage area selected → Lead engine tags supplier zone
→ Incoming buyer requests matched to supplier zone + category
→ Lead delivered via preferred channel (WhatsApp / email / dashboard)
```

**Coverage zones:**

| Zone ID | Market | Lead Volume | Focus Sector |
|---|---|---|---|
| `SURAT` | Primary metro | Highest | Textile, FMCG, Trade |
| `AHMEDABAD` | Secondary metro | High | FMCG, Pharma, Retail |
| `VADODARA` | Industrial zone | Medium | Manufacturing, Engineering |
| `RAJKOT` | SME cluster | Medium | Engineering, Auto parts |
| `GUJARAT` | Statewide | Broad | All categories |
| `PAN_INDIA` | National | Trade directory | Export/Import, B2B |
| `INTERNATIONAL` | Global | Export leads | Specialized trade |

---

## 🔗 Platform Integration Points

```
Tragad Soni Main Platform
        │
        ├── Family Registration Form     → captures member location + profile
        │
        └── MetroMate Module
                │
                ├── Supplier Reg Form    → MetroMate_Supplier_Registration_Form.html
                ├── Location Engine      → config/location-trigger-rules.json
                ├── Lead Matching DB     → Airtable / Google Sheets / custom DB
                ├── n8n Automation       → webhook-based lead delivery & nurturing
                ├── WhatsApp Notify      → wa.me/919727413309
                └── Admin Dashboard      → internal review + approval queue
```

---

## 👩‍💻 Developer Guide

### For Frontend Developers

1. **Form styling** — All CSS lives inside the `<style>` block in the HTML. Design tokens are at `:root`. Modify colors via CSS variables only — never hardcode hex values.
2. **Adding new fields** — Use the `.q-card` + `.q-label` pattern. Required fields get `<span class="req">*</span>`.
3. **Responsive breakpoints** — Form is mobile-first. Main breakpoint at `520px`. Test at `375px` (iPhone SE) and `768px` (tablet).
4. **Validation** — Currently HTML5 `required` + basic JS. Upgrade to real-time inline validation using `--green` (#28c97a) for success and `#ff5c5c` for error states (already in design tokens).
5. **Success modal** — `.modal-overlay` + `.modal-card` — triggers `submitForm()` on button click. Currently shows static content. Connect to actual backend submission response.
6. **Character counters** — `.q-counter` spans exist on textarea fields. Wire up `input` event listeners to update counts dynamically.

### For Backend Developers

1. **Endpoint setup** — Add `action="YOUR_ENDPOINT" method="POST"` to the `<form>` tag, or intercept in the existing JS `submitForm()` function using `fetch()`.
2. **Data format** — All field `name` attributes match the JSON schema keys above. Collect as `FormData` or JSON body.
3. **n8n integration** — Create an n8n **Webhook** node → Parse JSON body → Fan out to:
   - Google Sheets node (write row)
   - Gmail / Resend node (supplier welcome email)
   - HTTP Request node (WhatsApp via Wati/Interakt)
   - Airtable node (CRM entry)
4. **Google Sheets MVP** — Use Apps Script `doPost(e)` as a simple webhook. Sheet columns must match the field schema exactly.
5. **WhatsApp confirmation** — Send a welcome message to `business_phone` via Wati, Interakt, or the official `wa.me` click-to-chat link.
6. **Lead engine trigger** — After saving the supplier record, fire a secondary internal webhook to enroll the supplier in the correct lead bucket (by `primary_category` + `coverage_areas`).

### Environment & Deployment

```
Current hosting:  Static HTML — works on any static host
Recommended:      Vercel / Hostinger / GitHub Pages
Backend:          n8n (self-hosted or n8n.cloud) for automation
Database MVP:     Google Sheets
Database Scale:   Airtable → Supabase → Custom API
Auth:             Not required for public registration form
```

---

## 📊 Metrics & KPIs to Track

| Metric | Target | Tracking Method |
|---|---|---|
| Form completion rate | > 70% | Google Analytics / Hotjar |
| Supplier registrations / month | 50+ (Phase 1) | Google Sheets row count |
| Lead delivery rate | > 90% | n8n execution logs |
| Supplier lead activation rate | > 60% | CRM tag tracking |
| WhatsApp response rate | > 40% | Wati / Interakt dashboard |
| Coverage zone distribution | Balanced across Gujarat | Sheets pivot table |
| Service upsell conversion | > 25% | CRM pipeline stage |

---

## 📌 Repository Topics

> These GitHub topics are set on this repo for discoverability by developers and trade platform contributors:

`trade-generation` · `lead-generation` · `b2b` · `b2c` · `supplier-onboarding` · `metromate` · `sntl84` · `gujarat` · `surat` · `fmcg` · `automation` · `n8n` · `google-sheets` · `html5` · `dark-theme` · `whatsapp-business` · `tragad-soni`

---

## 📅 Roadmap — MetroMate Phase Plan

| Phase | Milestone | Status |
|---|---|---|
| **Phase 1** | Supplier Registration Form (HTML, dark UI) | ✅ Complete |
| **Phase 2** | Backend webhook + Google Sheets integration | 🔄 In Progress |
| **Phase 3** | n8n automation (email + WhatsApp on submit) | 📋 Planned |
| **Phase 4** | Supplier dashboard (view + manage leads) | 📋 Planned |
| **Phase 5** | Location-based lead matching engine | 📋 Planned |
| **Phase 6** | Trade directory (public supplier listing page) | 📋 Planned |
| **Phase 7** | Payment integration (service plan activation) | 📋 Planned |
| **Phase 8** | AI lead scoring + auto-routing | 📋 Planned |

---

## 🧑‍🤝‍🧑 Team & Contacts

| Role | Contact |
|---|---|
| **Project Owner / SNTL 84** | [WhatsApp: +91 97274 13309](https://wa.me/919727413309) |
| **GitHub Repository** | [SNTL84 / Tragad-Soni-Website-Roadmap](https://github.com/SNTL84/Tragad-Soni-Website-Roadmap) |
| **Developer Website** | [desidevioper.com](https://desidevioper.com) |
| **LinkedIn** | [linkedin.com/in/sntl2784](https://www.linkedin.com/in/sntl2784) |
| **Email** | 3goldenlotusroots@gmail.com |
| **Aratt Profile** | [aratt.ai/user/@desidevloper](https://aratt.ai/user/@desidevloper) |

---

*Module maintained by SNTL 84 | Tragad Soni Platform Roadmap | MetroMate Trade Generation Engine*
