# Directus LMS Setup Guide

This guide will help you set up the Directus LMS backend with all custom services, flows, and database schema.

---

## What's Included

This Directus setup includes:

- **Complete LMS Schema** - All collections for courses, modules, lessons, quizzes, and more
- **RAG Service** - AI-powered course content generation using OpenAI + vector search
- **PDF Service** - Automatic lesson plan PDF generation
- **Custom Flows** - 13 automated workflows for content generation
- **Extensions** - Pre-configured Directus extensions
- **PostgreSQL Database** - Pre-populated with schema and flows

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                     Directus Core                        │
│  (Admin Panel + API + MCP Server on port 8055)          │
└───────────────┬─────────────────────────────────────────┘
                │
    ┌───────────┼───────────┬──────────────┬─────────────┐
    │           │           │              │             │
    v           v           v              v             v
┌────────┐ ┌────────┐ ┌─────────┐  ┌──────────┐  ┌──────────┐
│Postgres│ │ Qdrant │ │   RAG   │  │   PDF    │  │Extensions│
│  :5432 │ │ :6333  │ │ Service │  │ Service  │  │  Folder  │
│        │ │        │ │  :8000  │  │  :8001   │  │          │
└────────┘ └────────┘ └─────────┘  └──────────┘  └──────────┘
     │          │           │             │             │
     v          v           v             v             v
  [Database] [Vectors] [AI Content] [PDF Gen]    [Custom UI]
```

### Services Explained:

1. **Directus** (`:8055`) - Main application server
2. **PostgreSQL** (`:5432`) - Database with complete LMS schema
3. **Qdrant** (`:6333`) - Vector database for RAG (similarity search)
4. **RAG Service** (`:8000`) - AI content generation (modules, lessons, lesson plans)
5. **PDF Service** (`:8001`) - Converts HTML lesson plans to PDF

---

## Prerequisites

- **Docker & Docker Compose** installed
- **At least 8GB RAM** (16GB recommended)
- **20GB free disk space**
- **OpenAI API Key** (for content generation features)

---

## Quick Start

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd <repo-directory>/Directus
```

### Step 2: Place Pre-configured Data

The repository includes pre-configured folders with complete database schema and extensions:

```
Directus/
├── postgres_data/          # ← Complete database with schema + flows
├── extensions/             # ← Custom Directus extensions
├── docker-compose.yml
├── .env.example
└── README.md
```

**Important:** The `postgres_data` and `extensions` folders are already configured. **DO NOT delete or modify them** unless you want to start fresh.

### Step 3: Configure Environment Variables

Create your `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and configure:

```env
# Security Keys (CHANGE THESE!)
KEY=your-super-secret-key-here-generate-random-string

# Admin Account
ADMIN_EMAIL=your-email@example.com
ADMIN_PASSWORD=your-secure-password

# Database Configuration (can keep defaults)
DB_CLIENT=pg
DB_HOST=postgres
DB_PORT=5432
DB_DATABASE=directus
DB_USER=directus_user
DB_PASSWORD=your-secure-db-password

# OpenAI API Key (REQUIRED for content generation)
OPENAI_API_KEY=sk-your-openai-api-key-here
```

**How to generate a secure KEY:**
```bash
openssl rand -base64 32
```

**Get OpenAI API Key:**
1. Go to https://platform.openai.com/api-keys
2. Create a new secret key
3. Copy it to your `.env` file

### Step 4: Understand the Services

#### RAG Service (`/rag-service`)

**Purpose:** AI-powered content generation using RAG (Retrieval-Augmented Generation)

**Features:**
- Generates course modules based on curriculum PDFs
- Generates lessons for modules
- Generates lesson content (HTML format)
- Generates lesson plans (structured PDF format)
- Generates interactive simulations
- Q&A over uploaded course materials

**How it works:**
1. You upload curriculum PDFs to Directus
2. RAG service extracts text and converts to vectors
3. Stores vectors in Qdrant
4. When generating content, it searches relevant curriculum sections
5. Sends context + OpenAI to generate high-quality, curriculum-aligned content

**Endpoints:**
- `POST /process-document` - Process uploaded PDF
- `POST /generate-modules` - Generate course modules
- `POST /generate-lessons` - Generate module lessons
- `POST /generate-lesson-content` - Generate lesson HTML
- `POST /generate-lesson-plan` - Generate structured lesson plan
- `POST /generate-simulation` - Generate interactive simulation
- `POST /query` - Ask questions about course materials

#### PDF Service (`/pdf-service`)

**Purpose:** Convert HTML lesson plans to professional PDFs

**Features:**
- Converts HTML to PDF using WeasyPrint
- Maintains formatting, tables, and structure
- Landscape A4 format optimized for lesson plans
- Automatic file management in Directus

**How it works:**
1. Lesson plan is created/updated in Directus
2. Flow triggers PDF generation
3. PDF service receives HTML content
4. Generates PDF and uploads to Directus
5. Returns new PDF URL

**Endpoints:**
- `POST /convert-to-pdf` - Create new PDF
- `POST /update-pdf` - Update existing PDF (deletes old, creates new)

### Step 5: Start All Services

```bash
# Start all containers
docker-compose up -d

