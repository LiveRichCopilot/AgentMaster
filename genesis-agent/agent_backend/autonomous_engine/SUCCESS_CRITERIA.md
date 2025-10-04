# SUCCESS CRITERIA - Friend Chat App

This document defines the **immutable contract** for what it means to have a "working app."

The autonomous system **MUST NOT** declare success until **ALL** criteria are met.

---

## ✅ **Build Integrity** (All files must exist)

Required files:
- [ ] `app.py`
- [ ] `templates/index.html`  
- [ ] `static/style.css`
- [ ] `static/script.js`
- [ ] `requirements.txt`

**Verification:** Check that each file exists and has content (> 50 characters)

---

## ✅ **Backend Functionality** (API must work)

Required endpoints:
- [ ] `GET /` returns 200 OK
- [ ] `POST /chat` accepts JSON and returns 200 OK

**Verification:** Make HTTP requests with `requests` library

---

## ✅ **Frontend Functionality** (UI must work)

Required UI elements (must exist in browser):
- [ ] `#chat-container` - Main chat container
- [ ] `#message-form` - Form for sending messages  
- [ ] `#message-input` - Text input field
- [ ] `#send-button` or `button[type="submit"]` - Send button

Required behaviors:
- [ ] Page loads without JavaScript errors
- [ ] User can type in message input
- [ ] User can click send button
- [ ] No console errors logged

**Verification:** Use Playwright to load page in real browser and check DOM

---

## 🚫 **Failure Conditions**

Any of these = FAILURE:
- Missing any required file
- Any file is empty or has < 50 chars
- Backend endpoint returns 404, 500, or any non-200 status
- Frontend has JavaScript console errors
- Any required UI element is missing from DOM
- Page doesn't load within 10 seconds

---

## ✅ **Success = ALL Criteria Met**

The system declares success **ONLY** when:
- ✅ All 5 files exist with content
- ✅ Both backend endpoints work
- ✅ All 4 UI elements exist in browser
- ✅ Zero JavaScript errors
- ✅ User can interact with UI

**No exceptions. No shortcuts. 100% or failure.**

