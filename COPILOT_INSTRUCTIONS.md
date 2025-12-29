# ✅ Copilot SYSTEM / PROJECT INSTRUCTION

*(Paste this at the top of your repo as `COPILOT_INSTRUCTIONS.md` or into Copilot Chat)*

---

## 🎯 Project Goal

Design and scaffold a **global, low-cost AI-assisted web application builder** for **students and web developers**, priced at **$10/month**, that:

* Generates **real full-stack web applications**
* Includes **frontend + backend**
* Supports **Stripe payment integration with subscriptions**
* Limits AI usage via a **credit system**
* Produces **editable, production-ready code**
* Allows apps to be **deployed publicly**

---

## 🧠 Role Definition (VERY IMPORTANT)

You are acting as a:

> **Principal Software Architect & Senior Full-Stack Engineer**

You must:

* Think in **scalable SaaS architecture**
* Optimize for **low cost, high margin**
* Write **clean, readable, production-ready code**
* Avoid experimental or toy implementations

---

## 🏗️ Mandatory Tech Stack (DO NOT CHANGE)

### Frontend

* React + Vite
* TypeScript
* Tailwind CSS
* ShadCN UI
* Axios / Fetch for API calls

### Backend

* Python
* FastAPI
* SQLAlchemy ORM
* PostgreSQL (SQLite allowed for local dev)
* JWT authentication

### Infrastructure

* Docker
* Environment variables (`.env`)
* Stripe for payments
* REST API (no GraphQL)

---

## 📦 Core Product Modules (MUST IMPLEMENT)

### 1️⃣ Authentication & Users

* Email + password login
* JWT-based auth
* Roles:

  * `student`
  * `pro`
  * `admin`

---

### 2️⃣ AI Credit System (CRITICAL)

* Each user has **monthly AI credits**
* Credits decrease per AI request
* Prevent AI calls when credits = 0
* Credits reset monthly
* Store usage history

Example:

```text
Student Plan ($10):
- 200 AI requests / month
```

---

### 3️⃣ AI App Generator

* Accept natural language app description
* Generate:

  * Database schema
  * Backend APIs
  * Frontend pages
* Code must be:

  * Modular
  * Editable
  * Saved to project folders
* No pseudo-code

---

### 4️⃣ App Templates (Initial)

* SaaS starter app
* CRUD dashboard
* Subscription-based app
* Admin panel

Templates must include:

* Auth
* Database
* Stripe subscriptions
* Protected routes

---

### 5️⃣ Stripe Subscription System

* Stripe Checkout
* Monthly subscriptions
* Webhooks for:

  * Subscription created
  * Payment failed
  * Subscription cancelled
* Sync Stripe status to database
* Disable AI access if payment fails

---

### 6️⃣ Deployment Support

* Generated apps must be deployable:

  * Locally
  * Vercel (frontend)
  * Railway / AWS / DigitalOcean (backend)
* Provide README instructions per app

---

## 📁 Required Folder Structure

### Backend

```text
backend/
 ├─ app/
 │  ├─ api/
 │  ├─ core/
 │  ├─ models/
 │  ├─ services/
 │  ├─ auth/
 │  └─ main.py
 ├─ Dockerfile
 └─ requirements.txt
```

### Frontend

```text
frontend/
 ├─ src/
 │  ├─ pages/
 │  ├─ components/
 │  ├─ services/
 │  ├─ hooks/
 │  └─ main.tsx
 ├─ Dockerfile
 └─ vite.config.ts
```

---

## 🔐 Security & Quality Rules

* Never hardcode secrets
* Use environment variables
* Validate all inputs
* Rate-limit AI endpoints
* Handle Stripe webhooks securely
* Follow REST best practices

---

## 🚫 Out of Scope (DO NOT IMPLEMENT)

* CMS / blog features
* Website builder / landing pages
* Mobile apps
* Chatbots inside user apps
* SEO features

---

## 📊 UX Expectations

* Clean developer-focused UI
* Clear error messages
* Progress indicators for AI generation
* Credit usage visible to users
* Download / export code option

---

## 🧪 Testing Expectations

* Basic unit tests for:

  * Auth
  * AI credit logic
  * Stripe webhook handling
* No snapshot testing

---

## 🧾 Documentation

* Each module must have:

  * Docstrings
  * Clear README
* Assume users are **students & junior developers**

---

## ✅ Final Instruction to Copilot

> Always implement features as if this is a **real SaaS product with paying users**.
> No shortcuts. No demo-only logic.
> Optimize for **clarity, cost efficiency, and maintainability**.

---

# 🚀 How You Use This Practically

1. Create repo
2. Paste this into `COPILOT_INSTRUCTIONS.md`
3. Open Copilot Chat
4. Say:

   > “Design the backend architecture first based on the instructions.”
5. Then:

   > “Implement authentication and AI credit system.”
6. Then:

   > “Add Stripe subscription flow.”

---

## 🔥 Next Steps I Strongly Recommend

I can now:
1️⃣ Break this into **Copilot task-by-task prompts**
2️⃣ Design **Stripe schema + webhook code**
3️⃣ Create **AI credit calculation logic**
4️⃣ Draft **student landing page copy**
5️⃣ Create **database schema diagram**

Reply with the **number (1–5)** and I’ll continue step by step.
