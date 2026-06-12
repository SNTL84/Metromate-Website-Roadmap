# TRAGAD SONI MVP - QUICK REFERENCE GUIDE

## 🎯 PROJECT OVERVIEW

**Project:** Tragad Soni - B2C/B2B Trade Directory & Workspace Platform  
**Lead:** SNTL 84 (MetroMate) - wa.me/919727413309  
**Timeline:** 21 days to MVP launch  
**Target:** 3000-5000 registered users with workspace profiles

---

## 📊 SYSTEM ARCHITECTURE (One-Page)

```
┌─────────────────────────────────────────────────────┐
│              FRONTEND LAYER                         │
│  Next.js 14 + Tailwind CSS + Vercel Hosting         │
│  Routes: /auth, /directory, /workspace/[id], /ads   │
└──────────────────┬──────────────────────────────────┘
                   │ HTTP/WebSocket
┌──────────────────┴──────────────────────────────────┐
│         SUPABASE BACKEND (All-in-One)               │
│  ┌─────────────────────────────────────────────┐    │
│  │ Auth Layer: OAuth (Google, GitHub)          │    │
│  │ + Row-Level Security (RLS) Policies         │    │
│  └─────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────┐    │
│  │ Database: PostgreSQL                        │    │
│  │ 11 Tables: users, profiles, directory,      │    │
│  │ follows, messages, offers, notifications... │    │
│  │ 24 Indexes for performance                  │    │
│  └─────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────┐    │
│  │ Realtime: Live updates for directory        │    │
│  │ Storage: Profile images (optimized)         │    │
│  │ Functions: Edge functions for triggers      │    │
│  └─────────────────────────────────────────────┘    │
└────────┬───────────────────────────────┬────────────┘
         │                               │
    ┌────▼─────┐        ┌────────────────▼──┐
    │OneSignal │        │ Twilio WhatsApp    │
    │(Push)    │        │ API (Forms)        │
    └──────────┘        └───────────────────┘
```

---

## 🗄️ DATABASE TABLES (11 Core)

| # | Table | Purpose | Key Columns | Scale |
|---|-------|---------|----------|-------|
| 1 | **users** | Authentication | id, email, oauth_provider | 5000 users |
| 2 | **profiles** | User workspaces | user_id, workspace_name, bio, verified | 5000 profiles |
| 3 | **social_handles** | Social links | user_id, platform, handle | 10000 records |
| 4 | **workspaces** | Trade pages | id, user_id, category, status | 5000 workspaces |
| 5 | **directory** | Listings | user_id, reach_score, status | 5000 entries |
| 6 | **follows** | Following | follower_id, following_id, daily_count | 50000 relations |
| 7 | **messages** | Bot chat | user_id, bot_level (1-2), status | 20000 messages |
| 8 | **offers** | Promos | workspace_id, title, active | 5000 offers |
| 9 | **push_notifications** | Notification log | user_id, offer_id, status, sent_at | 20000 logs |
| 10 | **ads** | Ad placement | workspace_id, placement, impressions | 500 ads |
| 11 | **whatsapp_forms** | Form submissions | user_id, form_data (JSON), status | 10000 forms |

---

## 🚀 KEY REPOSITORIES & LINKS

### Priority Order for Implementation

```
DAY 1-3: Foundation
├─ https://supabase.com/docs/guides/auth ..................... OAuth + RLS
├─ https://github.com/supabase/examples-nextjs ............... Full-stack base
└─ Schema + Triggers (provided in detail guide)

DAY 4-7: Core Features
├─ https://github.com/vercel/next.js/examples/tailwind ........ Workspace UI
├─ https://github.com/supabase/realtime/examples/presence .... Live updates
└─ Directory search + pagination

DAY 8-10: Notifications & Bot
├─ https://github.com/supabase-community/onesignal ........... Push notifications
├─ https://github.com/SupaGroup/edge-functions-push ......... Serverless trigger
└─ https://github.com/supabase-community/supabase-rag ........ Bot scaffolding

DAY 11-14: Integrations
├─ https://github.com/shridarpatil/whatomate ................ WhatsApp API
└─ Ad components (custom Tailwind)

DAY 15-18: Optimization
├─ https://github.com/supabase/storage/resizing ............ Image optimization
└─ Caching + query tuning

DAY 19-21: Deploy & Test
└─ Vercel deployment + Supabase monitoring
```