# Check logs
docker-compose logs -f

# Or check individual service logs
docker logs directus-directus-1 -f
docker logs directus-rag-service-1 -f
docker logs directus-pdf-service-1 -f
```

**Wait for all services to be ready:**

```
✓ Directus: Server listening on 0.0.0.0:8055
✓ RAG: Embedding model loaded successfully
✓ PDF: FastAPI running on 0.0.0.0:8001
✓ Qdrant: Collection ready
```

This takes about 2-3 minutes on first start (downloads embedding model).

### Step 6: Access Directus

Open your browser:
```
http://localhost:8055
```

**Login credentials:**
- Email: (what you set in `.env` as `ADMIN_EMAIL`)
- Password: (what you set in `.env` as `ADMIN_PASSWORD`)

---

## Understanding the Pre-configured Database

The `postgres_data` folder contains a **complete LMS database** with:

### Collections (26 total):

**Core Learning Content:**
- `lms_courses` - Course information
- `lms_modules` - Course modules/sections
- `lms_lessons` - Individual lessons
- `Learning_paths` - Lesson plans with PDF links
- `lms_topics` - Course topics/categories
- `lms_tracks` - Learning tracks

**Assessments:**
- `quizz` - Quizzes linked to modules
- `question_bank` - Quiz questions
- `quizz_question_bank` - Junction table

**Interactive Content:**
- `lms_simulations` - Interactive demos
- `lms_assignement` - Assignments
- `lms_lessons_resources` - Downloadable resources

**User Management:**
- `lms_enrollments` - Student enrollments
- `lms_comments` - Lesson comments
- `lms_courses_reviews` - Course reviews
- `lms_instructors` - Instructor profiles

**Organization:**
- `Organization` - Organizations/schools
- `Lms_Portfolio` - Portfolio items
- `lms_settings` - System settings

**Junction Tables:**
- Multiple M2M relationship tables

### Pre-configured Flows (13 total):

**Content Generation Flows:**
1. **Generate modules for course** - Creates course modules from curriculum
2. **Generate lessons for module** - Creates lessons for a module
3. **Generate Content for lesson** - Generates lesson HTML content
4. **Generate lesson plan** - Creates structured lesson plan
5. **Generate_simulation** - Creates interactive simulations
6. **Generate assignments** - Creates assignments
7. **Generate description for course** - Generates course descriptions
8. **Create lessons** - Batch lesson creation
9. **Create assignments** - Batch assignment creation
10. **Create modules** - Batch module creation

**PDF Management Flows:**
11. **PDF LOOP** - Triggers PDF generation
12. **PDF Processing Flow** - Processes PDFs for RAG
13. **Update Lesson Plan PDF** - Updates lesson plan PDFs when content changes

These flows are **already configured** and will work immediately after setup.

---

## Verifying Your Setup

### 1. Check Service Health

```bash
# Check all containers are running
docker ps

# You should see 5 containers:
# - directus-directus-1
# - directus-postgres-1
# - qdrant
# - directus-rag-service-1
# - directus-pdf-service-1
```

### 2. Test RAG Service

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "qdrant_connected": true,
  "collections_count": 1
}
```

