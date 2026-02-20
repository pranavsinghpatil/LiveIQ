# **Daily Practice Learning Platform — Requirements Specification (v1.0)**

## **1\. Overview**

A web \+ Android (PWA) learning platform for daily subject‑wise practice. Students belong to either **PCM (Physics, Chemistry, Maths)** or **PCB (Physics, Chemistry, Biology)** stream and must solve a daily set of questions before 12:00 PM. The system tracks performance, streaks, analytics, and automatically shares daily performance to parents via WhatsApp bot.

---

## **2\. User Roles**

### **2.1 Student**

* Register and login  
* Attempt daily questions  
* View dashboard analytics  
* Maintain streaks  
* Request device change (through admin)

### **2.2 Parent (Passive Role)**

* Receives WhatsApp performance report daily and weekly summary  
* No login required

### **2.3 Admin**

* Manage students and parents  
* Upload daily/weekly/monthly questions  
* Modify question sets anytime before test unlock time  
* Monitor performance  
* Reset/switch student device  
* Handle disputes & support  
* View platform analytics

---

## **3\. Streams and Subjects**

Each student belongs to ONLY ONE stream.

### **PCM Stream**

| Subject | Questions | Marks per Question | Total Marks |
| ----- | ----- | ----- | ----- |
| Physics | 50 | 1 | 50 |
| Chemistry | 50 | 1 | 50 |
| Maths | 50 | 2 | 100 |
| **Total** | 150 |  | **200 Marks** |

### **PCB Stream**

| Subject | Questions | Marks per Question | Total Marks |
| ----- | ----- | ----- | ----- |
| Physics | 50 | 1 | 50 |
| Chemistry | 50 | 1 | 50 |
| Biology | 50 | 2 | 100 |
| **Total** | 150 |  | **200 Marks** |

---

## **4\. Daily Practice Rules**

1. New question set generated every day  
2. Available from 12:00 PM (Day N) to 11:59 AM (Day N+1)  
3. After 12:00 PM — locked permanently  
4. Missed day breaks streak  
5. Student can attempt only once  
6. All questions mandatory before submission  
7. Submission after 12 PM is rejected even if opened earlier  
8. No negative marking  
9. Correct answers visible after 12 PM next day

---

## **5\. Student Flow**

1. Login  
2. System verifies device  
3. View today’s practice  
4. Solve subject‑wise sections  
5. Submit answers  
6. Instant score calculated  
7. Dashboard updated  
8. WhatsApp report sent to parent immediately

---

## **6\. Dashboard (Student Analytics)**

### **Metrics**

* Today’s Score  
* Subject‑wise score  
* Weekly performance graph  
* Monthly performance graph  
* Accuracy %  
* Attempt rate  
* Global Rank (within stream)  
* Streak days  
* Best streak  
* Improvement trend  
* Weak topics (AI ready feature)

---

## **7\. WhatsApp Parent Report**

Sent automatically after submission \+ weekly summary.

### **Daily Includes**

* Student name  
* Date  
* Score / 200  
* Subject‑wise marks  
* Accuracy %  
* Streak status  
* Remark (Good / Average / Needs Improvement)

### **Weekly Summary Includes**

* Average score  
* Best day  
* Weak subject  
* Improvement trend  
* Attendance consistency

---

## **8\. Device Restriction Policy**

* One active device per student  
* Login on new device blocked  
* Student must request admin to switch device  
* Admin resets device binding  
* New device becomes primary

---

## **9\. Admin Panel Features**

### **Student Management**

* Add/Edit/Delete students  
* Assign PCM or PCB  
* Link parent phone number  
* Reset device  
* Reset streak (special case)

### **Question Management**

* **AI Ingester:** Auto-convert PDF/Images to digital MCQ format.
* Upload question sets daily / weekly / monthly  
* Modify question sets before release time  
* Bulk upload CSV/Excel  
* Subject wise tagging  
* Difficulty tagging  
* Correct answer marking  
* Schedule test release automatically

### **Monitoring**

* Daily attempt rate  
* Active students  
* Global leaderboard  
* Late submission rejection logs  
* Weak subjects report

