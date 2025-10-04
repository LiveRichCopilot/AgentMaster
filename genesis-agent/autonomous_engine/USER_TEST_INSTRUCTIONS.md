# 🧪 Autonomous Engine - User Test Instructions

**Goal**: Test the autonomous engine in a safe, controlled environment to verify it works as expected.

---

## 📋 **Test Scenario**

The autonomous engine will perform a simple, non-critical task:

**Task**: Create a new file named `test_run.txt` and write "Autonomous engine test successful. Date: [current date]" inside it.

---

## 🚀 **How to Run the Test**

### Step 1: Navigate to the autonomous engine directory
```bash
cd "/Users/liverichmedia/Agent master /genesis-agent/agent_backend/autonomous_engine"
```

### Step 2: Run the autonomous engine with the test goal
```bash
python3 autonomous_engine.py
```

This will run the built-in test that creates a file called `hello.txt`.

### Step 3: Verify the result

After the engine finishes, check that the file was created:

```bash
cat autonomous_workspace/hello.txt
```

You should see:
```
// hello.txt
// Created by Autonomous Engine

File created by Autonomous Engine
```

---

## ✅ **Success Criteria**

The test is **SUCCESSFUL** if:

1. ✅ The engine runs without errors
2. ✅ You see the autonomous execution messages:
   - "🚀 AUTONOMOUS EXECUTION STARTED"
   - "🎯 Goal decomposed into X tasks"
   - "▶️ Starting task: ..."
   - "✅ Task completed: ..."
   - "✅ AUTONOMOUS EXECUTION COMPLETE"
3. ✅ The file `hello.txt` exists in `autonomous_workspace/`
4. ✅ The file contains the expected content
5. ✅ A state file (`execution_state.json`) was created

---

## 🔍 **What to Look For**

### Good Signs:
- ✅ Clear progress messages
- ✅ Tasks complete successfully
- ✅ File created correctly
- ✅ No errors in output

### Red Flags (Report These):
- ❌ Python errors or exceptions
- ❌ Tasks failing repeatedly
- ❌ File not created
- ❌ Execution hangs or freezes

---

## 🧪 **Advanced Test (Optional)**

If the basic test works, you can try a custom goal:

### Create a custom test file:

```bash
cat > test_custom_goal.py << 'EOF'
import asyncio
from autonomous_engine import run_autonomous_task

async def custom_test():
    result = await run_autonomous_task(
        goal="Create a file called my_test.txt with content 'I tested the autonomous engine!'",
        workspace_dir="./my_test_workspace"
    )
    print(f"\n🎯 Result: {result}")
    
asyncio.run(custom_test())
EOF
```

### Run it:
```bash
python3 test_custom_goal.py
```

### Verify:
```bash
cat my_test_workspace/my_test.txt
```

Should contain: `I tested the autonomous engine!`

---

## 📊 **Reporting Results**

After testing, report back:

1. **Did the basic test work?** (Yes/No)
2. **Did you see all the expected messages?** (Yes/No)
3. **Was the file created correctly?** (Yes/No)
4. **Any errors or issues?** (Describe)
5. **Optional: Did the custom test work?** (Yes/No/Didn't try)

---

## 🛡️ **Safety Notes**

- ✅ The autonomous engine can only work in its `autonomous_workspace` directory
- ✅ It cannot access your other files
- ✅ It has command validation to prevent dangerous operations
- ✅ You can stop it anytime with `Ctrl+C`

---

## 🎯 **What This Test Validates**

By running this test, you're verifying:

1. **Task Decomposition** - Can break down a goal into tasks
2. **Task Execution** - Can execute tasks using environment tools
3. **File Operations** - Can create and write files
4. **Progress Tracking** - Tracks and reports progress
5. **State Management** - Saves execution state
6. **Error Handling** - Handles errors gracefully
7. **Autonomous Loop** - Runs until completion

---

## 📞 **Next Steps After Testing**

### If everything works:
- ✅ Report success
- ✅ We'll review what you learned
- ✅ Then move to Phase 2 (LLM integration)

### If you find issues:
- 🔧 Report the issues
- 🔧 We'll fix them together
- 🔧 Re-test before moving forward

---

**Remember**: This is YOUR test. Take your time, observe everything, and report what you see. This is how we build confidence in the system together.

**Good luck! 🚀**

