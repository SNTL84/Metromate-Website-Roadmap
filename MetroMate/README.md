# 📍 MetroMate — Location-Based Lead Generation Services

> Smart services pushed to registered members based on their **location profile**.

---

## 🗂️ Overview

**MetroMate** is the location-aware services module of the Tragad Soni platform. When a member registers their profile, MetroMate automatically identifies their city/metro zone and delivers relevant **B2B** and **B2C** lead generation services tailored to their geography.

---

## 📦 Services Included

| Service | Type | Target Audience | Trigger |
|---|---|---|---|
| B2B Lead Generation | B2B | Business Owners, Wholesalers, Distributors | On profile registration with business category |
| B2C Lead Generation | B2C | Consumers, Families, Individuals | On profile registration with location pin |

---

## 🏙️ How It Works

1. **Member registers** on the Tragad Soni platform and fills their profile
2. **Location is captured** — City, Pincode, Metro Zone
3. **MetroMate engine** reads the location tag and matches the member to their metro bucket
4. **Services are pushed** — B2B leads (if business profile) or B2C leads (if consumer profile)
5. **Dashboard updates** with matched leads from the same metro area

---

## 📁 Folder Structure

```
MetroMate/
├── README.md                        ← You are here
├── services/
│   ├── B2B-Lead-Generation.md       ← B2B service spec
│   └── B2C-Lead-Generation.md       ← B2C service spec
└── config/
    └── location-trigger-rules.json  ← Rules for service push by location
```

---

## 🔗 Integration Points

- **Family Registration Form** → captures location at Step 1
- **Member Profile DB** → stores metro zone tag
- **Lead Engine** → queries MetroMate services by zone
- **Notification System** → pushes service alerts to matched members

---

*Module by SNTL84 | Tragad Soni Platform Roadmap*
