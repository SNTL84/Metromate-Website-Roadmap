# TRAGAD SONI MVP - DEPTH REFERENCE & ARCHITECTURE

> **Note:** This file is the Markdown version of `Tragad_Soni_MVP_Depth_Reference.xlsx`  
> **Generated:** June 2026 | **Project Lead:** SNTL 84 (MetroMate)

---

## SECTION 1: REPOSITORY REFERENCE & TECH STACK

| Link | Description | Purpose | Relevance to MVP | Status |
|------|-------------|---------|-----------------|--------|
| https://github.com/SNTL84/Tragad-Soni-Website-Roadmap | Blueprint & Roadmap | Feature requirements spec | Core MVP baseline | Reference |
| https://supabase.com/docs/guides/auth | Supabase Auth + User Profiles | OAuth registration & profiles | User database foundation | Primary |
| https://github.com/supabase-community/onesignal | Supabase + OneSignal | Push notifications | Offer notifications | Secondary |
| https://github.com/supabase/examples-nextjs | Next.js + Supabase | Full-stack boilerplate | Directory & profiles | Primary |
| https://github.com/supabase-community/nextjs-oauth | Next.js OAuth Integration | Google/GitHub auth | OAuth implementation | Primary |
| https://github.com/shridarpatil/whatomate | WhatsApp Business API | 2-way messaging | WhatsApp form submission | Secondary |
| https://github.com/vercel/next.js/examples/tailwind | Next.js + Tailwind | Frontend framework | Trade workspace UI | Primary |
| https://github.com/supabase-community/supabase-rag | Message Bot Scaffolding | AI-powered responses | 2-level bot system | Secondary |
| https://github.com/supabase/storage-resizing | Supabase Storage | Image optimization | Profile images & speed | Tertiary |
| https://github.com/supabase/realtime-presence | Supabase Realtime | Live updates | Real-time directory | Secondary |
| https://github.com/leerob/nextjs-supabase-todo | Next.js CRUD base | Simplified example | MVP iteration speed | Reference |
| https://github.com/SupaGroup/edge-functions-push | Edge Functions | Serverless triggers | Offer push notify | Primary |

---

## SECTION 2: DATABASE DESIGN & SCHEMA

| Table | Description | Key Columns | Purpose |
|-------|-------------|-------------|----------|
| **users** | Core user profiles | id, email, name, oauth_provider, created_at | User authentication & identity |
| **profiles** | Extended user data | user_id, bio, profile_pic_url, workspace_name, verified | Directory space & customization |
| **social_handles** | Social media links | user_id, platform, handle, verified | Connect to social accounts |
| **workspaces** | Trade/business pages | id, user_id, name, description, category, created_at | 3000-5000 registered spaces |
| **directory** | User directory listing | user_id, profile_visibility, status, reach_score | Directory lookup & discovery |
| **follows** | Follow relationships | follower_id, following_id, followed_at, daily_count | Daily follows tracking |
| **messages** | Bot-user interactions | id, user_id, content, bot_level (1-2), response | 2-level message bot system |
| **offers** | Promotional offers | id, workspace_id, title, description, pushed_at | Offer management & push |
| **push_notifications** | Notification logs | id, user_id, offer_id, type, status, sent_at | Track push delivery |
| **ads** | Advertisement display | id, workspace_id, content, placement, impressions | Ads on trade workspace |
| **whatsapp_forms** | WhatsApp submissions | id, user_id, form_data, submission_date, status | WhatsApp form storage |

---

## SECTION 3: DATABASE QUERIES & OPERATIONS

| Operation | Query Type | Frequency | Performance | Impact |
|-----------|-----------|-----------|-------------|--------|
| User Registration | INSERT into users + profiles | Real-time | < 100ms | Critical |
| Directory Search | SELECT from directory + profiles | High (daily) | 50-150ms | High |
| Follow Tracking | INSERT/UPDATE follows (daily) | Daily batch | 15 min/50K | Medium |
| Push Notifications | UPDATE push_notifications + trigger webhook | Per offer | < 300ms | Critical |
| Offer Retrieval | SELECT offers by workspace_id | Hourly | < 100ms | Medium |
| Bot Message Log | INSERT messages + bot_level check | Real-time | 50-100ms | Medium |
| Profile Updates | UPDATE profiles/social_handles | Weekly average | < 200ms | Low |
| Ad Impressions | UPDATE ads impressions count | Real-time (batched) | 50ms/batch | Low |

---

## SECTION 4: ARCHITECTURE VERIFICATION CHECKLIST

