# 🛍️ B2C Lead Generation Service

**Module:** MetroMate  
**Service Type:** Business-to-Consumer (B2C)  
**Delivery:** Pushed to members who register with a **consumer/family profile**

---

## 🎯 Purpose

Connect registered consumer/family members with **relevant local services, offers, and vendors** from businesses operating in their metro zone. Businesses get qualified consumer leads; members get curated local offers.

---

## 👥 Target Members

- Families registering on the platform
- Individual community members
- Consumers seeking local products/services
- Members looking for Soni-specific vendors (jewellery, catering, events, etc.)

---

## 📌 Trigger Conditions

| Condition | Value |
|---|---|
| Profile Type | `family` or `individual` |
| Location Captured | City + Pincode |
| Interests/Needs | Filled in profile (optional but preferred) |
| Verification Status | Email/WhatsApp verified |

---

## 📋 Services Delivered to B2C Members

### 1. 🏪 Local Vendor Discovery
- Surface nearby registered Soni businesses (jewellers, caterers, garment sellers, etc.)
- Filtered by member's city and category preference
- Delivered on dashboard under "Near You"

### 2. 🎁 Exclusive Community Offers
- Registered businesses can push special offers to metro-matched consumers
- Member receives offer notification via WhatsApp/SMS
- Offer validity window + business contact included

### 3. 💍 Event & Occasion Matching
- Member flags upcoming events (wedding, engagement, pooja)
- MetroMate auto-matches with relevant local vendors
- Pre-qualified vendor list pushed within 24 hours

### 4. 📞 Service Request → Lead Push
- Member posts a service request (catering for 100 guests, mehendi artist, etc.)
- Matched to registered vendors in the same zone
- Vendor receives the lead; member receives quotes

### 5. 🗺️ Metro Zone Community Feed
- Location-filtered community posts, announcements, job postings, and help requests
- Only visible to members in the same metro zone

---

## 🔁 Delivery Frequency

| Service | Frequency |
|---|---|
| Local Vendor Discovery | On login / weekly refresh |
| Exclusive Offers | Real-time push |
| Event Matching | On event date entry |
| Service Request Lead | Within 24 hours of request |
| Community Feed | Daily digest |

---

## 📐 Data Fields Required

```json
{
  "member_id": "string",
  "profile_type": "family",
  "family_head_name": "string",
  "city": "string",
  "pincode": "string",
  "metro_zone": "string",
  "contact_whatsapp": "string",
  "interests": ["jewellery", "catering", "events"],
  "upcoming_events": ["wedding_2026", "engagement"]
}
```

---

*MetroMate B2C Service | SNTL84 | Tragad Soni Platform*