---

## **10\. Data Model (Conceptual)**

### **Student**

* id  
* name  
* phone  
* stream (PCM/PCB)  
* parent\_phone  
* device\_id  
* streak  
* best\_streak

### **Question**

* id  
* subject  
* stream  
* marks  
* correct\_option  
* date

### **Attempt**

* student\_id  
* date  
* answers  
* score  
* accuracy  
* completed\_time

---

## **11\. Platform Components**

### **Frontend**

* **Unified PWA (Next.js):** Responsive Web + Installable Android experience.

### **Backend**

* **NestJS API:** Modular logic for Auth, Test, Analytics, and Notifications.
* **AI Engine:** Integration with LLM for question ingestion.

### **Integrations**

* WhatsApp Business API  
* Redis (Session & Submission locking)

---

## **12\. Security Requirements**

* JWT authentication  
* Device binding token  
* Encrypted parent phone storage  
* Prevent answer tampering  
* Prevent multiple attempts (Atomic Redis locking)

---

## **13\. Recommended Enhancements (Future)**

* AI weak topic detection  
* Adaptive difficulty questions  
* All India leaderboard  
* Doubt solving chatbot  
* Performance prediction  
* Exam simulation mode

---

## **14\. Non Functional Requirements**

Performance: Support 500 concurrent students  
Reliability: Daily auto backup  
Scalability: Cloud ready architecture  
Usability: \< 3 clicks to start test

---

## **15\. Success Criteria**

* Students solve daily without friction  
* Parents receive report reliably  
* Admin manages without manual tracking  
* Streak system motivates consistency

---

## **16\. Architecture Diagrams (Optimized for 500 Users)**

### **16.1 High Level System Architecture**

[ Student Web / PWA ]  <--- (Single Codebase)
        |  
Internet (HTTPS)
        |  
    [ CDN ]  
        |  
[ Next.js Frontend ]  
        |  
    HTTPS API  
        |  
 [ NestJS Backend ]  
 |      |      |      |  
Auth   Test   AI    Notification  
Module Engine Engine  Service  
 |      |      |      |  
PostgreSQL     |    WhatsApp API  
       |       |  
     Redis Cache

---

### **16.2 Component Diagram**

Backend (NestJS)

- Auth Module  
  • Login  
  • Device Binding  
  • Session Validation

- Test Module  
  • Fetch Daily Questions  
  • Validate Attempt Window  
  • Store Answers  
  • Lock Submission (via Redis)

- AI Ingestion Module
  • PDF/Image Processing
  • Text Extraction (Vision API)
  • Human-in-the-loop Correction UI

- Scoring Engine  
  • Calculate Score  
  • Accuracy  
  • Rank

- Analytics Module  
  • Streaks  
  • Weekly Stats  
  • Monthly Trends

- Notification Module  
  • WhatsApp Daily Report  
  • Weekly Summary

Database Layer  
  PostgreSQL → permanent data  
  Redis → Atomic locks + ranking cache

---

### **16.3 Daily Submission Flow (Sequence Diagram)**

Student → PWA → Backend → Redis/DB → Backend → WhatsApp → Parent

1\. Student opens test  
2\. Backend verifies time window via Redis  
3\. Questions fetched  
4\. Student submits answers  
5\. Backend validates device + atomic check (Redis)  
6\. Score calculated  
7\. Attempt stored in PostgreSQL  
8\. Dashboard updated  
9\. WhatsApp report sent immediately to parent

---

### **16.4 Device Change Flow**

Student → Admin Request → Admin Panel → Backend → DB

1\. Student reports device issue  
2\. Admin resets device binding  
3\. Student logs in new device  
4\. New device becomes primary

---

### **16.5 Deployment Diagram**

Cloud Provider (e.g., Railway/AWS)

[ CDN ]  
   |  
[ Next.js Frontend ]  
   |  
[ NestJS Backend Server ]  
   |        |  
   |        |  
[ PostgreSQL ]   [ Redis ]  
        |  
[ Supabase Storage (PDF/Image Uploads) ]  
        |  
[ WhatsApp Cloud API ]