| Component | Status | Priority | Stabilization Notes | Optimize Phase |
|-----------|--------|----------|--------------------|-----------------|
| OAuth Registration | Core | P0 | Use Supabase Auth (Day 1-2) | Post-MVP |
| Database Schema | Core | P0 | PostgreSQL with RLS (Day 2-3) | Indexing + Sharding |
| User Profiles | Core | P0 | Profile table + social handles (Day 3) | Search optimization |
| Directory Listing | Core | P1 | 3000-5000 directory + workspace pages (Week 1) | Pagination + Caching |
| Daily Follows | Backend | P1 | Batch job via Supabase cron (Week 1) | Realtime API |
| WhatsApp Forms | Integration | P2 | Twilio/WhatsApp Business API (Week 2) | Full 2-way chat |
| Message Bots (2-level) | Backend | P2 | Conditional routing Level 1 FAQ → Level 2 Escalation (Week 2) | AI embeddings + RAG |
| Push Notifications | Integration | P1 | OneSignal + Edge Functions (Week 1) | Personalization + Timing |
| Ads on Workspace | Frontend | P2 | Tailwind UI component (Week 2) | Ad rotation + analytics |
| Cost Optimization | Ops | P0 | Image resizing, query optimization, caching | CDN + Compression |

---

## SECTION 5: STABILIZATION & DELIVERY TIMELINE

| Phase | Duration | Key Deliverables | Dependencies | Status |
|-------|----------|-----------------|--------------|--------|
| Phase 1: Foundation | Days 1-3 | DB schema + OAuth + user profiles | Supabase project setup | Start |
| Phase 2: Core Features | Days 4-7 | Directory listing + profiles + follows | Schema + OAuth complete | After Phase 1 |
| Phase 3: Notifications & Bot | Days 8-10 | Push notifications + 2-level bot | Database + user mgmt ready | After Phase 2 |
| Phase 4: Integration | Days 11-14 | WhatsApp forms + ads UI | Core features stable | After Phase 3 |
| Phase 5: Optimization | Days 15-18 | Image optimization + caching + queries | All features functional | After Phase 4 |
| Phase 6: Testing & Deploy | Days 19-21 | Full test suite + production deploy | Optimization complete | Final |

---

## SECTION 6: DATABASE USAGE & COST OPTIMIZATION

| Aspect | Strategy | Expected Impact | Implementation Cost | Ongoing Cost Reduction |
|--------|----------|-----------------|---------------------|------------------------|
| Query Optimization | Indexes on user_id, workspace_id, followed_at | -40% query time | Low | -30% per month |
| Image Storage | WebP + Resizing (Supabase Storage) | -60% storage size | Low | -50% bandwidth |
| Caching | Redis on frequently accessed profiles | -80% DB reads | Medium | -40% DB costs |
| Connection Pooling | PgBouncer with Supabase | 1000+ concurrent users | Low | -20% connection overhead |
| Row-Level Security | Native PostgreSQL RLS | No unauthorized access | Low | Zero security cost |
| Realtime Opt | Selective subscriptions (only active workspaces) | -70% realtime overhead | Medium | -50% realtime costs |
| Batch Operations | Nightly job for follows/impressions | -90% transaction cost | Low | -80% daily batch cost |

---

## SECTION 7: PROJECT CREDITS & CONTRIBUTORS

| Role | Name/Handle | Contribution | Contact | GitHub |
|------|-------------|--------------|---------|--------|
| Project Lead & Founder | SNTL 84 (MetroMate/Tragad Soni) | Architecture, strategy, product vision | wa.me/919727413309 | github.com/SNTL84 |
| Tech Lead | TBD - Full-Stack Developer | Next.js + Supabase implementation | To be assigned | To be assigned |
| Database Engineer | TBD - Database Specialist | Schema optimization & queries | To be assigned | To be assigned |
| Frontend Developer | TBD - UI/UX Engineer | Workspace pages + ad placement UI | To be assigned | To be assigned |
| Integration Engineer | TBD - API Integration Lead | WhatsApp + Push notification setup | To be assigned | To be assigned |
| DevOps & Cost Optimization | TBD - Cloud Operations | Supabase config, monitoring, scaling | To be assigned | To be assigned |

---

## SECTION 8: TECH STACK SUMMARY

| Layer | Technology | Purpose | URL/Link | Status |
|-------|-----------|---------|----------|--------|
| Frontend | Next.js 14 + Tailwind CSS | Web app, workspace pages, ad placement | github.com/vercel/next.js | Core |
| Auth | Supabase Auth (OAuth) | Google/GitHub login + user registration | supabase.com/docs/guides/auth | Core |
| Database | PostgreSQL (Supabase) | User data, profiles, follows, messages | supabase.com | Core |
| Realtime | Supabase Realtime | Live directory updates, presence | supabase.com/docs/realtime | Secondary |
| Storage | Supabase Storage | Profile images, optimized delivery | supabase.com/docs/storage | Core |
| Push Notifications | OneSignal + Edge Functions | Offer push notifications | onesignal.com | Core |
| WhatsApp Integration | Twilio WhatsApp Business API | Form submission, messaging | twilio.com | Secondary |
| Message Bot | Supabase Functions + embeddings | 2-level bot (FAQ + escalation) | supabase.com/docs/functions | Secondary |
| Analytics | Supabase Logs + PostgREST | Usage metrics, optimization insights | supabase.com | Tertiary |

---

**Questions?** Contact SNTL 84 → wa.me/919727413309 | github.com/SNTL84