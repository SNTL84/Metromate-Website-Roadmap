# TRAGAD SONI MVP - COMPLETE IMPLEMENTATION GUIDE

**Project:** Tragad Soni - B2C/B2B Trade Directory & Workspace Platform  
**Lead:** SNTL 84 (MetroMate)  
**Timeline:** 21 days to MVP launch  
**Target Users:** 3,000-5,000 registered users with workspace profiles

---

## 📋 TABLE OF CONTENTS

1. [Architecture Overview](#architecture-overview)
2. [Database Design & Schema](#database-design--schema)
3. [Database Creation Steps](#database-creation-steps)
4. [Database Usage Patterns](#database-usage-patterns)
5. [Push Notifications Implementation](#push-notifications-implementation)
6. [Architecture Verification Checklist](#architecture-verification-checklist)
7. [MVP Timeline & Milestones](#mvp-timeline--milestones)
8. [Cost Optimization Strategies](#cost-optimization-strategies)
9. [Repository Reference & Execution Guide](#repository-reference--execution-guide)
10. [Team Credits & Assignments](#team-credits--assignments)

---

## ARCHITECTURE OVERVIEW

### High-Level System Design

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                           │
│  Next.js 14 + Tailwind CSS (Workspace UI, Profile Pages)   │
└────────────────┬────────────────────────────────────────────┘
                 │
┌─────────────────┴──────────────────────────────────────────┐
│              AUTHENTICATION LAYER                           │
│  Supabase Auth (OAuth: Google, GitHub)                     │
│  Row-Level Security (RLS) Policies                         │
└─────────────────┬──────────────────────────────────────────┘
                 │
┌─────────────────┴──────────────────────────────────────────────┐
│           DATABASE & REALTIME LAYER                            │
│  PostgreSQL (Supabase) - Core Data Store                       │
│  Supabase Realtime - Live Updates                             │
│  Supabase Edge Functions - Serverless Logic                   │
└─────────────────┬──────────────────────────────────────────────┘
                 │
        ┌────────┼────────┬────────┬─────────┐
        │        │        │        │         │
    ┌───▼──┐  ┌─▼──┐  ┌──▼──┐  ┌──▼──┐  ┌──▼─────┐
    │Push  │  │Bot │  │WA   │  │Ads  │  │Storage │
    │Notif │  │Msgs│  │API  │  │DB   │  │Optimized│
    └──────┘  └────┘  └─────┘  └─────┘  └────────┘
```

### Core Features Architecture

| Feature | Technology | Database Component | API Layer | Status |
|---------|-----------|-------------------|-----------|--------|
| OAuth Registration | Supabase Auth | users table + RLS | Built-in | ✅ Core |
| User Profiles (3000-5000) | Profiles table | profiles + social_handles | PostgREST | ✅ Core |
| Workspace Pages | Next.js dynamic routes | workspaces table | PostgREST | ✅ Core |
| Directory Listing | Optimized SELECT | directory table + indexes | PostgREST + Realtime | ✅ Core |
| Daily Follows Tracking | Batch jobs + cron | follows table | Cron + Realtime | ✅ P1 |
| 2-Level Message Bot | Supabase Functions | messages table + bot_level | Edge Functions | ✅ P2 |
| Offer Push Notifications | OneSignal + Edge Functions | offers + push_notifications tables | Webhooks | ✅ P1 |
| WhatsApp Form Submission | Twilio WhatsApp API | whatsapp_forms table | Webhooks | ✅ P2 |
| Ads on Workspace | Tailwind components | ads table | PostgREST | ✅ P2 |

---

## DATABASE DESIGN & SCHEMA

### Complete SQL Schema

```sql
-- ============================================
-- 1. CORE USERS & AUTHENTICATION
-- ============================================

CREATE TABLE public.users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    oauth_provider TEXT, -- e.g., 'google', 'github'
    oauth_id TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT valid_email CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')
);

CREATE INDEX idx_users_email ON public.users(email);
CREATE INDEX idx_users_oauth ON public.users(oauth_provider, oauth_id);

-- ============================================
-- 2. USER PROFILES & WORKSPACE DATA
-- ============================================

CREATE TABLE public.profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    bio TEXT,
    profile_pic_url TEXT,
    workspace_name TEXT NOT NULL,
    workspace_description TEXT,
    category TEXT,
    verified BOOLEAN DEFAULT FALSE,
    verified_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id)
);

CREATE INDEX idx_profiles_user_id ON public.profiles(user_id);
CREATE INDEX idx_profiles_category ON public.profiles(category);
CREATE INDEX idx_profiles_verified ON public.profiles(verified);

-- ============================================
-- 3. SOCIAL HANDLES & CONNECTIONS
-- ============================================

CREATE TABLE public.social_handles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    platform TEXT NOT NULL, -- e.g., 'linkedin', 'whatsapp', 'instagram'
    handle TEXT NOT NULL,
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, platform)
);

CREATE INDEX idx_social_handles_user_id ON public.social_handles(user_id);
CREATE INDEX idx_social_handles_platform ON public.social_handles(platform);

-- ============================================
-- 4. WORKSPACES (3000-5000 directory spaces)
-- ============================================

CREATE TABLE public.workspaces (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    category TEXT,
    status TEXT DEFAULT 'active', -- 'active', 'paused', 'closed'
    reach_score INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_workspaces_user_id ON public.workspaces(user_id);
CREATE INDEX idx_workspaces_category ON public.workspaces(category);
CREATE INDEX idx_workspaces_status ON public.workspaces(status);

-- ============================================
-- 5. DIRECTORY LISTING & VISIBILITY
-- ============================================

CREATE TABLE public.directory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    profile_visibility TEXT DEFAULT 'public',
    status TEXT DEFAULT 'active',
    reach_score INT DEFAULT 0,
    last_activity TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id)
);

CREATE INDEX idx_directory_user_id ON public.directory(user_id);
CREATE INDEX idx_directory_status ON public.directory(status);
CREATE INDEX idx_directory_reach_score ON public.directory(reach_score DESC);

-- ============================================
-- 6. FOLLOW RELATIONSHIPS (Daily tracking)
-- ============================================

CREATE TABLE public.follows (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    follower_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    following_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    followed_at TIMESTAMP DEFAULT NOW(),
    daily_count INT DEFAULT 1,
    active BOOLEAN DEFAULT TRUE,
    UNIQUE(follower_id, following_id),
    CHECK (follower_id != following_id)
);

CREATE INDEX idx_follows_follower ON public.follows(follower_id);
CREATE INDEX idx_follows_following ON public.follows(following_id);
CREATE INDEX idx_follows_daily ON public.follows(followed_at DESC);

-- ============================================
-- 7. MESSAGE BOT INTERACTIONS (2-level)
-- ============================================

CREATE TABLE public.messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    bot_level INT DEFAULT 1, -- 1: FAQ/Auto-responses, 2: Escalated/Human review
    response TEXT,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW(),
    resolved_at TIMESTAMP,
    CHECK (bot_level IN (1, 2))
);

CREATE INDEX idx_messages_user_id ON public.messages(user_id);
CREATE INDEX idx_messages_bot_level ON public.messages(bot_level);
CREATE INDEX idx_messages_status ON public.messages(status);

-- ============================================
-- 8. OFFERS & PROMOTIONAL DATA
-- ============================================

CREATE TABLE public.offers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES public.workspaces(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT,
    offer_type TEXT,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_offers_workspace_id ON public.offers(workspace_id);
CREATE INDEX idx_offers_active ON public.offers(active);
CREATE INDEX idx_offers_created_at ON public.offers(created_at DESC);

-- ============================================
-- 9. PUSH NOTIFICATIONS LOG
-- ============================================

CREATE TABLE public.push_notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    offer_id UUID REFERENCES public.offers(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    sent_at TIMESTAMP,
    delivered_at TIMESTAMP,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    onesignal_id TEXT
);

CREATE INDEX idx_push_notif_user_id ON public.push_notifications(user_id);
CREATE INDEX idx_push_notif_offer_id ON public.push_notifications(offer_id);
CREATE INDEX idx_push_notif_status ON public.push_notifications(status);
CREATE INDEX idx_push_notif_sent_at ON public.push_notifications(sent_at DESC);

-- ============================================
-- 10. ADVERTISEMENTS MANAGEMENT
-- ============================================

CREATE TABLE public.ads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES public.workspaces(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    ad_type TEXT,
    placement TEXT,
    active BOOLEAN DEFAULT TRUE,
    impressions INT DEFAULT 0,
    clicks INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_ads_workspace_id ON public.ads(workspace_id);
CREATE INDEX idx_ads_active ON public.ads(active);
CREATE INDEX idx_ads_placement ON public.ads(placement);

-- ============================================
-- 11. WHATSAPP FORM SUBMISSIONS
-- ============================================

CREATE TABLE public.whatsapp_forms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    form_data JSONB NOT NULL,
    phone_number TEXT,
    submission_status TEXT DEFAULT 'received',
    twilio_message_id TEXT,
    submitted_at TIMESTAMP DEFAULT NOW(),
    processed_at TIMESTAMP
);

CREATE INDEX idx_whatsapp_forms_user_id ON public.whatsapp_forms(user_id);
CREATE INDEX idx_whatsapp_forms_status ON public.whatsapp_forms(submission_status);
CREATE INDEX idx_whatsapp_forms_submitted_at ON public.whatsapp_forms(submitted_at DESC);

-- ============================================
-- 12. ROW-LEVEL SECURITY (RLS) POLICIES
-- ============================================

ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.social_handles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.workspaces ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.directory ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.follows ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.offers ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.push_notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ads ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.whatsapp_forms ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read their own profile"
    ON public.users FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Users can update their own profile"
    ON public.users FOR UPDATE
    USING (auth.uid() = id)
    WITH CHECK (auth.uid() = id);

CREATE POLICY "Users can read own profile data"
    ON public.profiles FOR SELECT
    USING (user_id = auth.uid() OR EXISTS (
        SELECT 1 FROM public.directory 
        WHERE user_id = profiles.user_id 
        AND profile_visibility = 'public'
    ));

CREATE POLICY "Users can update own profile data"
    ON public.profiles FOR UPDATE
    USING (user_id = auth.uid())
    WITH CHECK (user_id = auth.uid());

-- ============================================
-- 13. USEFUL VIEWS FOR COMMON QUERIES
-- ============================================

CREATE VIEW public.directory_view AS
SELECT 
    d.id,
    u.id AS user_id,
    u.email,
    p.workspace_name,
    p.bio,
    p.profile_pic_url,
    p.category,
    p.verified,
    d.status,
    d.reach_score,
    COUNT(DISTINCT f.follower_id) AS follower_count,
    d.last_activity
FROM public.directory d
LEFT JOIN public.users u ON d.user_id = u.id
LEFT JOIN public.profiles p ON u.id = p.user_id
LEFT JOIN public.follows f ON d.user_id = f.following_id
WHERE d.status = 'active'
GROUP BY d.id, u.id, p.id;
```

---

## DATABASE CREATION STEPS

### Day 1: Supabase Setup
1. Create Supabase project at https://supabase.com
2. Go to SQL Editor
3. Copy the complete schema above
4. Run in SQL Editor
5. Verify all 11 tables created

### Day 2: OAuth Configuration
1. Enable Google OAuth in Supabase Auth settings
2. Enable GitHub OAuth
3. Configure callback URLs for Vercel deployment
4. Test signup flow

### Day 3: Verify RLS Policies
1. Test that users cannot access other users' data
2. Test public directory visibility
3. Verify trigger functions work

---

## DATABASE USAGE PATTERNS

### Pattern 1: User Registration
```javascript
// Auto-trigger creates profile on signup
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'password'
});
// Trigger: auto-creates users + profiles + directory entry
```
**Performance:** < 100ms

### Pattern 2: Directory Search (Paginated)
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

### Pattern 3: Send Push Notification
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

### Pattern 4: Track Ad Impression (Batched)
```sql
UPDATE ads 
SET impressions = impressions + 1
WHERE id = $1;
-- Batched every 100 updates to reduce cost
```
**Performance:** 50ms per batch

### Pattern 5: Daily Follow Batch Job (Cron)
```sql
-- Run nightly at 2 AM UTC
UPDATE follows 
SET daily_count = daily_count + 1, 
    followed_at = NOW() 
WHERE active = TRUE 
  AND DATE(followed_at) != CURRENT_DATE;
```
**Duration:** ~15 minutes for 50K follows

### Pattern 6: 2-Level Bot Message
```javascript
// Level 1: FAQ match
const { data: faqMatch } = await supabase
  .from('faq')
  .select('answer')
  .textSearch('question', userMessage)
  .limit(1);

if (faqMatch?.length > 0) {
  // Auto-respond with FAQ answer (Level 1)
} else {
  // Escalate to human (Level 2)
  await supabase.from('messages').update({ bot_level: 2 });
}
```

---

## PUSH NOTIFICATIONS IMPLEMENTATION

### Architecture
```
Offer Created → Supabase Trigger 
  ↓ 
Supabase Edge Function 
  ↓ 
OneSignal API 
  ↓ 
User Device (98%+ delivery)
  ↓ 
Push Notification Log (audit trail)
```

### Setup Steps
1. Create OneSignal account at https://onesignal.com
2. Deploy Supabase Edge Function for push trigger
3. Configure webhook: Offer insert → trigger function
4. Test with a sample offer creation

### Key References
- OneSignal Integration: https://github.com/supabase-community/onesignal
- Edge Function Trigger: https://github.com/SupaGroup/supabase-edge-functions-push

---

## ARCHITECTURE VERIFICATION CHECKLIST

### Phase 1 (Days 1-3) - Foundation
- [ ] Supabase project created
- [ ] All 11 tables deployed
- [ ] RLS policies enabled on all tables
- [ ] OAuth (Google, GitHub) working
- [ ] Trigger function auto-creating profiles

### Phase 2 (Days 4-7) - Core Features  
- [ ] Directory listing API returning results
- [ ] Pagination working (20 records/page)
- [ ] Search filtering by category
- [ ] Follow/unfollow working
- [ ] Workspace pages rendering

### Phase 3 (Days 8-10) - Notifications
- [ ] OneSignal account configured
- [ ] Edge Function deployed
- [ ] Push notifications delivering 98%+
- [ ] Bot Level 1 responding to FAQs
- [ ] Bot Level 2 escalation working

### Phase 4 (Days 11-14) - Integrations
- [ ] Twilio WhatsApp webhook configured
- [ ] Form submissions stored in DB
- [ ] Ads displaying on workspace pages
- [ ] Ad impressions being tracked

### Phase 5 (Days 15-18) - Optimization
- [ ] Images converting to WebP on upload
- [ ] Redis caching hot profiles
- [ ] Slow queries optimized (EXPLAIN ANALYZE)
- [ ] Load test: 1000 concurrent users passing

### Phase 6 (Days 19-21) - Deploy
- [ ] Security audit passed (no SQL injection, no XSS)
- [ ] All RLS policies verified
- [ ] Production deployment successful
- [ ] Monitoring dashboards live

---

## MVP TIMELINE & MILESTONES

**PHASE 1: Foundation (Days 1-3)** - CRITICAL PATH
- Day 1: Supabase project + schema deployment
- Day 2: OAuth + RLS policies
- Day 3: Profiles + directory creation

**PHASE 2: Core Features (Days 4-7)** - CRITICAL PATH
- Day 4: Directory listing with pagination
- Day 5: Follow system + daily batch job
- Day 6: Workspace pages (Next.js)
- Day 7: Search optimization

**PHASE 3: Notifications & Bot (Days 8-10)** - P1
- Day 8: OneSignal push integration
- Day 9: 2-level bot Level 1 (FAQ)
- Day 10: Bot Level 2 (escalation)

**PHASE 4: Integrations (Days 11-14)** - P2
- Day 11: WhatsApp form submission
- Day 12: WhatsApp API webhooks
- Day 13: Ads UI components
- Day 14: Ad rotation & tracking

**PHASE 5: Optimization (Days 15-18)** - STABILIZATION
- Day 15: Image optimization + WebP conversion
- Day 16: Redis caching + query tuning
- Day 17: Connection pooling + indexes
- Day 18: Performance testing (1000 concurrent users)

**PHASE 6: Testing & Deploy (Days 19-21)** - FINAL
- Day 19: Full regression + security audit
- Day 20: Load testing + RLS verification
- Day 21: Production deployment + monitoring

---

## COST OPTIMIZATION STRATEGIES

| Strategy | Implementation | Impact | Timeline |
|----------|---|---|---|
| **Image Resizing** | Supabase Storage + Serverless Function | -60% storage size | Week 1 |
| **WebP Format** | Next.js Image Optimization | -40% bandwidth | Week 1 |
| **CDN Caching** | Vercel CDN for static assets | -70% egress cost | Week 2 |
| **Connection Pooling** | PgBouncer (Supabase) | -20% DB connection cost | Setup |
| **Query Optimization** | Indexes + EXPLAIN ANALYZE | -40% query time | Week 1 |
| **Batch Operations** | Nightly cron jobs | -90% transaction cost | Week 1 |
| **Selective Realtime** | Only active subscriptions | -70% realtime overhead | Week 2 |
| **Caching Layer** | Redis for hot data | -80% DB reads | Week 2 |

### Estimated Monthly Costs (MVP at 3000-5000 users)

| Component | Monthly Cost |
|-----------|--------------|
| Supabase Database | $15 |
| Supabase Storage | $5 |
| Supabase Realtime | $10 |
| Supabase Functions | $20 |
| OneSignal Push | $0 (free tier) |
| Vercel Hosting | $20 |
| Twilio WhatsApp | $20 |
| Redis Caching | $10 |
| **TOTAL** | **~$100/month** |

---

## REPOSITORY REFERENCE & EXECUTION GUIDE

### Phase 1: Authentication & Database (Days 1-3)
1. **Supabase Auth Guide** - https://supabase.com/docs/guides/auth/auth-user-management
2. **Next.js + Supabase User Management** - https://github.com/supabase/examples-nextjs-user-management
3. **Next.js OAuth Integration** - https://github.com/supabase-community/nextjs-oauth-user-management

### Phase 2: Directory & Workspace (Days 4-7)
4. **Next.js + Tailwind Frontend** - https://github.com/vercel/next.js/tree/canary/examples/with-tailwindcss
5. **Supabase Realtime Presence** - https://github.com/supabase/supabase/tree/master/examples/realtime/presence

### Phase 3: Push Notifications & Bots (Days 8-10)
6. **OneSignal + Supabase Integration** - https://github.com/supabase-community/onesignal
7. **Supabase Edge Functions + Push** - https://github.com/SupaGroup/supabase-edge-functions-push
8. **Message Bot Scaffolding** - https://github.com/supabase-community/supabase-rag

### Phase 4: Integrations (Days 11-14)
9. **WhatsApp Business API** - https://github.com/shridarpatil/whatomate

### Phase 5: Optimization (Days 15-18)
10. **Image Resizing & Optimization** - https://github.com/supabase/supabase/tree/master/examples/storage/resizing
11. **Simplified CRUD Example** - https://github.com/leerob/nextjs-supabase-todo

---

## TEAM CREDITS & ASSIGNMENTS

| Position | Responsibility | Assigned To | Days | Status |
|----------|---|---|---|---|
| **Project Lead** | Architecture, product vision, strategy | SNTL 84 (MetroMate) | 1-21 | ✅ Active |
| **Tech Lead (Full-Stack)** | Next.js + Supabase architecture, API design | TBD | 1-21 | 🔴 Open |
| **Database Engineer** | Schema optimization, query tuning, RLS policies | TBD | 1-18 | 🔴 Open |
| **Frontend Developer** | Workspace UI, profile pages, ad components | TBD | 4-14 | 🔴 Open |
| **Integration Engineer** | OneSignal, Twilio WhatsApp, Edge Functions | TBD | 7-14 | 🔴 Open |
| **DevOps & Optimization** | Supabase config, monitoring, cost optimization | TBD | 1-18 | 🔴 Open |
| **QA & Testing** | Test plan execution, security audit | TBD | 15-21 | 🔴 Open |

---

**Project Lead Contact:** SNTL 84 → wa.me/919727413309 | github.com/SNTL84