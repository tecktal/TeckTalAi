# TeckTal AI - LMS Platform with AI-Powered Content Generation

A complete Learning Management System powered by **Directus CMS** + **LibreChat** + **Local LLMs**, featuring AI-driven content generation, interactive simulations, and intelligent course assistance.

---

## 🎯 What Is This?

This project provides a **complete, production-ready LMS platform** that combines:

1. **Directus CMS** - Flexible backend for managing courses, lessons, quizzes, and more
2. **LibreChat** - AI chat interface with direct access to your LMS database
3. **Local LLM Support** - Run powerful AI models locally (Ollama) or use cloud models
4. **RAG (Retrieval-Augmented Generation)** - AI generates content based on your curriculum
5. **Automated Workflows** - 13 pre-built flows for content generation and PDF management

---

## ✨ Key Features

### 🎓 Complete LMS Functionality
- **Courses** with modules and lessons
- **Quizzes** with multiple question types
- **Interactive simulations** for hands-on learning
- **Assignments** and downloadable resources
- **Student enrollments** and progress tracking
- **Comments** and course reviews
- **Instructor profiles** and course management

### 🤖 AI-Powered Content Generation
- **Generate course modules** from curriculum PDFs
- **Generate lessons** aligned with your curriculum
- **Generate lesson plans** in structured PDF format
- **Generate interactive simulations** automatically
- **Generate assignments** and quizzes
- **Q&A over course materials** using RAG

### 💬 Intelligent Assistant (LibreChat + MCP)
- **Natural language queries**: "Show me all physics courses"
- **Navigate hierarchies**: "Get modules for Foundations of Algebra"
- **Retrieve lesson plans**: "Give me the lesson plan for Lesson 1"
- **Update content**: "Change the lesson plan objective to..."
- **Query quizzes**: "Show me quiz questions for Module 2"
- **Direct database access** via Model Context Protocol (MCP)

### 🔧 Technical Highlights
- **Docker-based** - One-command setup
- **Pre-configured database** - 26+ collections ready to use
- **Custom services** - RAG (AI) + PDF generation
- **13 automated workflows** - Content generation, PDF processing
- **Local or cloud AI** - Your choice of models
- **Optimized instructions** - Fine-tuned for LMS operations

---

## 📊 Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                         USER                                  │
│                           │                                   │
│           ┌───────────────┼───────────────┐                  │
│           │                               │                  │
│           v                               v                  │
│    ┌─────────────┐                ┌─────────────┐           │
│    │  LibreChat  │◄───────MCP────►│  Directus   │           │
│    │   :3080     │                │    :8055    │           │
│    └─────────────┘                └──────┬──────┘           │
│           │                               │                  │
│           │                    ┌──────────┼──────────┐       │
│           │                    │          │          │       │
│           v                    v          v          v       │
│    ┌─────────────┐      ┌─────────┐ ┌────────┐ ┌────────┐  │
│    │    Ollama   │      │   RAG   │ │  PDF   │ │Postgres│  │
│    │   (Local    │      │ Service │ │Service │ │  :5432 │  │
│    │   LLMs)     │      │  :8000  │ │ :8001  │ └────────┘  │
│    └─────────────┘      └────┬────┘ └────────┘             │
│                              │                               │
│                              v                               │
│                         ┌─────────┐                          │
│                         │ Qdrant  │                          │
│                         │ :6333   │                          │
│                         │(Vectors)│                          │
│                         └─────────┘                          │
└──────────────────────────────────────────────────────────────┘
```

### Component Roles:

| Component | Purpose | Port |
|-----------|---------|------|
| **Directus** | LMS backend + admin panel | 8055 |
| **LibreChat** | AI chat interface + agent platform | 3080 |
| **Ollama** | Local LLM inference | 11434 |
| **RAG Service** | AI content generation | 8000 |
| **PDF Service** | Lesson plan PDF generation | 8001 |
| **PostgreSQL** | Database | 5432 |
| **Qdrant** | Vector database for RAG | 6333 |

---

## 🚀 Quick Start Guide

### Prerequisites

Before you begin, ensure you have:

- **Docker** & **Docker Compose** installed
- **Ollama** installed ([ollama.ai](https://ollama.ai)) - for local LLMs
- **Git** installed
- **At least 16GB RAM** (32GB recommended for large models)
- **30GB free disk space**
- **OpenAI API Key** (optional, for cloud models)

---

## 📂 Repository Structure

```
project-root/
├── README.md                    ← You are here (start here!)
│
├── Directus/                    ← Backend LMS setup
│   ├── README.md               ← Read this second
│   ├── docker-compose.yml
│   ├── .env.example
│   ├── postgres_data/          ← Pre-configured database
│   ├── extensions/             ← Custom Directus extensions
│   ├── uploads/                ← File uploads (created on first run)
│   ├── rag-service/           ← AI content generation
│   │   ├── main.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── pdf-service/           ← PDF generation
│       ├── main.py
│       ├── Dockerfile
│       └── requirements.txt
│
└── LibreChat/                   ← AI chat interface setup
    ├── README.md               ← Read this third
    ├── librechat.yaml          ← Pre-configured with Directus MCP
    ├── Modelfile               ← Optimized local LLM
    └── docker-compose.override.yaml