### 3. Test PDF Service

```bash
curl http://localhost:8001/health
```

Expected response:
```json
{
  "status": "healthy"
}
```

### 4. Check Directus Collections

1. Log into Directus admin panel
2. Click "Content" in sidebar
3. You should see all 26+ collections
4. Open `lms_courses` - the structure is ready
5. Go to Settings → Flows - you should see 13 active flows

### 5. Test Content Generation (Optional)

1. Create a new course in Directus
2. Upload a curriculum PDF to the course
3. Click the "Generate Modules" button (custom button in course detail)
4. Wait for modules to be generated (uses RAG + OpenAI)
5. Open a module and generate lessons
6. Open a lesson and generate content

**Note:** Content generation requires valid `OPENAI_API_KEY` in `.env`.

---

## Creating a Directus Static Token (for LibreChat MCP)

To connect LibreChat to your Directus instance:

### Step 1: Log into Directus Admin

```
http://localhost:8055
```

### Step 2: Create a Static Token

1. Go to **Settings** (gear icon in sidebar)
2. Click **Access Tokens** under "Project Settings"
3. Click **"+"** (Create Token)
4. Configure:
   - **Name:** LibreChat MCP Token
   - **Token:** (auto-generated, copy this!)
   - **Role:** Admin (or create custom role with read permissions)
   - **Expires:** Never (or set expiration)
5. Click **Save**
6. **Copy the token immediately** - you won't see it again!

### Step 3: Test the Token

```bash
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  http://localhost:8055/items/lms_courses
```

You should see a JSON response with courses data.

### Step 4: Use in LibreChat

Add to LibreChat's `.env`:
```env
DIRECTUS_URL=http://YOUR_SERVER_IP:8055
DIRECTUS_TOKEN=your_static_token_here
```

Or if running on same machine:
```env
DIRECTUS_URL=http://host.docker.internal:8055
DIRECTUS_TOKEN=your_static_token_here
```

---

## Uploading Curriculum Files for RAG

To use the AI content generation features:

### Step 1: Prepare Your PDFs

Organize your curriculum documents:
- Course syllabus
- Lesson plans
- Teacher guides
- Textbook chapters
- Reference materials

**Supported formats:** PDF only

### Step 2: Upload to Directus

1. Go to **Content → lms_courses**
2. Open a course
3. Scroll to **"Curriculum File"** field
4. Click **"Choose File"** or drag and drop PDFs
5. Click **Save**

### Step 3: Process PDFs for RAG

The **"PDF Processing Flow"** automatically:
1. Detects new PDF upload
2. Sends PDF to RAG service
3. Extracts text from PDF
4. Splits into chunks
5. Generates embeddings (vectors)
6. Stores in Qdrant vector database

**Check processing logs:**
```bash
docker logs directus-rag-service-1 --tail 50
```

You should see:
```
📄 Processing: your-file.pdf
📖 Extracting text...
✂️ Chunking text...
🧮 Generating embeddings...
💾 Storing in Qdrant...
✅ Successfully processed: 127 chunks
```

### Step 4: Generate Content

Now when you generate modules/lessons/content, the AI will:
1. Search the vector database for relevant curriculum sections
2. Use those sections as context
3. Generate content that aligns with your curriculum

---

## Customizing Flows

All flows are in Directus → **Settings → Flows**.

### Example: Modify "Generate lesson plan" Flow

1. Go to Settings → Flows
2. Click **"Generate lesson plan"**
3. You'll see the flow diagram
4. Click any operation to edit
5. Common customizations:
   - Change OpenAI model (gpt-4, gpt-5, etc.)
   - Adjust prompts
   - Modify PDF formatting
   - Change trigger conditions

### Flow Structure Example:

```
Trigger: Action (Button Click)
    ↓
Operation 1: Read Item (Get lesson data)
    ↓
Operation 2: Webhook (Call RAG service /generate-lesson-plan)
    ↓
Operation 3: Update Item (Save generated content)
    ↓
Operation 4: Webhook (Call PDF service /convert-to-pdf)
    ↓
Operation 5: Update Item (Save PDF URL)
```

---

## Troubleshooting

### RAG Service Issues

**Problem:** "Embedding model not loading"

