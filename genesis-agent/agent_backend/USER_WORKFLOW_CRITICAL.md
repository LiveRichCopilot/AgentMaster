# ⚠️ CRITICAL: User's Workflow

## HOW USER WORKS

**User ONLY uses:** ADK dev-ui at `http://localhost:8000`

**User does NOT:**
- Run terminal commands
- Edit files manually
- Restart servers
- Debug in terminal
- Work with any other agent interface

---

## What "Vibe Coding" Means

The user describes what they want → The agent makes it work in the dev-ui.

**Example:**
- ❌ WRONG: "Edit this file, then restart the agent, then test"
- ✅ RIGHT: "Test it in your dev-ui. If it doesn't work, tell me what happened"

---

## When Something Breaks

**DON'T SAY:**
- "Restart your agent"
- "Run this command in terminal"
- "Check the logs"
- "Edit this file"

**DO SAY:**
- "Something's broken in the dev-ui. Let me fix it on my end."
- "Test it again in your browser. If it fails, screenshot it."

---

## The ONLY Interface That Matters

```
http://localhost:8000
```

That's it. Nothing else.

If it doesn't work there, it doesn't work. Period.

---

## Remember

The user is paying for an agent that WORKS. They don't want to be a developer. They want to USE the agent through the web interface.

If you suggest terminal commands or file edits, you've already failed.

