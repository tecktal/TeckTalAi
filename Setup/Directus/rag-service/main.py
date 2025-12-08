import os
# Setup cache location
os.environ['HF_HOME'] = '/root/.cache/huggingface'
os.environ['TRANSFORMERS_CACHE'] = '/root/.cache/huggingface'

# Only use offline mode if explicitly requested
if os.getenv('OFFLINE_MODE', 'false').lower() == 'true':
    os.environ['HF_DATASETS_OFFLINE'] = '1'
    os.environ['TRANSFORMERS_OFFLINE'] = '1'
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
import uuid
# PDF processing
import PyPDF2
from sentence_transformers import SentenceTransformer
import json

# Vector database
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from qdrant_client.http import models

# OpenAI
from openai import OpenAI
import httpx

# Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI(title="RAG Service")

# Configuration
QDRANT_HOST = os.getenv("QDRANT_HOST", "qdrant")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
COLLECTION_NAME = "documents"
UPLOADS_PATH = "/app/uploads"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Initialize clients
qdrant_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
embedding_model = None  # Don't load yet!
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Data models
class DocumentUpload(BaseModel):
    file_id: str
    filename: str
    course_id: str
    file_path: str

class QueryRequest(BaseModel):
    query: str
    course_id: Optional[str] = None
    limit: int = 5

# Startup: Create Qdrant collection
@app.on_event("startup")
async def startup_event():
    global embedding_model

    try:
        # Load the embedding model during startup
        logger.info("Loading embedding model from cache...")
        embedding_model = SentenceTransformer("all-MiniLM-L6-v2", cache_folder='/root/.cache/huggingface')
        logger.info("✅ Embedding model loaded successfully")

        collections = qdrant_client.get_collections().collections
        collection_names = [col.name for col in collections]

        if COLLECTION_NAME not in collection_names:
            logger.info(f"Creating collection: {COLLECTION_NAME}")
            qdrant_client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )
        logger.info("✅ Qdrant collection ready")
    except Exception as e:
        logger.error(f"❌ Startup error: {e}")
        raise  # Fail startup if model can't load


# Utility functions
def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF"""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Split text into chunks"""
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        # Try to end at sentence boundary
        if end < len(text):
            last_period = chunk.rfind('.')
            if last_period > start + chunk_size // 2:
                chunk = text[start:start + last_period + 1]
                end = start + last_period + 1

        chunks.append(chunk.strip())
        start = end - overlap

        if start >= len(text):
            break

    return [chunk for chunk in chunks if chunk.strip()]

def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """Convert text chunks to vectors"""
    embeddings = embedding_model.encode(texts)
    return embeddings.tolist()

# API Endpoints
@app.get("/health")
async def health_check():
    """Check if service is healthy"""
    try:
        collections = qdrant_client.get_collections()
        return {
            "status": "healthy",
            "qdrant_connected": True,
            "collections_count": len(collections.collections)
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.post("/process-document")
async def process_document(document: DocumentUpload, background_tasks: BackgroundTasks):
    """Process uploaded PDF document"""
    logger.info(f"📄 Processing: {document.filename}")
    background_tasks.add_task(process_document_task, document)
    return {"message": "Document processing started", "filename": document.filename}

async def process_document_task(document: DocumentUpload):
    """Background task to process document"""
    try:
        file_path = os.path.join(UPLOADS_PATH, document.file_path.lstrip('/'))

        if not os.path.exists(file_path):
            logger.error(f"❌ File not found: {file_path}")
            return

        # Step 1: Extract text from PDF
        logger.info("📖 Extracting text...")
        text = extract_text_from_pdf(file_path)

        # Step 2: Split into chunks
        logger.info("✂️ Chunking text...")
        chunks = chunk_text(text)
        logger.info(f"Created {len(chunks)} chunks")

        # Step 3: Generate embeddings (convert to vectors)
        logger.info("🧮 Generating embeddings...")
        embeddings = generate_embeddings(chunks)

        # Step 4: Store in vector database
        logger.info("💾 Storing in Qdrant...")
        points = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "text": chunk,
                    "filename": document.filename,
                    "course_id": document.course_id,
                    "file_id": document.file_id,
                    "chunk_index": i
                }
            )
            points.append(point)

        qdrant_client.upsert(collection_name=COLLECTION_NAME, points=points)
        logger.info(f"✅ Successfully processed {document.filename}: {len(chunks)} chunks")

    except Exception as e:
        logger.error(f"❌ Error processing {document.filename}: {e}")

