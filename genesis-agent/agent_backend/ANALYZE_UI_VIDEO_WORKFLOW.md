# 🎬 Analyze UI/UX Video - Complete Workflow

## Your Goal
Film the Dream Machine app → Upload video → Get detailed UI analysis → Get code structure to replicate it

---

## Step 1: Film Your Video

**What to capture:**
- Full screen recording of the Dream Machine app
- Show the entire layout
- Navigate through different sections
- Interact with key features
- Keep it **under 2 minutes** for faster processing

**Tools:**
- Mac: QuickTime Player → File → New Screen Recording
- Or use: `Cmd + Shift + 5` (built-in screen recorder)

**Save as:** `dream_machine_ui.mp4`

---

## Step 2: Upload to Google Cloud Storage

```bash
# Upload your video
gsutil cp dream_machine_ui.mp4 gs://your-bucket/videos/

# Or use the web console
# https://console.cloud.google.com/storage
```

**Get the public URL:** `gs://your-bucket/videos/dream_machine_ui.mp4`

---

## Step 3: Ask JAi to Analyze

### Option A: Via ADK Dev-UI (EASIEST)

```bash
cd "/Users/liverichmedia/Agent master /genesis-agent/agent_backend"
adk dev-ui
```

Go to `http://localhost:8000`

**Upload the video** and type:

```
Analyze this Dream Machine UI video and provide:

1. **Layout Structure Analysis:**
   - Overall page structure (header, main content, sidebar, footer)
   - Grid system or flexbox layout used
   - Responsive breakpoints

2. **Color Palette:**
   - Primary, secondary, accent colors
   - Background gradients
   - Text color hierarchy

3. **Typography:**
   - Font families
   - Font sizes and weights
   - Line heights and spacing

4. **UI Components:**
   - List all major components (buttons, cards, modals, etc.)
   - Component styling patterns
   - Animation/transition effects

5. **Video Player Integration:**
   - How the video player is embedded
   - Controls and features
   - Aspect ratio handling

6. **Code Structure to Replicate:**
   - React component hierarchy
   - CSS/Tailwind class structure
   - State management approach
   - API calls needed

Please provide actual code snippets I can use to build this same layout.
```

### Option B: Programmatically

```python
from jai_cortex_working import chat
import asyncio

async def analyze_dream_machine_ui():
    prompt = """
    I've uploaded a video of the Dream Machine app UI at:
    gs://your-bucket/videos/dream_machine_ui.mp4
    
    Please analyze the video and provide:
    1. Complete layout structure breakdown
    2. Color scheme and typography details
    3. All UI components and their styling
    4. Code structure (React components) to replicate this
    5. CSS/Tailwind classes needed
    6. Any animations or transitions
    
    Give me actual code I can use to build this same interface.
    """
    
    response = await chat(prompt)
    print(response)

asyncio.run(analyze_dream_machine_ui())
```

---

## Step 4: What JAi Will Return

### Example Output Structure:

```markdown
# Dream Machine UI Analysis

## 1. Layout Structure
The app uses a grid-based layout:
- Header: Fixed, 64px height
- Main content: 70% width, centered
- Sidebar: 30% width, sticky position
- Footer: Full width, 80px height

## 2. Color Palette
- Primary: #FF6B6B (coral red)
- Secondary: #4ECDC4 (turquoise)
- Background: Linear gradient from #1A1A2E to #16213E
- Text: #FFFFFF (white), #A8A8A8 (gray)

## 3. Typography
- Headings: Inter, 600 weight, 32px
- Body: Inter, 400 weight, 16px
- Line height: 1.6

## 4. UI Components

### Video Player
```jsx
<div className="video-container relative w-full aspect-video rounded-2xl overflow-hidden">
  <video 
    className="w-full h-full object-cover"
    controls
    autoPlay
    loop
  >
    <source src="video.mp4" type="video/mp4" />
  </video>
  <div className="controls absolute bottom-4 left-4 right-4 flex gap-2">
    <button className="bg-white/20 backdrop-blur-md rounded-full p-3">
      {/* Play button */}
    </button>
  </div>
</div>
```

### Main Layout
```jsx
function DreamMachineUI() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <VideoPlayer />
            <PromptInput />
          </div>
          <aside className="lg:col-span-1">
            <GeneratedVideos />
          </aside>
        </div>
      </main>
    </div>
  );
}
```

## 5. Complete Code Structure

[Full React component code here...]
```

---

## Step 5: Build Your Version

1. Take the code JAi provides
2. Create new React components
3. Apply the styling
4. Test and refine

---

## Alternative: Use Gemini Vision Directly

If you want INSTANT analysis without waiting for Video Intelligence:

```python
from google import genai
from google.genai import types

client = genai.Client(vertexai=True)

# Upload video
response = client.models.generate_content(
    model="gemini-2.0-flash-exp",
    contents=[
        types.Part.from_uri(
            file_uri="gs://your-bucket/videos/dream_machine_ui.mp4",
            mime_type="video/mp4"
        ),
        """Analyze this UI and provide:
        1. Layout structure
        2. Color scheme
        3. Component breakdown
        4. React code to replicate it
        """
    ]
)

print(response.text)
```

This is **FASTER** because it uses Gemini's native video understanding (not Video Intelligence API).

---

## Which Method Should You Use?

### For UI/UX Analysis:
**USE GEMINI VISION** (faster, better for design analysis)

### For Video Content Analysis:
**USE VIDEO INTELLIGENCE API** (better for detecting objects, scenes, labels)

---

## Test It NOW

1. Film your Dream Machine video
2. Upload to GCS or provide to JAi
3. Use the prompt above
4. Get your code structure

**Ready to test?**

