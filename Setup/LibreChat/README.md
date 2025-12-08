# LibreChat Setup Guide

This guide will help you set up LibreChat with Directus MCP integration and optimized local LLM support.

---

## Prerequisites

Before you begin, ensure you have:

- **Docker & Docker Compose** installed
- **Ollama** installed ([ollama.ai](https://ollama.ai))
- **Git** installed
- At least **16GB RAM** (32GB recommended for larger models)
- **GPU** (optional but recommended for faster inference)

---

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/danny-avila/LibreChat.git
cd LibreChat
```

### 2. Replace Configuration Files

This project includes pre-configured files optimized for Directus integration:

```bash
# Copy the provided librechat.yaml
cp /path/to/provided/librechat.yaml ./librechat.yaml

# Copy the Modelfile for optimized local LLM
cp /path/to/provided/Modelfile ./Modelfile
```

**Files included:**
- `librechat.yaml` - Complete LibreChat configuration with Directus MCP
- `Modelfile` - Optimized Ollama model for Directus interactions

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` and add these required variables:

```env
# Directus Configuration
DIRECTUS_URL=https://lms.tecktal.ai
DIRECTUS_TOKEN=your_directus_static_token_here

# OpenAI API (optional, for GPT models)
OPENAI_API_KEY=your_openai_api_key_here

# Other required variables
APP_TITLE=LibreChat
DOMAIN_CLIENT=http://localhost:3080
DOMAIN_SERVER=http://localhost:3080

# Database
MONGO_URI=mongodb://mongodb:27017/LibreChat

# Search
MEILI_MASTER_KEY=your_meili_master_key
```

**How to get Directus token:**
1. Log into your Directus instance at https://lms.tecktal.ai
2. Go to Settings → Access Tokens
3. Create a new static token with appropriate permissions
4. Copy the token to your `.env` file

---

## Setting Up Local LLM (Ollama)

### 1. Install Ollama

**Windows:**
Download from [ollama.ai](https://ollama.ai) and install

**Linux/Mac:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Pull Base Models

```bash
# For fast inference (recommended for testing)
ollama pull qwen2.5-coder:14b

# For best quality (requires more RAM/VRAM)
ollama pull qwen2.5:32b
```

### 3. Create Optimized Model

Use the provided Modelfile to create a model optimized for Directus interactions:

```bash
# Navigate to LibreChat directory
cd LibreChat

# Create the optimized model
ollama create directus-assistant -f Modelfile

# Verify creation
ollama list
```

You should see `directus-assistant` in the list.

---

## Starting LibreChat

### 1. Start Docker Services

```bash
# Start all services
docker-compose up -d

# Check logs
docker logs LibreChat -f
```

**Wait for initialization message:**
```
MCP servers initialized successfully. Added 20 MCP tools.
```

This confirms Directus MCP is connected.

### 2. Access LibreChat

Open your browser and navigate to:
```
http://localhost:3080
```

### 3. Create an Account

1. Click "Sign Up"
2. Create your account
3. Log in

---

## Creating the Directus Research Agent

### 1. Navigate to Agents

Click the **"Agents"** icon in the left sidebar

### 2. Create New Agent

Click **"+ New Agent"**

### 3. Configure Agent

**Basic Settings:**
- **Name:** Directus Research Assistant
- **Description:** Expert assistant with access to Directus LMS database
- **Category:** General

**Model Settings:**
- **Provider:** Qwen Local (or Ollama)
- **Model:** `directus-assistant` (the model you created)

**Instructions:**

The agent instructions are already configured in the LibreChat system through `librechat.yaml`. You can add additional custom instructions here if needed.

**Recommended additional instructions:**
```
You are helping users navigate and manage educational content in a Directus LMS. 

Be helpful, precise, and always format responses beautifully with proper markdown. When users ask for lesson plans, always provide the PDF link by default unless they specifically request the content.
```

### 4. Add Tools

1. Click **"Add Tools"**
2. You should see **"directus"** in the MCP servers list
3. Click to expand and you'll see 20 tools
4. Click **"Add All Tools"** or select specific tools
5. Click **"Save"**

**Available Directus Tools:**
- read-collections
- read-items
- read-fields
- create-item
- update-item
- read-users
- read-files
- read-folders
- And 12 more...

### 5. Configure Model Parameters (Optional)

Click **"Model Parameters"** to fine-tune:

**Recommended settings:**
- **Temperature:** 0.12 (already set in Modelfile)
- **Max Context Tokens:** 16384
- **Max Output Tokens:** 2048
- **Top P:** 0.90

These are optimized for precise tool calling.

### 6. Save Agent

Click **"Save"** at the bottom of the agent builder.

---

## Testing Your Setup

### Test 1: Basic Query

Ask your agent:
```
Show me all courses
```

**Expected response:**
A formatted list of courses with titles and descriptions.

### Test 2: Hierarchical Navigation

```
Get modules for Foundations of Algebra
```

**Expected response:**
A tree structure showing all modules in that course.

### Test 3: Lesson Plan Retrieval

```
Get lesson plan for Lesson 1: Mastering Arithmetic Operations
```

**Expected response:**
A link to download the lesson plan PDF.

### Test 4: Quiz Query

```
Get quiz for Module 1
```

**Expected response:**
Quiz title, description, and all questions with correct answers marked.

### Test 5: Lesson Plan Update (Critical Test)

```
Update the lesson plan for Lesson 1, change the objective from "Learn addition" to "Master addition and subtraction"
```

**Expected workflow:**
1. Agent shows current content
2. Agent asks for confirmation
3. You confirm
4. Agent updates and returns NEW PDF URL

---

## Alternative: Using GPT Models

If you prefer using GPT models instead of local LLMs:

### 1. Add OpenAI API Key

Ensure `OPENAI_API_KEY` is set in your `.env` file

### 2. Create Agent with OpenAI

When creating the agent:
- **Provider:** OpenAI
- **Model:** gpt-4o or gpt-4o-mini

The Directus MCP tools work with any model provider.

---

## Troubleshooting

### MCP Tools Not Showing (0 tools)

**Check logs:**
```bash
docker logs LibreChat | grep MCP
```

**Common issues:**
1. **DIRECTUS_TOKEN not set**: Check your `.env` file
2. **Directus not accessible**: Verify `DIRECTUS_URL` is correct
3. **Docker restart needed**: Run `docker-compose restart`

**Solution:**
```bash
docker-compose down
docker-compose up -d
docker logs LibreChat -f
```

Look for:
```
[MCP][directus] ✓ Initialized
MCP servers initialized successfully. Added 20 MCP tools.
```

### Ollama Model Not Found

**Error:** "The model 'directus-assistant' is not available"

**Solution:**
```bash
# Verify model exists
ollama list

# If not found, recreate it
ollama create directus-assistant -f Modelfile
```

### Slow Response Times

**Issue:** Agent takes 20-30 seconds to respond

**Solutions:**

1. **Use smaller model:**
```bash
ollama pull qwen2.5-coder:14b
# Update agent to use qwen2.5-coder:14b instead
```

2. **Enable GPU acceleration:**
```bash
# Check if GPU is being used
ollama ps
```

3. **Increase Docker resources:**
Docker Desktop → Settings → Resources → Increase CPU/Memory

### Agent Can't Find Collections

**Error:** "Permission denied on field 'course_id'"

**Cause:** This is a field naming issue (documented in instructions)

**Solution:** The agent should automatically retry with correct field names. If persisting:
- Restart LibreChat
- Recreate the agent
- Verify Directus token has proper permissions

### Connection Timeout

**Error:** "MCP initialization timed out"

**Solution:**
```bash
# Increase timeout in librechat.yaml
mcpServers:
  directus:
    initTimeout: 180000  # 3 minutes
    timeout: 120000      # 2 minutes
```

Then restart:
```bash
docker-compose restart
```

---

## Advanced Configuration

### Multiple Model Options

You can configure multiple Ollama models in `librechat.yaml`:

```yaml
custom:
  - name: "Ollama"
    models:
      default:
        - "directus-assistant"  # Optimized for Directus
        - "qwen2.5-coder:14b"   # Fast alternative
        - "llama3.3:70b"        # High quality
```

Then select the appropriate model when creating agents.

### Custom System Prompts

While the Modelfile includes optimized instructions, you can add conversation-specific instructions in the agent builder for different use cases:

**Example - Student Support Agent:**
```
You're helping students navigate course materials. Be encouraging and patient. Always offer to find related resources when answering questions.
```

**Example - Content Management Agent:**
```
You're assisting instructors with content management. Focus on accuracy and always confirm before making updates. Provide clear summaries of changes.
```

---

## Updating LibreChat

To get the latest LibreChat updates:

```bash
# Pull latest changes
git pull origin main

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

**Note:** Your `librechat.yaml` and `Modelfile` won't be overwritten.

---

## Performance Optimization

### For Maximum Speed:

1. **Use GPU-accelerated Ollama**
2. **Use smaller models for simple queries:**
   - `qwen2.5-coder:14b` - Fast, good quality
   - `llama3.2:latest` - Very fast, lighter tasks

3. **Reduce context windows in agent settings:**
   - Max Context: 8192 (instead of 16384)
   - Max Output: 1024 (instead of 2048)

### For Best Quality:

1. **Use larger models:**
   - `qwen2.5:32b` - Best quality for local
   - `llama3.3:70b` - Highest quality (requires 48GB+ RAM)

2. **Or use GPT-4:**
   - Provider: OpenAI
   - Model: gpt-4o

---

## Next Steps

After successful setup:

1. **Explore the Directus documentation** to understand the LMS schema
2. **Create multiple agents** for different use cases (student support, content management, etc.)
3. **Customize agent instructions** for specific workflows
4. **Share agents with your team** using LibreChat's sharing features

---

## Support & Resources

- **LibreChat Documentation:** https://www.librechat.ai/docs
- **Ollama Documentation:** https://ollama.ai/docs
- **Directus MCP Documentation:** https://docs.directus.io/mcp

For project-specific issues, check the main repository README.

---

## Security Notes

⚠️ **Important Security Considerations:**

1. **Keep your `.env` file secure** - Never commit it to version control
2. **Use strong passwords** for all services
3. **Limit Directus token permissions** to only what's needed
4. **Use HTTPS in production** - The provided setup uses HTTP for local development only
5. **Regularly update** Docker images and Ollama models

---

**Setup complete!** You now have a fully functional LibreChat instance with Directus MCP integration and optimized local LLM support.