```

---

## 📖 Setup Instructions

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd <repo-directory>
```

### Step 2: Set Up Directus (Backend)

Follow the complete guide:

```bash
cd Directus
cat README.md  # Read the full setup instructions
```

**Quick summary:**
1. Configure `.env` file with your settings
2. Add your OpenAI API key (for content generation)
3. Run `docker-compose up -d`
4. Access Directus at `http://localhost:8055`
5. Create a static token for LibreChat

**Estimated time:** 10-15 minutes

### Step 3: Set Up LibreChat (Frontend)

Follow the complete guide:

```bash
cd LibreChat
cat README.md  # Read the full setup instructions
```

**Quick summary:**
1. Copy provided `librechat.yaml` and `Modelfile`
2. Configure `.env` with Directus connection
3. Install and configure Ollama
4. Create optimized local LLM model
5. Run `docker-compose up -d`
6. Create agent with Directus MCP tools

**Estimated time:** 15-20 minutes

### Step 4: Create Your First AI Agent

1. Open LibreChat: `http://localhost:3080`
2. Go to **Agents** → **New Agent**
3. Configure:
   - **Name:** Directus Research Assistant
   - **Provider:** Qwen Local (or OpenAI)
   - **Model:** directus-assistant (if using local)
4. Add **Tools** → Select all Directus MCP tools
5. Save and start chatting!

**Estimated time:** 5 minutes

---

## 🎮 What Can You Do?

### As a Content Creator (Directus):

```bash
# Access admin panel
http://localhost:8055

# What you can do:
1. Create courses and upload curriculum PDFs
2. Generate modules automatically (AI reads your PDFs)
3. Generate lessons for each module
4. Generate interactive simulations
5. Create quizzes and assignments
6. Generate professional lesson plan PDFs
7. Manage students and enrollments
```

### As a User (LibreChat Agent):

```bash
# Access chat interface
http://localhost:3080

# Example queries:
"Show me all courses"
"Get modules for Foundations of Algebra"
"Give me the lesson plan for Lesson 1"
"Show me quiz questions for Module 2"
"Find courses about physics"
"Update the lesson plan objective to..."
"What assignments are in Lesson 3?"
```

### As a Developer:

```bash
# Customize flows in Directus
Settings → Flows → Edit any flow

# Modify AI prompts
Edit: rag-service/main.py

# Add custom collections
Directus → Create Collection → Add fields

# Customize agent instructions
Edit: LibreChat agent instructions
```

---

## 🔐 Security Notes

### Important Security Steps:

1. **Change all default passwords** in `.env` files
2. **Generate secure random keys**:
   ```bash
   openssl rand -base64 32
   ```
3. **Use strong database passwords**
4. **Keep API keys secure** - Never commit `.env` to git
5. **Limit Directus token permissions** - Create role-based tokens
6. **Enable HTTPS in production** - Use nginx reverse proxy
7. **Regularly update** Docker images and dependencies

### Production Deployment:

- Use environment variable management (HashiCorp Vault, AWS Secrets Manager)
- Set up proper firewall rules
- Enable rate limiting
- Implement backup strategy
- Monitor logs for security events
- Use SSL/TLS certificates
- Restrict database access to internal network only

---

## 🧪 Testing Your Setup

### Test 1: Directus is Running

```bash
curl http://localhost:8055/server/health
```

Expected: `{"status":"ok"}`

### Test 2: RAG Service is Healthy

```bash
curl http://localhost:8000/health
```

Expected: `{"status":"healthy","qdrant_connected":true}`

### Test 3: PDF Service is Healthy

```bash
curl http://localhost:8001/health
```

Expected: `{"status":"healthy"}`

### Test 4: LibreChat Agent Works

1. Open LibreChat
2. Select your Directus agent
3. Ask: "Show me all courses"
4. Should return formatted list of courses

### Test 5: Content Generation Works

1. Log into Directus
2. Create a test course
3. Upload a PDF curriculum
4. Click "Generate Modules"
5. Wait for modules to appear
6. Verify they're aligned with your curriculum

---

## 📚 Documentation

### Detailed Guides:

- **[Directus Setup](./Directus/README.md)** - Complete backend setup with RAG and PDF services
- **[LibreChat Setup](./LibreChat/README.md)** - AI chat interface and agent configuration

### External Resources:

