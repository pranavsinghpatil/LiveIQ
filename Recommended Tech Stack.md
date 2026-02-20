# **Recommended Tech Stack (Optimized for 500 Users)**

## **1\) Frontend (Unified PWA)**

### **Next.js (React \+ TypeScript)**  
**Approach:** Progressive Web App (PWA)
*   **Why:** One codebase for both Web and Android. Fast page loads via SSR/ISR help on weak mobile networks. 
*   **Mobile:** Students "Install to Home Screen" for a full-screen app experience, bypassing Play Store review cycles.
*   **UI Library:** TailwindCSS for clean utilitarian UI and Shadcn/ui for professional forms and tables.

---

## **2\) Backend**

**Node.js \+ NestJS (TypeScript)**

Why NestJS:
* Structured like enterprise Java backend.
* Clear modules → Auth, Test, Scoring, Analytics, Notifications.
* Easy for team collaboration.
* Prevents spaghetti code (very important for long-term maintenance).

---

## **3\) Database**

**PostgreSQL**

Reason:
* Strong relational data (students, attempts, questions).
* Transactions (important for submission locking).
* Ranking queries are easy and performant.
* Reliable for analytics.

ORM: **Prisma ORM**
* Type-safe, fast development, and easy migrations.

---

## **4\) Cache / Performance**

**Redis**  
Used for:
* **Atomic Submissions:** Preventing race conditions when 500 students submit at 11:59 AM.
* **Daily test locking:** Ensuring no submissions after the 12:00 PM cutoff.
* **Ranking cache:** For high-speed leaderboard updates.

---

## **5\) Authentication & Security**

**JWT \+ Device Binding**

Store:
`student_id`, `device_fingerprint`, `session_token`

**Security Rule:** Login allowed only if device matches. This is crucial for preventing account sharing. Admin panel includes a "Reset Device" feature for legitimate changes.

---

## **6\) AI Question Ingester (New Feature)**

**GPT-4o / Vision API**
*   **Why:** To solve the "unprofessional PDF/Image" problem.
*   **Workflow:** Admin uploads the PDF/Image source -> AI extracts text, options, and correct answers -> Admin verifies in a clean UI -> Saved as professional digital MCQ.

---

## **7\) WhatsApp Bot**

**WhatsApp Cloud API (Meta Official API)**

Flow: Backend → webhook → send template message → parent phone.
*   **Strategy:** Use official "Utility" templates to ensure reliability and cost-efficiency.

---

## **8\) Hosting / Infra**

*   **Backend/Frontend:** Railway / Render.
*   **DB:** Managed PostgreSQL (Supabase / RDS).
*   **Redis:** Upstash.
*   **File storage (questions CSV/Images):** S3 / Supabase Storage.

---

# **Architecture Overview**

`Student PWA / Admin Web`  
     `↓`  
`Next.js (App Router)`  
     `↓`  
`NestJS API`  
     `↓`  
`PostgreSQL + Redis`  
     `↓`  
`WhatsApp API`

---

# **Expected Scale This Stack Handles**

### **Without any rewrite:**
* 500 daily users → EASY
* 500 concurrent users → SAFE (Targeted Scale)
* 2,000 users → Still works with vertical scaling

### **Bottleneck threshold:**
At \~10k+ users you would add read replicas, but for the current 500-user scope, this is highly efficient.

---

# **Why this stack is correct for YOUR project**
This stack optimizes **correctness under deadline pressure** (students submitting near 12 PM) while being significantly faster to deploy than a native Android app.
