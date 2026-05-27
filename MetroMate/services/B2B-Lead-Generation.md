# 🏢 B2B Lead Generation Service

**Module:** MetroMate  
**Service Type:** Business-to-Business (B2B)  
**Delivery:** Pushed to members who register with a **business/trade profile**

---

## 🎯 Purpose

Connect registered business members — wholesalers, distributors, retailers, manufacturers, and service providers — with qualified B2B leads from the **same metro zone or nearby cities**.

---

## 👥 Target Members

- Soni community business owners
- Wholesalers & distributors
- Manufacturers & exporters
- Service providers (CA, legal, logistics, IT)
- Franchise seekers / investors

---

## 📌 Trigger Conditions

| Condition | Value |
|---|---|
| Profile Type | `business` or `trade` |
| Location Captured | City + Pincode |
| Business Category | Filled in registration form |
| Verification Status | Basic verified |

---

## 📋 Services Delivered to B2B Members

### 1. 🔍 Local Buyer Matching
- Match registered buyers with sellers from the same city/metro zone
- Filtered by product/service category
- Delivered via dashboard + SMS/WhatsApp alert

### 2. 📊 Trade Lead Alerts
- Weekly curated list of high-intent B2B leads in member's category
- Location-filtered: same district → same state → national fallback
- Format: Name | Business | Contact | Requirement Summary

### 3. 🤝 Supplier-Distributor Connect
- Match manufacturers seeking distributors with interested distributor profiles
- Metro-first matching, expandable to state level

### 4. 📣 Business Directory Listing
- Auto-list the member's business in the Tragad Soni B2B metro directory
- Visible to other registered members in their zone

### 5. 📬 RFQ (Request for Quote) Notifications
- Receive RFQs from buyers that match the member's product/service category
- Real-time push notification on new RFQs

---

## 🔁 Delivery Frequency

| Service | Frequency |
|---|---|
| Buyer Matching | Instant on new match |
| Trade Lead Alerts | Weekly digest |
| Supplier Connect | On new registration match |
| Directory Listing | Permanent (on signup) |
| RFQ Notifications | Real-time |

---

## 📐 Data Fields Required

```json
{
  "member_id": "string",
  "profile_type": "business",
  "business_name": "string",
  "business_category": "string",
  "city": "string",
  "pincode": "string",
  "metro_zone": "string",
  "contact_whatsapp": "string",
  "products_services": ["string"]
}
```

---

*MetroMate B2B Service | SNTL84 | Tragad Soni Platform*