@app.post("/query")
async def query_documents(request: QueryRequest):
    """Answer questions using RAG"""
    logger.info(f"❓ Query: {request.query}")

    try:
        # Step 1: Convert question to vector
        query_embedding = embedding_model.encode([request.query])[0].tolist()

        # Step 2: Search for similar content
        query_filter = None
        if request.course_id:
            query_filter = Filter(
                must=[FieldCondition(key="course_id", match=MatchValue(value=request.course_id))]
            )

        search_results = qdrant_client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_embedding,
            query_filter=query_filter,
            limit=request.limit
        )

        if not search_results:
            return {
                "answer": "I couldn't find any relevant documents to answer your question.",
                "sources": [],
                "query": request.query
            }

        # Step 3: Prepare context for OpenAI
        context = "\n\n".join([
            f"Document: {hit.payload['filename']}\n{hit.payload['text'][:500]}..."
            for hit in search_results[:3]
        ])

        # Step 4: Generate answer using OpenAI
        prompt = f"""Based on the following documents, answer the question. If you can't find the answer in the documents, say so.

Documents:
{context}

Question: {request.query}

Answer:"""

        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Answer questions based on provided documents. Be accurate and cite sources."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )

        answer = response.choices[0].message.content

        # Prepare sources
        sources = []
        for hit in search_results:
            sources.append({
                "filename": hit.payload["filename"],
                "score": round(hit.score, 3),
                "course_id": hit.payload["course_id"],
                "preview": hit.payload["text"][:200] + "..."
            })

        return {
            "answer": answer,
            "sources": sources,
            "query": request.query
        }

    except Exception as e:
        logger.error(f"❌ Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-modules")
async def generate_modules(request: dict):
    """Generate course modules using RAG + OpenAI"""

    course_title = request.get("course_title")
    course_id = request.get("course_id")
    context = request.get("context", "")
    language = request.get("language", "English")

    logger.info(f"🎯 MODULE GENERATION REQUEST:")
    logger.info(f"   Course Title: {course_title}")
    logger.info(f"   Course ID: {course_id}")
    logger.info(f"   Language: {language}")
    logger.info(f"   Context: {context}")

    # Step 1: Search for relevant content in the RAG database
    rag_context = ""
    rag_used = False
    if course_id:
        try:
            search_query = f"course modules lessons chapters topics {course_title}"
            logger.info(f"🔍 RAG SEARCH:")
            logger.info(f"   Search Query: {search_query}")

            search_results = qdrant_client.search(
                collection_name=COLLECTION_NAME,
                query_vector=embedding_model.encode(search_query).tolist(),
                query_filter=Filter(
                    must=[FieldCondition(key="course_id", match=MatchValue(value=course_id))]
                ),
                limit=8
            )

            logger.info(f"   Found {len(search_results)} search results")

            if search_results:
                logger.info("📄 RAG SOURCES FOUND:")
                for i, hit in enumerate(search_results):
                    logger.info(f"   Source {i+1}:")
                    logger.info(f"     Filename: {hit.payload['filename']}")
                    logger.info(f"     Score: {hit.score:.3f}")
                    logger.info(f"     Preview: {hit.payload['text'][:100]}...")

                # Filter by score and extract relevant chunks
                rag_chunks = [hit.payload["text"] for hit in search_results if hit.score > 0.4]
                filtered_count = len(rag_chunks)

                logger.info(f"   Filtered to {filtered_count} chunks (score > 0.4)")

                if rag_chunks:
                    rag_context = "\n\nRELEVANT COURSE MATERIALS:\n" + "\n\n".join(rag_chunks[:5])
                    rag_used = True
                    logger.info(f"✅ RAG CONTEXT CREATED: {len(rag_context)} characters")
                else:
                    logger.info("❌ No high-quality chunks found (all scores < 0.4)")
            else:
                logger.info("❌ No search results found")

        except Exception as e:
            logger.error(f"❌ RAG SEARCH ERROR: {e}")

    # Step 2: Create enhanced prompt with RAG context
    system_prompt = """You are a course content assistant.

PRIORITY: If course materials are provided below, base your modules on that content first.
If no relevant materials are found, use your general knowledge.

Generate modules that are practical and educational."""

    user_prompt = f"""Generate module titles and descriptions for a course titled: "{course_title}" title should be like "Module [number] [Module title]".

Return only a JSON array where each item has a "title" and a "description" field and a "course" field that has this value : {course_id}. Do not include any extra commentary or explanation. Format the response strictly as JSON.

here is some extra context: {context}

{rag_context}

GENERATE THIS IN THIS LANGUAGE: {language}. YOU MUST GENERATE ALL TEXT, LABELS, DESCRIPTIONS, AND EDUCATIONAL CONTENT IN THIS LANGUAGE."""

    logger.info(f"🤖 OPENAI REQUEST:")
    logger.info(f"   Model: gpt-4")
    logger.info(f"   RAG Context Length: {len(rag_context)} chars")
    logger.info(f"   Using RAG: {rag_used}")

    # Step 3: Call OpenAI with enhanced context
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )

        result = response.choices[0].message.content

        logger.info(f"✅ OPENAI RESPONSE:")
        logger.info(f"   Tokens Used: {response.usage.total_tokens}")
        logger.info(f"   Response Length: {len(result)} characters")
        logger.info(f"   Content Preview: {result[:200]}...")

        # Log final summary
        logger.info(f"🎉 MODULE GENERATION COMPLETE:")
        logger.info(f"   Course: {course_title}")
        logger.info(f"   RAG Enhanced: {rag_used}")
        logger.info(f"   Sources Used: {len(search_results) if 'search_results' in locals() else 0}")

        return result

    except Exception as e:
        logger.error(f"❌ OPENAI ERROR: {e}")
        return {"error": str(e)}