---

## 💾 DATABASE QUERIES REFERENCE

### 1. Register New User (Auto-trigger)
```sql
INSERT INTO users (id, email, name, oauth_provider)
VALUES (auth.uid(), email, name, provider);
-- Trigger automatically creates profile + directory entry
```
**Performance:** < 100ms

### 2. List Directory (Paginated)
```sql
SELECT 
    d.user_id, p.workspace_name, p.bio, 
    COUNT(f.id) AS followers, d.reach_score
FROM directory d
JOIN profiles p ON d.user_id = p.user_id
LEFT JOIN follows f ON d.user_id = f.following_id
WHERE d.status = 'active'
ORDER BY d.reach_score DESC
LIMIT 20 OFFSET 0;
```
**Performance:** 50-150ms (with indexes)

### 3. Send Push Notification
```javascript
// Supabase Edge Function trigger
const response = await fetch('https://onesignal.com/api/v1/notifications', {
    method: 'POST',
    headers: {
        'Authorization': `Basic ${ONESIGNAL_API_KEY}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        app_id: ONESIGNAL_APP_ID,
        include_external_user_ids: [user_email],
        contents: { en: 'New offer in your workspace!' }
    })
});
```
**Performance:** < 300ms

### 4. Track Ad Impression (Batched)
```sql
UPDATE ads 
SET impressions = impressions + 1
WHERE id = $1;
-- Batched every 100 updates to reduce cost
```
**Performance:** 50ms per batch

### 5. Daily Follow Batch Job (Cron)
```sql
-- Run nightly at 2 AM UTC
UPDATE follows 
SET daily_count = daily_count + 1, 
    followed_at = NOW() 
WHERE active = TRUE 
  AND DATE(followed_at) != CURRENT_DATE;
```
**Duration:** ~15 minutes for 50K follows

---

## 📈 COST BREAKDOWN (Monthly at 3000-5000 Users)

| Service | Cost | Why |
|---------|------|-----|
| **Supabase (DB + Storage + Functions)** | $40 | 2GB DB, 3GB storage, 2M function invocations |
| **OneSignal Push** | $0 | Free tier covers 5000 users |
| **Twilio WhatsApp** | $20 | ~1000 messages/month |
| **Vercel Hosting** | $20 | 50GB bandwidth |
| **Redis Caching** (optional) | $10 | Reduces DB load |
| **Monitoring & CDN** | $10 | Logs, analytics, edge cache |
| **TOTAL** | **~$100/month** | Highly scalable |

**Cost Optimization:**
- ✅ Image resizing: -60% storage
- ✅ Query batching: -90% transaction cost
- ✅ RLS policies: Zero extra cost
- ✅ Connection pooling: -20% overhead

---

## 🛠️ TECHNOLOGY STACK

| Layer | Technology | Why | URL |
|-------|-----------|-----|-----|
| **Frontend** | Next.js 14 | Fast, SSR, API routes | nextjs.org |
| **Styling** | Tailwind CSS | Rapid UI development | tailwindcss.com |
| **Hosting** | Vercel | Seamless Next.js deployment | vercel.com |
| **Auth** | Supabase Auth | OAuth ready, RLS built-in | supabase.com |
| **Database** | PostgreSQL | Powerful, cost-effective | postgresql.org |
| **Realtime** | Supabase Realtime | WebSocket subscriptions | supabase.com |
| **Storage** | Supabase Storage | Image optimization, CDN | supabase.com |
| **Push Notifications** | OneSignal | 98%+ delivery rate | onesignal.com |
| **WhatsApp API** | Twilio | Form submissions, messaging | twilio.com |
| **Serverless** | Supabase Functions | Auto-triggers, webhooks | supabase.com |

---

## 📋 21-DAY SPRINT TIMELINE

```
WEEK 1 (Days 1-7)
├─ Mon-Tue: Database setup + OAuth ............................ CRITICAL PATH
├─ Wed: User profiles + directory ............................ CRITICAL PATH
├─ Thu: Directory search + pagination ......................... P1
├─ Fri: Workspace UI + routing ............................... P1
└─ Weekend: Push notification setup ........................... P1