- **Directus:** https://docs.directus.io
- **LibreChat:** https://www.librechat.ai/docs
- **Ollama:** https://ollama.ai/docs
- **Model Context Protocol:** https://modelcontextprotocol.io

---

## 🛠 Troubleshooting

### Common Issues:

| Issue | Solution |
|-------|----------|
| **Port conflicts** | Check what's using ports 3080, 8055, 8000, 8001, 5432, 6333 |
| **MCP tools not showing** | Verify DIRECTUS_TOKEN in LibreChat .env |
| **Content generation fails** | Check OPENAI_API_KEY in Directus .env |
| **Slow responses** | Use smaller models (qwen2.5-coder:14b instead of :32b) |
| **Database connection fails** | Verify postgres is running: `docker ps` |
| **RAG not finding content** | Check PDFs are uploaded and processed |

### Getting Help:

1. Check service logs:
   ```bash
   docker-compose logs -f [service-name]
   ```

2. Verify environment variables:
   ```bash
   cat .env
   ```

3. Check service health endpoints (URLs above)

4. Review individual README files for service-specific troubleshooting

---

## 🎨 Customization

### Add Custom Collections:

1. Go to Directus → **Settings** → **Data Model**
2. Click **"Create Collection"**
3. Add fields as needed
4. Update agent instructions to include new collection

### Modify AI Behavior:

1. **For content generation:** Edit `Directus/rag-service/main.py`
2. **For agent responses:** Edit agent instructions in LibreChat
3. **For model behavior:** Edit `LibreChat/Modelfile` and rebuild model

### Add Custom Flows:

1. Go to Directus → **Settings** → **Flows**
2. Click **"+"** to create new flow
3. Configure trigger and operations
4. Test and activate

---

## 📈 Performance Optimization

### For Faster Responses:

1. **Use smaller models:**
   - `qwen2.5-coder:14b` - Good balance (recommended)
   - `llama3.2:latest` - Very fast for simple queries

2. **Reduce context windows:**
   - LibreChat agent settings: 8192 instead of 16384

3. **Enable GPU acceleration:**
   - Install NVIDIA drivers
   - Verify with `ollama ps`

### For Better Quality:

1. **Use larger models:**
   - `qwen2.5:32b` - Best local quality
   - `llama3.3:70b` - Highest quality (needs 48GB+ RAM)
   - `gpt-4o` - Best cloud quality

2. **Increase context windows:**
   - Agent settings: 32768 for complex queries

3. **Use cloud models for critical tasks:**
   - Set agent provider to OpenAI
   - Use gpt-4o or gpt-4o-mini

---

## 🤝 Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Areas for Contribution:

- Additional Directus flows
- Custom agent instructions
- New MCP tools
- Documentation improvements
- Bug fixes
- Performance optimizations

---

## 📄 License

[Add your license here]

---

## 🙏 Acknowledgments

This project is built on top of:

- **Directus** - Flexible CMS platform
- **LibreChat** - Open-source AI chat interface
- **Ollama** - Local LLM runtime
- **OpenAI** - AI models and APIs
- **Qdrant** - Vector database
- **Model Context Protocol** - Tool integration standard

---

## 🚀 Getting Started Checklist

Use this checklist to ensure proper setup:

### Directus Setup:
- [ ] Docker and Docker Compose installed
- [ ] `.env` file configured with secure keys
- [ ] OpenAI API key added
- [ ] `docker-compose up -d` executed
- [ ] Accessed Directus at http://localhost:8055
- [ ] Created admin account
- [ ] Verified 26+ collections exist
- [ ] Verified 13 flows are active
- [ ] Created static token for LibreChat
- [ ] Tested RAG service health endpoint

### LibreChat Setup:
- [ ] Ollama installed
- [ ] Base model pulled (`ollama pull qwen2.5:32b`)
- [ ] Custom model created (`ollama create directus-assistant -f Modelfile`)
- [ ] `librechat.yaml` copied to LibreChat folder
- [ ] `.env` configured with Directus URL and token
- [ ] `docker-compose up -d` executed
- [ ] Accessed LibreChat at http://localhost:3080
- [ ] Created user account
- [ ] Created agent with Directus MCP tools
- [ ] Verified 20 MCP tools loaded
- [ ] Tested basic query: "Show me all courses"

### Final Verification:
- [ ] Content generation works (generate modules)
- [ ] PDF generation works (lesson plans)
- [ ] Agent can query database
- [ ] Agent can update lesson plans
- [ ] Quiz queries work
- [ ] All services running: `docker ps` shows 8 containers

**Once all checkmarks are complete, your system is ready!** 🎉

---

**Need help?** Read the detailed setup guides in:
- `./Directus/README.md`
- `./LibreChat/README.md`

**Ready to start?** Begin with [Directus Setup](./Directus/README.md)!