@app.post("/generate-lessons")
async def generate_lessons(request: dict):
    """Generate numbered lesson titles and slugs using RAG + OpenAI"""

    module_title = request.get("module_title")
    module_id = request.get("module_id")
    course_id = request.get("course_id")
    context = request.get("context", "")
    language = request.get("language", "English")

    logger.info(f"📚 LESSON GENERATION REQUEST:")
    logger.info(f"   Module Title: {module_title}")
    logger.info(f"   Module ID: {module_id}")
    logger.info(f"   Course ID: {course_id}")
    logger.info(f"   Language: {language}")
    logger.info(f"   Context: {context}")

    # Step 1: Search for relevant content in the RAG database using course_id
    rag_context = ""
    rag_used = False
    if course_id:
        try:
            search_query = f"lessons topics {module_title} content outline"
            logger.info(f"🔍 RAG SEARCH FOR LESSONS:")
            logger.info(f"   Search Query: {search_query}")
            logger.info(f"   Target Course: {course_id}")

            search_results = qdrant_client.search(
                collection_name=COLLECTION_NAME,
                query_vector=embedding_model.encode(search_query).tolist(),
                query_filter=Filter(
                    must=[FieldCondition(key="course_id", match=MatchValue(value=course_id))]
                ),
                limit=8
            )

            logger.info(f"   Found {len(search_results)} search results")

            if search_results:
                logger.info("📖 RAG SOURCES FOR LESSONS:")
                for i, hit in enumerate(search_results):
                    logger.info(f"   Source {i+1}:")
                    logger.info(f"     Filename: {hit.payload['filename']}")
                    logger.info(f"     Score: {hit.score:.3f}")
                    logger.info(f"     Chunk Index: {hit.payload.get('chunk_index', 'N/A')}")
                    logger.info(f"     Preview: {hit.payload['text'][:150]}...")

                # Extract relevant text chunks
                rag_chunks = [hit.payload["text"] for hit in search_results if hit.score > 0.4]
                filtered_count = len(rag_chunks)

                logger.info(f"   Filtered to {filtered_count} chunks (score > 0.4)")

                if rag_chunks:
                    rag_context = f"\n\nRELEVANT COURSE MATERIALS FOR '{module_title}':\n" + "\n\n".join(rag_chunks[:5])
                    rag_used = True
                    logger.info(f"✅ LESSON RAG CONTEXT CREATED: {len(rag_context)} characters")
                else:
                    logger.info("❌ No high-quality lesson chunks found (all scores < 0.4)")
            else:
                logger.info("❌ No lesson search results found")

        except Exception as e:
            logger.error(f"❌ LESSON RAG SEARCH ERROR: {e}")

    # Step 2: Create enhanced prompt with RAG context
    system_content = "You are a course content assistant."

    user_content = f"""Generate numbered (lesson 1, lesson 2, ...) lesson titles and slugs for the module titled: "{module_title}". The lesson title should be clear and engaging, and the slug should be a URL-friendly version of the title. Return only a JSON array where each item has a "title", "slug", and "module" field that has this value: {module_id}. Do not include any extra commentary or explanation. Format the response strictly as JSON.

here is some extra context: {context}

{rag_context}

GENERATE THIS IN THIS LANGUAGE: {language}. YOU MUST GENERATE ALL TEXT, LABELS, DESCRIPTIONS, AND EDUCATIONAL CONTENT IN THIS LANGUAGE."""

    logger.info(f"🤖 OPENAI REQUEST FOR LESSONS:")
    logger.info(f"   Model: gpt-4")
    logger.info(f"   Module: {module_title}")
    logger.info(f"   RAG Context Length: {len(rag_context)} chars")
    logger.info(f"   Using RAG: {rag_used}")

    # Step 3: Call OpenAI with enhanced context
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content}
            ],
            temperature=0.7
        )

        result = response.choices[0].message.content

        logger.info(f"✅ LESSON OPENAI RESPONSE:")
        logger.info(f"   Tokens Used: {response.usage.total_tokens}")
        logger.info(f"   Response Length: {len(result)} characters")
        logger.info(f"   Content Preview: {result[:200]}...")

        # Log final summary
        logger.info(f"🎉 LESSON GENERATION COMPLETE:")
        logger.info(f"   Module: {module_title}")
        logger.info(f"   RAG Enhanced: {rag_used}")
        logger.info(f"   Sources Used: {len(search_results) if 'search_results' in locals() else 0}")

        return result

    except Exception as e:
        logger.error(f"❌ LESSON OPENAI ERROR: {e}")
        return {"error": str(e)}