WEEK 2 (Days 8-14)
├─ Mon: Bot Level 1 (FAQ) .................................... P2
├─ Tue: Bot Level 2 (Escalation) ............................. P2
├─ Wed: WhatsApp form integration ............................. P2
├─ Thu: Ads UI components .................................... P2
├─ Fri: Integration testing ................................... P1
└─ Weekend: Load testing (1000 concurrent users) ............. P1

WEEK 3 (Days 15-21)
├─ Mon-Tue: Image optimization + caching ..................... P1
├─ Wed: Query optimization + indexing ......................... P1
├─ Thu: Security audit + RLS verification .................... P0
├─ Fri: Full regression testing ............................... P0
└─ Weekend: Production deployment + monitoring ................ P0
```

---

## ✅ DEPLOYMENT CHECKLIST

### Pre-Launch (Day 19)

- [ ] All 11 database tables created + tested
- [ ] OAuth working (Google, GitHub)
- [ ] Directory listing showing all 5000 users
- [ ] Push notifications delivering 98%+
- [ ] WhatsApp forms capturing submissions
- [ ] Bot responding to messages
- [ ] Ads displaying on workspace pages
- [ ] Images optimized (WebP + resized)
- [ ] Performance: Page load < 2 seconds
- [ ] RLS policies verified (no unauthorized access)

### Day 20 (Security & Scale)

- [ ] SQL injection tests passed
- [ ] XSS protection verified
- [ ] Load test: 1000+ concurrent users
- [ ] Database backups automated
- [ ] Error monitoring configured (Sentry)
- [ ] CDN caching enabled

### Day 21 (Go Live)

- [ ] Production database migrated
- [ ] SSL certificates verified
- [ ] Monitoring dashboards live
- [ ] Incident response plan documented
- [ ] Customer support ready
- [ ] Launch email sent to early users

---

## 📞 PROJECT LEADERSHIP

**Project Lead:** SNTL 84 (MetroMate)
- 📧 Email: desidevloper.com
- 💬 WhatsApp: wa.me/919727413309
- 🔗 LinkedIn: linkedin.com/in/sntl2784
- 🐙 GitHub: github.com/SNTL84
- 📸 Instagram: @desibiztrade
- 🎥 YouTube: @SNTL84

---

## 🎓 LEARNING RESOURCES

### Supabase Masterclass
1. Auth with RLS: https://supabase.com/docs/guides/auth
2. Realtime subscriptions: https://supabase.com/docs/realtime
3. Edge Functions: https://supabase.com/docs/functions

### Next.js Frontend
1. App Router: https://nextjs.org/docs/app
2. API Routes: https://nextjs.org/docs/pages/building-your-application/routing/api-routes
3. Deployment: https://nextjs.org/docs/deployment

### Database Design
1. PostgreSQL EXPLAIN: https://www.postgresql.org/docs/current/sql-explain.html
2. Index strategies: https://use-the-index-luke.com/
3. RLS policies: https://supabase.com/docs/guides/auth/row-level-security

---

## 🚨 COMMON PITFALLS TO AVOID

| Pitfall | Solution |
|---------|----------|
| ❌ Missing RLS policies | ✅ Enable on all tables immediately |
| ❌ N+1 queries in directory | ✅ Use JOIN + aggregate functions |
| ❌ Unoptimized images | ✅ Auto-resize on upload to Storage |
| ❌ Realtime costs exploding | ✅ Only subscribe to active workspaces |
| ❌ Database connection limits | ✅ Enable PgBouncer pooling |
| ❌ No follow-up notifications | ✅ Implement batch reminders (separate table) |
| ❌ Bot training not scalable | ✅ Use similarity search, not hardcoded FAQs |
| ❌ Ads not tracking impressions | ✅ Batch updates every 100 views |

---

## 📞 QUICK SUPPORT LINKS

- **Supabase Status:** https://status.supabase.com
- **Vercel Status:** https://www.vercel-status.com
- **OneSignal Docs:** https://documentation.onesignal.com
- **Twilio Docs:** https://www.twilio.com/docs
- **Next.js Forum:** https://github.com/vercel/next.js/discussions

---

**Version:** 1.0 | **Last Updated:** 2024 | **Next Review:** Post-MVP
