# Phase 2: LLM Integration - Implementation Plan

**Date**: October 2, 2025  
**Decision**: Start with Gemini 2.5 Pro only  
**Future**: Add GPT-5-codex and Claude Sonnet 4.5 later  

---

## 🎯 Phase 2 Goal

Add **Gemini 2.5 Pro intelligence** to the autonomous engine for:
1. **Intelligent goal decomposition** - Break down complex goals
2. **Real code generation** - Write actual code, not templates
3. **Error analysis** - Understand what went wrong
4. **Self-correction** - Fix errors automatically

---

## ✅ Why Start with Gemini

1. ✅ **Already integrated** - Used by JAi Cortex
2. ✅ **Authentication setup** - GCP credentials already configured
3. ✅ **Fast and cheap** - Good for rapid iteration
4. ✅ **Proven** - Already powering JAi successfully
5. ✅ **Function calling** - Supports tool use
6. ✅ **Large context** - 2M token window

**Result**: Fastest path to working autonomous intelligence

---

## 🏗️ Phase 2 Architecture

```python
from google import genai

class AutonomousEngine:
    def __init__(self):
        self.llm = genai.GenerativeModel('gemini-2.5-pro')
        self.task_manager = TaskManager()
        self.environment = EnvironmentTools()
        
    async def decompose_goal(self, goal: str) -> List[Task]:
        """Use Gemini to intelligently break down the goal."""
        prompt = f"""
        Break down this goal into specific, executable tasks:
        Goal: {goal}
        
        Return a JSON list of tasks with:
        - description: What to do
        - type: 'create_file', 'write_code', 'run_command', etc.
        - details: Specific information needed
        """
        
        response = await self.llm.generate_content(prompt)
        tasks = parse_tasks(response.text)
        return tasks
        
    async def execute_task(self, task: Task) -> dict:
        """Use Gemini to generate execution plan for the task."""
        if task.type == 'write_code':
            # Use Gemini to write the actual code
            code = await self.generate_code(task)
            result = self.environment.create_file(task.filename, code)
            return result
        else:
            # Execute other task types
            return await self.execute_generic_task(task)
            
    async def generate_code(self, task: Task) -> str:
        """Use Gemini to generate actual code."""
        prompt = f"""
        Write production-quality code for:
        {task.description}
        
        Requirements:
        - Language: {task.language}
        - Framework: {task.framework}
        - Include proper imports
        - Add error handling
        - Follow best practices
        
        Return ONLY the code, no explanation.
        """
        
        response = await self.llm.generate_content(prompt)
        return response.text
```

---

## 📋 Phase 2 Implementation Steps

### Step 1: Gemini Integration (1-2 hours)
- [ ] Add Gemini client to autonomous_engine.py
- [ ] Create prompt templates for goal decomposition
- [ ] Test basic LLM integration
- [ ] Verify authentication works

### Step 2: Intelligent Goal Decomposition (2-3 hours)
- [ ] Build `decompose_goal_with_llm()` function
- [ ] Create prompts for different goal types
- [ ] Parse LLM responses into Task objects
- [ ] Test with complex goals

### Step 3: Code Generation (2-3 hours)
- [ ] Build `generate_code_with_llm()` function
- [ ] Create prompts for different languages (Python, TypeScript, etc.)
- [ ] Handle code extraction from LLM responses
- [ ] Test code quality

### Step 4: Error Analysis & Self-Correction (2-3 hours)
- [ ] Build `analyze_error_with_llm()` function
- [ ] Create prompts for error diagnosis
- [ ] Generate fix strategies
- [ ] Test self-correction loop

### Step 5: Integration & Testing (2-3 hours)
- [ ] Connect all pieces together
- [ ] Test end-to-end autonomous execution
- [ ] Verify complex scenarios work
- [ ] Document any limitations

**Total Estimated Time**: 9-14 hours of focused work

---

## 🧪 Test Scenarios for Phase 2

### Test 1: Simple Component
**Goal**: "Create a React Button component"

**Expected**:
- Gemini decomposes into: Create file, write component, add types
- Gemini generates actual React code
- File created with working code
- Component is functional

### Test 2: Component with Tests
**Goal**: "Create a React Button component with tests"

**Expected**:
- Gemini creates component file
- Gemini creates test file
- Both files have real, working code
- Tests are runnable

### Test 3: Full Feature
**Goal**: "Create a login form with validation"

**Expected**:
- Multiple files created (form, validation, types)
- Real TypeScript/React code
- Proper error handling
- Working validation logic

### Test 4: Self-Correction
**Goal**: "Create a function that has an intentional error"

**Expected**:
- Gemini creates code
- Error detected when run
- Gemini analyzes error
- Gemini generates fix
- Fixed code works

---

## 🎯 Success Criteria for Phase 2

Phase 2 is **COMPLETE** when:

1. ✅ Gemini can break down complex goals into tasks
2. ✅ Gemini generates actual working code (not templates)
3. ✅ Files are created with real, functional code
4. ✅ Errors are detected and analyzed
5. ✅ Self-correction fixes at least simple errors
6. ✅ End-to-end test completes successfully

---

## 🔮 Future Enhancements (Post Phase 2)

Once Gemini version works:

### Add GPT-5-codex
- Use for complex code generation
- Leverage Responses API
- Handle advanced algorithms

### Add Claude Sonnet 4.5
- Use for agent workflows
- Leverage memory features
- Handle multi-step coordination

### Multi-LLM Orchestration
- Route tasks to best LLM
- Fallback if one fails
- Cost optimization

---

## 📝 Next Session Plan

When ready to start Phase 2:

1. **Review Phase 1 results** - Confirm foundation is solid
2. **Start with Step 1** - Add Gemini integration
3. **Test incrementally** - Verify each step works
4. **Build step-by-step** - No rushing

**Estimated Sessions**: 2-3 focused sessions to complete Phase 2

---

## 🎯 Current Status

- ✅ Phase 1: Complete & tested
- 🔄 Phase 2: Ready to start
- ⏳ Phase 3: Waiting for Phase 2

**Decision**: Use Gemini only for Phase 2  
**Future**: Add GPT-5-codex and Claude Sonnet 4.5 when needed  
**Timeline**: Start Phase 2 next session  

---

**Ready when you are!** 🚀