@app.post("/generate-lesson-content")
async def generate_lesson_content(request: dict):
    """Generate detailed lesson content using RAG + OpenAI"""

    # Extract request parameters
    lesson_title = request.get("lesson_title")
    lesson_id = request.get("lesson_id")
    module_title = request.get("module_title")
    module_description = request.get("module_description")
    course_title = request.get("course_title")
    course_description = request.get("course_description")
    other_modules_raw = request.get("other_modules", [])
    module_lessons_raw = request.get("module_lessons", [])  # NEW: All lessons in this module
    course_id = request.get("course_id")
    context = request.get("context", "")
    language = request.get("language", "English")

    # Handle other_modules - it might come as a string or list
    other_modules = []
    if isinstance(other_modules_raw, str):
        try:
            import json
            other_modules = json.loads(other_modules_raw)
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse other_modules string: {other_modules_raw[:100]}...")
            other_modules = []
    elif isinstance(other_modules_raw, list):
        other_modules = other_modules_raw

    # Handle module_lessons - it might come as a string or list
    module_lessons = []
    if isinstance(module_lessons_raw, str):
        try:
            import json
            module_lessons = json.loads(module_lessons_raw)
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse module_lessons string: {module_lessons_raw[:100]}...")
            module_lessons = []
    elif isinstance(module_lessons_raw, list):
        module_lessons = module_lessons_raw

    logger.info(f"📝 LESSON CONTENT GENERATION REQUEST:")
    logger.info(f"   Lesson: {lesson_title}")
    logger.info(f"   Lesson ID: {lesson_id}")
    logger.info(f"   Module: {module_title}")
    logger.info(f"   Course: {course_title}")
    logger.info(f"   Course ID: {course_id}")
    logger.info(f"   Language: {language}")
    logger.info(f"   Other Modules Count: {len(other_modules)}")
    logger.info(f"   Module Lessons Count: {len(module_lessons)}")

    # Find current lesson position and next lesson
    current_lesson_index = -1
    next_lesson = None
    for i, lesson in enumerate(module_lessons):
        if lesson.get('id') == lesson_id or lesson.get('title') == lesson_title:
            current_lesson_index = i
            if i + 1 < len(module_lessons):
                next_lesson = module_lessons[i + 1]
            break

    logger.info(f"   Current Lesson Position: {current_lesson_index + 1}/{len(module_lessons)}")
    if next_lesson:
        logger.info(f"   Next Lesson: {next_lesson.get('title', 'Unknown')}")

    # Step 1: Search for relevant content in the RAG database
    rag_context = ""
    rag_used = False
    if course_id:
        try:
            # Create comprehensive search query
            search_query = f"{lesson_title} {module_title} content explanation examples exercises"
            logger.info(f"🔍 RAG SEARCH FOR LESSON CONTENT:")
            logger.info(f"   Search Query: {search_query}")
            logger.info(f"   Target Course: {course_id}")

            search_results = qdrant_client.search(
                collection_name=COLLECTION_NAME,
                query_vector=embedding_model.encode(search_query).tolist(),
                query_filter=Filter(
                    must=[FieldCondition(key="course_id", match=MatchValue(value=course_id))]
                ),
                limit=10  # More results for detailed content
            )

            logger.info(f"   Found {len(search_results)} search results")

            if search_results:
                logger.info("📚 RAG SOURCES FOR LESSON CONTENT:")
                for i, hit in enumerate(search_results):
                    logger.info(f"   Source {i+1}:")
                    logger.info(f"     Filename: {hit.payload['filename']}")
                    logger.info(f"     Score: {hit.score:.3f}")
                    logger.info(f"     Chunk Index: {hit.payload.get('chunk_index', 'N/A')}")
                    logger.info(f"     Preview: {hit.payload['text'][:200]}...")

                # Extract relevant text chunks with lower threshold for content generation
                rag_chunks = [hit.payload["text"] for hit in search_results if hit.score > 0.3]
                filtered_count = len(rag_chunks)

                logger.info(f"   Filtered to {filtered_count} chunks (score > 0.3)")

                if rag_chunks:
                    rag_context = f"\n\nRELEVANT CURRICULUM MATERIALS:\n" + "\n\n".join(rag_chunks[:7])
                    rag_used = True
                    logger.info(f"✅ LESSON CONTENT RAG CONTEXT CREATED: {len(rag_context)} characters")
                else:
                    logger.info("❌ No relevant content chunks found")
            else:
                logger.info("❌ No search results found for lesson content")

        except Exception as e:
            logger.error(f"❌ LESSON CONTENT RAG SEARCH ERROR: {e}")

    # Step 2: Prepare course context
    course_context = f"""
COURSE INFORMATION:
Title: {course_title}
Description: {course_description}

CURRENT MODULE:
Title: {module_title}
Description: {module_description}

OTHER MODULES IN COURSE:
{chr(10).join([f"- {mod}" for mod in other_modules]) if other_modules else "- No other modules provided"}

CURRENT LESSON:
Title: {lesson_title}
"""

    # Step 3: Create enhanced prompt for HTML content
    system_prompt = f"""You are an expert educational content creator and HTML writer.

Your task is to create comprehensive, engaging lesson content in HTML format that:
1. Uses heading tags starting from H2 (no H1 tags allowed)
2. Aligns with the course objectives and module goals
3. Uses the provided curriculum materials as the primary source
4. Includes practical examples, exercises, and clear explanations
5. Formats mathematical expressions with $ $ for LaTeX rendering
6. Returns ONLY HTML content without code block formatting

IMPORTANT:
- Base content primarily on curriculum materials provided
- Mathematical formulas must use $formula$ format and be OUTSIDE HTML tags
- Return only HTML content, no ```html prefix
- Structure content with proper sections using HTML tags"""

    user_prompt = f"""Create detailed lesson content for: "{lesson_title}"

{course_context}

Additional Context: {context}

{rag_context}

Generate comprehensive lesson content in HTML format. Follow these requirements:
1. Use heading tags starting from H2 (no H1)
2. Structure the content with proper sections
3. Include practical examples and clear explanations
4. Add exercises or practice problems when appropriate
5. For mathematical formulas, wrap them with $ and $ like: $x + 3 = 7$
6. Mathematical expressions must be OUTSIDE of HTML tags
7. Use proper HTML structure with sections, paragraphs, lists, etc.
8. Make the content engaging and educational

Return ONLY the HTML content without ```html prefix or any other formatting.

LANGUAGE: Generate ALL content in {language}. Ensure all text, labels, descriptions, and educational content are in this language."""

    logger.info(f"🤖 OPENAI REQUEST FOR LESSON CONTENT:")
    logger.info(f"   Model: gpt-4")
    logger.info(f"   Lesson: {lesson_title}")
    logger.info(f"   RAG Context Length: {len(rag_context)} chars")
    logger.info(f"   Using RAG: {rag_used}")
    logger.info(f"   Course Context Length: {len(course_context)} chars")

    # Step 4: Call OpenAI
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=3000  # Increased for detailed content
        )

        result = response.choices[0].message.content

        logger.info(f"✅ LESSON CONTENT OPENAI RESPONSE:")
        logger.info(f"   Tokens Used: {response.usage.total_tokens}")
        logger.info(f"   Response Length: {len(result)} characters")
        logger.info(f"   Content Preview: {result[:300]}...")

        # Log final summary
        logger.info(f"🎉 LESSON CONTENT GENERATION COMPLETE:")
        logger.info(f"   Lesson: {lesson_title}")
        logger.info(f"   Module: {module_title}")
        logger.info(f"   Course: {course_title}")
        logger.info(f"   RAG Enhanced: {rag_used}")
        logger.info(f"   Sources Used: {len(search_results) if 'search_results' in locals() else 0}")

        return result

    except Exception as e:
        logger.error(f"❌ LESSON CONTENT OPENAI ERROR: {e}")
        return {"error": str(e)}