```bash
docker logs directus-rag-service-1
```

**Solution:**
```bash
# Restart the service
docker-compose restart rag-service

# Or rebuild if needed
docker-compose build --no-cache rag-service
docker-compose up -d
```

**Problem:** "No relevant sources found when generating content"

**Solution:**
1. Check PDFs are uploaded and processed
2. Verify Qdrant has documents:
   ```bash
   curl http://localhost:6333/collections/documents
   ```
3. Check RAG logs for processing errors

### PDF Service Issues

**Problem:** "PDF generation fails"

**Solution:**
```bash
docker logs directus-pdf-service-1

# Check if WeasyPrint dependencies are installed
docker exec directus-pdf-service apt list --installed | grep libpango
```

### Database Issues

**Problem:** "Directus can't connect to database"

**Solution:**
```bash
# Check postgres is running
docker logs directus-postgres-1

# Verify credentials in .env match
cat .env | grep DB_

# Restart postgres
docker-compose restart postgres
```

### Extension Issues

**Problem:** "Custom buttons/interfaces not showing"

**Solution:**
1. Check extensions folder is mounted:
   ```bash
   docker exec directus-directus-1 ls /directus/extensions
   ```
2. Restart Directus:
   ```bash
   docker-compose restart directus
   ```

### Port Conflicts

**Problem:** "Port already in use"

**Solution:**
```bash
# Find what's using the port
sudo lsof -i :8055  # Directus
sudo lsof -i :5432  # Postgres
sudo lsof -i :6333  # Qdrant
sudo lsof -i :8000  # RAG service
sudo lsof -i :8001  # PDF service

# Change ports in docker-compose.yml if needed
```

---

## Updating Directus

To update to a newer version:

```bash
# Stop services
docker-compose down

# Pull latest image
docker-compose pull directus

# Start services
docker-compose up -d
```

**Your data is safe** - it's stored in volumes (`postgres_data`, `uploads`, `extensions`).

---

## Backup Strategy

### What to Backup:

1. **postgres_data/** - Complete database
2. **uploads/** - All uploaded files
3. **extensions/** - Custom extensions
4. **.env** - Configuration (keep secure!)

### Quick Backup:

```bash
# Create backup folder
mkdir backup_$(date +%Y%m%d)

# Copy important directories
cp -r postgres_data backup_$(date +%Y%m%d)/
cp -r uploads backup_$(date +%Y%m%d)/
cp -r extensions backup_$(date +%Y%m%d)/
cp .env backup_$(date +%Y%m%d)/.env.backup

# Create archive
tar -czf directus_backup_$(date +%Y%m%d).tar.gz backup_$(date +%Y%m%d)/
```

### Restore from Backup:

```bash
# Stop services
docker-compose down

# Extract backup
tar -xzf directus_backup_20241201.tar.gz

# Replace data
rm -rf postgres_data uploads extensions
cp -r backup_20241201/postgres_data .
cp -r backup_20241201/uploads .
cp -r backup_20241201/extensions .

# Start services
docker-compose up -d
```

---

## Production Deployment

### Security Checklist:

- [ ] Change all default passwords
- [ ] Generate secure random `KEY` in `.env`
- [ ] Use strong database password
- [ ] Enable HTTPS (use nginx reverse proxy)
- [ ] Restrict Directus to private network
- [ ] Set up firewall rules
- [ ] Enable rate limiting
- [ ] Regular backups
- [ ] Monitor logs
- [ ] Update Docker images regularly

### Recommended nginx Configuration:

```nginx
server {
    listen 443 ssl;
    server_name lms.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8055;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Resources

- **Directus Documentation:** https://docs.directus.io
- **OpenAI API:** https://platform.openai.com/docs
- **Qdrant Documentation:** https://qdrant.tech/documentation
- **WeasyPrint Documentation:** https://doc.courtbouillon.org/weasyprint

---

## Support

For issues specific to this setup:
1. Check logs: `docker-compose logs -f`
2. Verify environment variables: `cat .env`
3. Check service health endpoints
4. Review flow configurations in Directus

**Your Directus instance is now ready!** Access it at `http://localhost:8055` and start building your LMS content. 🚀