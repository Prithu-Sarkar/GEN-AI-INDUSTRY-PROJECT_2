# 🧠 Swarm Automation — README

### Overview  
This system is a **multi-agent swarm** built inside **n8n**, designed to interpret natural language commands (via Telegram, voice, or image) and automatically route them to the correct AI sub-agent workflows.  

The swarm intelligently handles:  
📩 Emails → Gmail  
📅 Calendar events → Google Calendar  
✈️ Travel planning → SerpAPI (Flights + Hotels)  
🔍 Research & knowledge → Tavily Search + Wikipedia  

All outputs are sanitized into **Telegram-safe plain text** for seamless user interaction.

---

## 🏗️ Swarm Architecture

### 🔹 1️⃣ Main Routing Agent  
**Workflow:** `Main Workflow.json`  
**Model:** Google Gemini  
**Role:**  
The brain of the swarm — interprets user intent, determines which sub-agent(s) to trigger, and merges their outputs.

**Responsibilities:**
- Detect intent from text, image, or voice.  
- Route task(s) to Email, Calendar, Travel, or Research agents.  
- Handle **compound queries** logically (e.g., “book flight + add to calendar + email itinerary”).  
- Convert all times to ISO 8601 (IST) → `YYYY-MM-DDThh:mm:ss+05:30`.  
- Merge sub-agent outputs into one concise message.  
- Format everything for **Telegram Parse Mode: None** (no Markdown/HTML).  

**Compound Routing Examples:**
| Query | Routing Order |
|--------|----------------|
| “Send an email to HR about leave.” | Email |
| “Schedule a meeting tomorrow.” | Calendar |
| “Find flights Delhi → Mumbai.” | Travel |
| “Research latest OpenAI updates.” | Research |
| “Find hotels in Goa and set reminder.” | Travel → Calendar |
| “Book flight and email me top options.” | Travel → Email |
| “Plan Tokyo trip — flight, calendar, email itinerary.” | Travel → Calendar → Email |
| “Research AI tools and email summary.” | Research → Email |

---

### 🔹 2️⃣ Email Agent  
**Workflow:** `Email Workflow.json`  
**Model:** GPT-4o  
**Purpose:** Manage Gmail operations automatically.

**Capabilities:**
- Send, read, reply, delete, or search emails.
- Summarize unread messages with sender, subject, and timestamp (ISO 8601 +05:30).  
- Confirm before mass deletes.  
- Output clean, short summaries ready for Telegram.

**Example Output:**
```
Action: Email Sent
To: hr@company.com
Subject: Leave Request
Timestamp: 2025-11-07T09:00:00+05:30
Status: Success
— End of results —
```

---

### 🔹 3️⃣ Calendar Agent  
**Workflow:** `Calendar Workflow.json`  
**Model:** GPT-4o  
**Purpose:** Handle all scheduling-related tasks.

**Capabilities:**
- Create, update, delete events.  
- Check availability or list events by date range.  
- Detect and resolve conflicts automatically.  
- Always output timestamps in ISO 8601 (IST).

**Example Output:**
```
Action: Event Created
Title: Team Sync
Start: 2025-11-08T15:00:00+05:30
End: 2025-11-08T16:00:00+05:30
Status: Confirmed
— End of results —
```

---

### 🔹 4️⃣ Travel Agent  
**Workflow:** `Travel Agent.json`  
**Model:** GPT-4o  
**Purpose:** Search and summarize **flights** and **hotels** using SerpAPI.

**Capabilities:**
- Flights → Find by departure/arrival/dates/class.  
- Hotels → Find by location, dates, rating, and class.  
- Defaults: One-way, 1 adult, economy, 4★+ hotels, rating ≥ 8.  
- Suggest alternative routes if no results.

**Example Output:**
```
Search Results: Flights
1) Air India — DEL → BKK
   Departure: 2025-12-05T11:05:00+05:30
   Duration: 4h20m
   Price: ₹8,200
2) IndiGo — DEL → BKK
   Departure: 2025-12-05T15:30:00+05:30
   Price: ₹7,800
— End of results —
```

**Mixed Example:**  
“Find hotels in Goa and add check-in reminder.”  
→ Travel Agent → Calendar Agent  

---

### 🔹 5️⃣ Research Agent  
**Workflow:** `Research Agent.json`  
**Model:** Google Gemini  
**Purpose:** Retrieve factual or recent information using **Wikipedia** (for structured facts) and **Tavily Search** (for current updates).

**Tool Logic:**
- **Wikipedia:** Definitions, background, static data.  
- **Tavily:** Recent events, trending topics, new releases.  
- **Combined Mode:** For hybrid queries (e.g., “latest ChatGPT updates”).  

**Example Output:**
```
ChatGPT is a conversational AI model by OpenAI.
Recent updates (2025-11-07T00:00:00+05:30):
- Introduced voice mode
- Faster responses
- Added memory recall
— End of results —
```

---

## ⚙️ Data Flow Summary

1️⃣ **User** sends message (text, voice, or image) via Telegram.  
2️⃣ **Main Routing Agent** detects intent and selects appropriate sub-agent(s).  
3️⃣ **Sub-Agent(s)** execute relevant workflow logic.  
4️⃣ **Outputs** are merged, simplified, and formatted into Telegram-safe text.  
5️⃣ **Telegram Bot** sends clean final message back to user.

---

## 🧩 Example End-to-End Scenarios

| User Query | Routed Agents | Final Outcome |
|-------------|----------------|----------------|
| “Send an email to HR about my leave.” | Email | Sends email, returns confirmation |
| “Book flight to Tokyo, add to calendar, email itinerary.” | Travel → Calendar → Email | Flight booked, event added, itinerary emailed |
| “Find hotel in Goa July 5–7 and remind me 1 day before check-in.” | Travel → Calendar | Hotel found + reminder scheduled |
| “Research OpenAI news and email summary.” | Research → Email | Generates research summary and emails it |
| “Check unread emails and schedule follow-ups.” | Email → Calendar | Extracts emails + creates events |

---

## ✅ Design Principles

- **Agentic Modularity:** Each agent is independent yet orchestrated via the Main Router.  
- **Sequential Chaining:** Multi-step queries route in logical order.  
- **Timezone Uniformity:** All dates in ISO 8601 (Asia/Kolkata).  
- **Telegram Safety:** Clean text only, under 4096 characters.  
- **Minimal Clarification:** The system asks only when data is missing.  

---

## 🧩 Tech Stack

| Layer | Tools |
|-------|-------|
| LLMs | Google Gemini & OpenAI GPT-4o |
| Integrations | Gmail, Google Calendar, SerpAPI, Tavily, Wikipedia |
| Platform | n8n (AI-powered automation) |
| Input Modes | Telegram (text, voice, image) |
| Output Mode | Telegram-safe plain text |

---

## 🏁 Outcome
This swarm acts as an **autonomous multimodal assistant** capable of:  
✅ Managing Gmail & Calendar  
✅ Planning trips & hotels  
✅ Researching web data  
✅ Combining agents for complex workflows  
✅ Communicating smoothly via Telegram  