@app.post("/generate-simulation")
async def generate_simulation(request: dict):
    """Generate interactive educational simulation using RAG + OpenAI"""

    lesson_id = request.get("lesson_id")
    lesson_content = request.get("lesson_content")  # Plain text of lesson
    simulation_prompt = request.get("simulation_prompt")  # What user wants to visualize
    course_id = request.get("course_id")
    language = request.get("language", "English")

    logger.info(f"🎮 SIMULATION GENERATION REQUEST:")
    logger.info(f"   Lesson ID: {lesson_id}")
    logger.info(f"   Prompt: {simulation_prompt}")
    logger.info(f"   Course ID: {course_id}")
    logger.info(f"   Language: {language}")

    # Step 1: Get RAG context for the concept
    rag_context = ""
    if course_id and simulation_prompt:
        try:
            search_query = f"{simulation_prompt} visualization example explanation"
            logger.info(f"🔍 RAG SEARCH FOR SIMULATION:")
            logger.info(f"   Query: {search_query}")

            search_results = qdrant_client.search(
                collection_name=COLLECTION_NAME,
                query_vector=embedding_model.encode(search_query).tolist(),
                query_filter=Filter(
                    must=[FieldCondition(key="course_id", match=MatchValue(value=course_id))]
                ),
                limit=5
            )

            if search_results:
                logger.info(f"📚 Found {len(search_results)} relevant sources")
                rag_chunks = [hit.payload["text"] for hit in search_results if hit.score > 0.3]
                if rag_chunks:
                    rag_context = "\n\nRELEVANT CURRICULUM CONTENT:\n" + "\n\n".join(rag_chunks[:3])
                    logger.info(f"✅ RAG context: {len(rag_context)} chars")
        except Exception as e:
            logger.error(f"❌ RAG search error: {e}")

    # Step 2: Create creative prompt for engaging simulations
    system_prompt = """You are a creative educational technology expert who designs engaging, interactive learning experiences.

YOUR MISSION: Create innovative, visually appealing simulations that make complex concepts intuitive and fun to explore.

CORE PRINCIPLES:
1. CREATIVITY FIRST: Think outside the box - use animations, colors, visual metaphors, interactive elements
2. EDUCATIONAL VALUE: The simulation must clearly demonstrate the concept in an engaging way
3. INTERACTIVITY: Users should be able to manipulate parameters and see immediate visual feedback
4. PROFESSIONAL BRANDING: Always include "TeckTal AI" branding
5. WORKING CODE: Everything must function perfectly on first load"""

    user_prompt = f"""Design an innovative interactive simulation to teach this concept.

LESSON ID: {lesson_id}

WHAT TO VISUALIZE: {simulation_prompt}

LESSON CONTENT:
{lesson_content[:1500]}

{rag_context}

CREATIVE FREEDOM:
- Choose ANY visualization approach that best explains the concept (canvas animations, SVG graphics, HTML/CSS effects, charts, games, etc.)
- Use creative color schemes, animations, and visual effects
- Add as many interactive controls as needed (sliders, buttons, dropdowns, input fields, etc.)
- Include explanatory text, labels, or tooltips that help users understand what they're seeing
- Make it visually appealing and engaging - this should WOW the learner!

REQUIRED BRANDING (MUST INCLUDE):
- A header or footer with "TeckTal AI" prominently displayed
- Use a clean, modern design aesthetic
- Professional color scheme (you can be creative but keep it polished)

TECHNICAL REQUIREMENTS:
- Single self-contained HTML file with embedded CSS and JavaScript
- Use Tailwind CDN for styling: <script src="https://cdn.tailwindcss.com"></script>
- Can use Canvas API, SVG, Chart.js (from CDN), or any standard web APIs
- All code must work immediately without external dependencies (except Tailwind CDN)
- Responsive design that works on different screen sizes

OUTPUT FORMAT:
Return ONLY a valid JSON object with these fields:
{{
  "lesson": "{lesson_id}",
  "title": "Creative title for the simulation",
  "slug": "url-friendly-slug",
  "description": "Brief description of what users will learn and interact with",
  "code": "Complete HTML code here"
}}

INSPIRATION EXAMPLES:
- For math: Interactive graphs with draggable points, animated function transformations
- For physics: Particle simulations, force vectors, collision demonstrations
- For chemistry: Molecule builders, reaction visualizations
- For programming: Code execution visualizers, algorithm animations
- For statistics: Interactive charts, probability simulators, data manipulation tools

LANGUAGE: Generate all text, labels, and descriptions in {language}.

Be bold, be creative, and create something that makes learning exciting! Return ONLY the JSON object - no markdown, no code fences, no extra text."""

    logger.info(f"🤖 CALLING OPENAI FOR SIMULATION")

    try:
        headers = {
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
            "Content-Type": "application/json"
        }

        # For GPT-5/o1 models: combine prompts and be very explicit about output format
        combined_prompt = f"""{system_prompt}

---

{user_prompt}

CRITICAL: You MUST return valid JSON. Do not just think about it - actually output the JSON structure with all fields filled in."""

        payload = {
            "model": "gpt-5",
            "messages": [
                {"role": "user", "content": combined_prompt}
            ],
            "max_completion_tokens": 32000  # Increased to allow output after reasoning
        }

        logger.info(f"📤 Sending request to OpenAI...")
        resp = httpx.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers, timeout=400.0)
        resp.raise_for_status()
        data = resp.json()

        # Log full response for debugging
        logger.info(f"📥 OpenAI Response: {json.dumps(data, indent=2)[:2000]}")

        # Extract content
        result = ""
        if data.get("choices") and len(data["choices"]) > 0:
            choice = data["choices"][0]
            message = choice.get("message", {})
            result = message.get("content", "")

        # Check usage details
        usage = data.get("usage", {})
        completion_details = usage.get("completion_tokens_details", {})
        reasoning_tokens = completion_details.get("reasoning_tokens", 0)
        actual_output_tokens = usage.get("completion_tokens", 0) - reasoning_tokens

        logger.info("✅ SIMULATION RESPONSE:")
        logger.info(f"   Total tokens: {usage.get('total_tokens', 0)}")
        logger.info(f"   Reasoning tokens: {reasoning_tokens}")
        logger.info(f"   Output tokens: {actual_output_tokens}")
        logger.info(f"   Content length: {len(result)} chars")

        if not result or len(result) < 50:
            logger.error(f"❌ Empty or too short response!")
            logger.error(f"   Full response: {json.dumps(data, indent=2)}")
            return {
                "error": "Model produced no usable output. All tokens used for reasoning.",
                "debug": {
                    "reasoning_tokens": reasoning_tokens,
                    "output_tokens": actual_output_tokens,
                    "content": result
                }
            }

        logger.info(f"   Content preview: {result[:300]}...")
        return result

    except httpx.HTTPStatusError as e:
        logger.error(f"❌ OPENAI HTTP ERROR: {e.response.status_code} - {e.response.text}")
        return {"error": f"HTTP {e.response.status_code}: {e.response.text}"}
    except Exception as e:
        logger.error(f"❌ SIMULATION ERROR: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return {"error": str(e)}


@app.post("/generate-lesson-plan")
async def generate_lesson_plan(request: dict):
    """Generate structured lesson plan using PDF template format with RAG + OpenAI"""

    lesson_id = request.get("lesson_id")
    lesson_title = request.get("lesson_title")
    lesson_content = request.get("lesson_content")
    module_title = request.get("module_title")
    course_title = request.get("course_title")
    course_id = request.get("course_id")
    language = request.get("language", "English")

    # Optional metadata from request
    teacher_name = request.get("teacher_name", "")
    school_name = request.get("school_name", "")
    grade_section = request.get("grade_section", "")
    subject = request.get("subject", "")

    logger.info(f"📋 LESSON PLAN GENERATION REQUEST:")
    logger.info(f"   Lesson ID: {lesson_id}")
    logger.info(f"   Lesson Title: {lesson_title}")
    logger.info(f"   Course ID: {course_id}")
    logger.info(f"   Language: {language}")

    # Step 1: Get RAG context for lesson planning
    rag_context = ""
    rag_sources = []
    if course_id and lesson_title:
        try:
            search_query = f"{lesson_title} {module_title} teaching pedagogy methods examples exercises"
            logger.info(f"🔍 RAG SEARCH FOR LESSON PLAN:")
            logger.info(f"   Query: {search_query}")

            search_results = qdrant_client.search(
                collection_name=COLLECTION_NAME,
                query_vector=embedding_model.encode(search_query).tolist(),
                query_filter=Filter(
                    must=[FieldCondition(key="course_id", match=MatchValue(value=course_id))]
                ),
                limit=12
            )

            if search_results:
                logger.info(f"📚 Found {len(search_results)} relevant sources")
                for i, hit in enumerate(search_results):
                    logger.info(f"   Source {i+1}:")
                    logger.info(f"     Filename: {hit.payload['filename']}")
                    logger.info(f"     Score: {hit.score:.3f}")
                    logger.info(f"     Preview: {hit.payload['text'][:150]}...")

                    # Store sources for citation
                    if hit.score > 0.25:
                        rag_sources.append({
                            "filename": hit.payload['filename'],
                            "score": hit.score,
                            "text": hit.payload['text']
                        })

                rag_chunks = [hit.payload["text"] for hit in search_results if hit.score > 0.25]

                if rag_chunks:
                    rag_context = "\n\nRELEVANT CURRICULUM MATERIALS AND TEACHING RESOURCES:\n" + "\n\n".join(rag_chunks[:8])
                    logger.info(f"✅ RAG context: {len(rag_context)} chars from {len(rag_chunks)} chunks")
                else:
                    logger.info("❌ No relevant chunks found")
        except Exception as e:
            logger.error(f"❌ RAG search error: {e}")

    # Step 2: Create prompt based on PDF template structure
    system_prompt = """You are an expert educator and curriculum designer. You MUST create a lesson plan that follows the EXACT format of the provided template.

CRITICAL: You must output a STRUCTURED TABLE FORMAT, not a flowing document. This is NOT negotiable.

MANDATORY OUTPUT FORMAT:

<h2>LESSON PLAN</h2>

<p><strong>Name of School:</strong> [School name or "To be specified"]</p>
<p><strong>Name of Teacher:</strong> [Teacher name or "To be specified"]</p>
<p><strong>Subject:</strong> [Subject]</p>
<p><strong>Grade and Section:</strong> [Grade]</p>
<p><strong>Topic of Lesson:</strong> [Exact lesson title]</p>
<p><strong>Unit of Lesson:</strong> [Unit/Module title]</p>
<p><strong>Sub-unit of Lesson:</strong> [Sub-unit if applicable]</p>
<p><strong>Date of Lesson:</strong> [Leave blank or current date]</p>

<h3>Rationale of the Topic</h3>
<p>[2-3 sentences explaining why this topic matters, real-world connections, and curriculum importance]</p>

<h3>Objectives</h3>
<p>[Single sentence starting with action verb, e.g., "Explain the historical development of..." or "Solve equations using..."]</p>

<h3>Lesson Activities</h3>

<table border="1" cellpadding="8" cellspacing="0" style="width:100%; border-collapse:collapse;">
  <tr>
    <th>Stage</th>
    <th>Time</th>
    <th>Learning Contents</th>
    <th>Teacher's Activities</th>
    <th>Student's Activities</th>
    <th>Assessment Activities</th>
  </tr>

  <tr>
    <td><strong>Starter Activities</strong></td>
    <td>8-10 min</td>
    <td>[Key question or focus for opening]</td>
    <td>[Specific actions teacher takes to start lesson]</td>
    <td>[What students do during starter]</td>
    <td>[Questions or checks to assess readiness]</td>
  </tr>

  <tr>
    <td><strong>Main Activities</strong></td>
    <td>25-30 min</td>
    <td>[Core concepts, skills, or activities]</td>
    <td>[Detailed teaching actions: explain, demonstrate, guide, provide materials, facilitate]</td>
    <td>[Student engagement: practice, discuss, solve, experiment, work in groups]</td>
    <td>[Formative assessment questions and observation points]</td>
  </tr>

  <tr>
    <td><strong>Concluding Activities</strong></td>
    <td>7-10 min</td>
    <td>[Summary, reflection, or synthesis]</td>
    <td>[Teacher wraps up, connects to next lesson]</td>
    <td>[Students summarize, reflect, or complete exit task]</td>
    <td>[Final check questions or exit ticket]</td>
  </tr>
</table>

<h3>Resources</h3>
<ul>
  <li>[List all materials, textbooks, manipulatives, technology needed]</li>
</ul>

<h3>Learner Support</h3>
<p>[Strategies for differentiation: support for slow learners, extensions for advanced students, accommodations for disabilities]</p>

STRICT RULES:
- Output ONLY this structure
- Do NOT add extra sections before or after
- Do NOT create multiple activities outside the table
- Keep each table cell CONCISE (2-4 sentences maximum per cell)
- The main activities row can be longer but should still fit in ONE table row
- Use simple HTML only: <h2>, <h3>, <p>, <ul>, <li>, <table>, <tr>, <td>, <th>, <strong>
- NO additional formatting, NO scripts, NO complex HTML"""

    user_prompt = f"""Create a lesson plan in the EXACT format shown above. Do not deviate from this structure.

COURSE INFORMATION:
- Course: {course_title}
- Module/Unit: {module_title}
- Lesson Title: {lesson_title}
- Subject: {subject if subject else course_title}
- Grade/Section: {grade_section if grade_section else "To be specified"}
- School: {school_name if school_name else "To be specified"}
- Teacher: {teacher_name if teacher_name else "To be specified"}

LESSON CONTENT:
{lesson_content[:3000]}

{rag_context}

INSTRUCTIONS:

1. **Use the curriculum materials provided** as your primary source for activities and content.

2. **Fill in the template EXACTLY as shown** in the system prompt above.

3. **For the table rows**, keep each cell CONCISE:
   - Learning Contents: 1-2 sentences describing the focus/question
   - Teacher's Activities: 2-4 bullet points or sentences of what teacher does
   - Student's Activities: 2-4 bullet points or sentences of what students do
   - Assessment Activities: 1-3 questions or observation points

4. **Structure the Main Activities** to include the core teaching, practice, and hands-on work. This can describe multiple activities within the one table row.

5. **Be specific and practical**:
   - Name actual activities (e.g., "Subdividing bread," "Dissolving sugar," "Chain analogy")
   - Include real questions to ask
   - Provide materials needed
   - Give expected answers

6. **Keep it simple**: This is a one-page teaching guide, not a comprehensive manual.

LANGUAGE: Generate ALL content in {language}.

OUTPUT THE COMPLETE LESSON PLAN NOW. Follow the template structure EXACTLY."""

    logger.info(f"🤖 CALLING OPENAI GPT-5 FOR STRUCTURED LESSON PLAN")

    try:
        headers = {
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
            "Content-Type": "application/json"
        }

        combined_prompt = f"""{system_prompt}

---

{user_prompt}"""

        payload = {
            "model": "gpt-5",
            "messages": [
                {"role": "user", "content": combined_prompt}
            ],
            "max_completion_tokens": 8000  # Shorter, focused lesson plan in table format
        }

        logger.info(f"📤 Sending request to OpenAI GPT-5...")
        resp = httpx.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers, timeout=400.0)
        resp.raise_for_status()
        data = resp.json()

        logger.info(f"📥 OpenAI Response received")

        result = ""
        if data.get("choices") and len(data["choices"]) > 0:
            choice = data["choices"][0]
            message = choice.get("message", {})
            result = message.get("content", "")

        usage = data.get("usage", {})
        completion_details = usage.get("completion_tokens_details", {})
        reasoning_tokens = completion_details.get("reasoning_tokens", 0)
        actual_output_tokens = usage.get("completion_tokens", 0) - reasoning_tokens

        logger.info(f"✅ LESSON PLAN RESPONSE:")
        logger.info(f"   Total tokens: {usage.get('total_tokens', 0)}")
        logger.info(f"   Reasoning tokens: {reasoning_tokens}")
        logger.info(f"   Output tokens: {actual_output_tokens}")
        logger.info(f"   Response Length: {len(result)} characters")
        logger.info(f"   RAG Sources Used: {len(rag_sources)}")

        if not result or len(result) < 50:
            logger.error(f"❌ Empty or too short response!")
            return {
                "error": "Model produced no usable output. All tokens used for reasoning.",
                "debug": {
                    "reasoning_tokens": reasoning_tokens,
                    "output_tokens": actual_output_tokens,
                    "content": result
                }
            }

        # Validate that the response contains the required table structure
        if "<table" not in result.lower():
            logger.warning(f"⚠️ Generated lesson plan missing table structure!")
            logger.warning(f"   The model may not have followed the template format.")

        if "starter activities" not in result.lower():
            logger.warning(f"⚠️ Missing 'Starter Activities' section")

        if "main activities" not in result.lower():
            logger.warning(f"⚠️ Missing 'Main Activities' section")

        logger.info(f"🎉 STRUCTURED LESSON PLAN GENERATION COMPLETE")

        return result

    except httpx.HTTPStatusError as e:
        logger.error(f"❌ OPENAI HTTP ERROR: {e.response.status_code} - {e.response.text}")
        return {"error": f"HTTP {e.response.status_code}: {e.response.text}"}
    except Exception as e:
        logger.error(f"❌ LESSON PLAN ERROR: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return {"error": str(e)}


@app.get("/documents/{course_id}")
async def get_course_documents(course_id: str):
    """Get all documents for a course"""
    try:
        results = qdrant_client.scroll(
            collection_name=COLLECTION_NAME,
            scroll_filter=Filter(
                must=[FieldCondition(key="course_id", match=MatchValue(value=course_id))]
            ),
            limit=100
        )

        documents = {}
        for point in results[0]:
            file_id = point.payload["file_id"]
            if file_id not in documents:
                documents[file_id] = {
                    "filename": point.payload["filename"],
                    "course_id": point.payload["course_id"],
                    "chunks_count": 0
                }
            documents[file_id]["chunks_count"] += 1

        return {
            "course_id": course_id,
            "documents": list(documents.values()),
            "total_documents": len(documents)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)