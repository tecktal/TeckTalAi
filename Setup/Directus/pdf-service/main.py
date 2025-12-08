from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from weasyprint import HTML, CSS
import os
import uuid
import json
import re
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configuration
UPLOADS_PATH = "/directus/uploads"
POSTGRES_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "postgres"),
    "database": os.getenv("POSTGRES_DB", "directus"),
    "user": os.getenv("POSTGRES_USER", "directus"),
    "password": os.getenv("POSTGRES_PASSWORD", "directus")
}

class HTMLContent(BaseModel):
    html: str
    filename: str = None
    orientation: str = "landscape"  # Add orientation option

    class Config:
        extra = 'ignore'

class UpdatePDFContent(BaseModel):
    file_id: str
    html: str
    filename: str = None
    orientation: str = "landscape"

    class Config:
        extra = 'ignore'

def get_db_connection():
    return psycopg2.connect(**POSTGRES_CONFIG)

def insert_file_record(file_id: str, filename: str, filesize: int):
    """Insert file record directly into Directus database"""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
        INSERT INTO directus_files (
            id,
            storage,
            filename_disk,
            filename_download,
            title,
            type,
            filesize,
            uploaded_on
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        """

        cursor.execute(query, (
            file_id,
            'local',
            filename,
            filename,
            filename.replace('.pdf', ''),
            'application/pdf',
            filesize,
            datetime.utcnow()
        ))

        conn.commit()
        result = cursor.fetchone()[0]
        return result

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def delete_file_record(file_id: str):
    """Delete file record from Directus database and return filename"""
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        # First, get the filename
        cursor.execute(
            "SELECT filename_disk FROM directus_files WHERE id = %s",
            (file_id,)
        )
        result = cursor.fetchone()

        if not result:
            return None

        filename = result['filename_disk']

        # Delete the record
        cursor.execute(
            "DELETE FROM directus_files WHERE id = %s",
            (file_id,)
        )

        conn.commit()
        return filename

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()


@app.post("/convert-to-pdf")
async def convert_html_to_pdf(request: Request):
    logger.info("=== Starting PDF conversion ===")

    try:
        body = await request.body()
        body_str = body.decode('utf-8')
        logger.debug(f"Received body length: {len(body_str)}")

        try:
            data = json.loads(body_str)
            if isinstance(data, str):
                data = json.loads(data)
        except json.JSONDecodeError as je:
            logger.warning(f"JSON decode error, attempting to clean: {je}")
            import re
            body_str = body_str.replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
            data = json.loads(body_str)
            if isinstance(data, str):
                data = json.loads(data)

        content = HTMLContent(**data)
        logger.info(f"Parsed content - filename: {content.filename}, orientation: {content.orientation}")
    except Exception as e:
        logger.error(f"Failed to parse request: {e}")
        raise HTTPException(status_code=422, detail=f"Invalid JSON format: {str(e)}")

    try:
        file_id = str(uuid.uuid4())
        logger.info(f"Generated file_id: {file_id}")

        if content.filename and content.filename != "undefined" and content.filename.strip():
            filename = f"{content.filename}.pdf"
        else:
            filename = f"lesson-plan-{datetime.now().strftime('%Y%m%d-%H%M%S')}.pdf"

        logger.info(f"Using filename: {filename}")

        pdf_path = os.path.join(UPLOADS_PATH, filename)
        os.makedirs(UPLOADS_PATH, exist_ok=True)
        logger.info(f"PDF path: {pdf_path}")

        # CSS for landscape orientation and proper table formatting
        css_string = '''
            @page {
                size: A4 landscape;
                margin: 0.5cm;
            }

            body {
                font-family: Arial, sans-serif;
                font-size: 9pt;
                line-height: 1.3;
            }

            table {
                width: 100%;
                border-collapse: collapse;
                font-size: 8pt;
            }

            tr {
                page-break-inside: avoid;
            }

            th, td {
                border: 1px solid #000;
                padding: 4px;
                vertical-align: top;
                text-align: left;
            }

            th {
                background-color: #f0f0f0;
                font-weight: bold;
            }

            h2 {
                font-size: 14pt;
                margin: 0.3em 0;
                text-align: center;
            }

            h3 {
                font-size: 11pt;
                margin: 0.5em 0 0.3em 0;
            }

            p {
                margin: 0.2em 0;
            }

            ul {
                margin: 0.2em 0;
                padding-left: 1.2em;
            }

            li {
                margin: 0.1em 0;
            }
        '''

        logger.info("Creating CSS object...")
        css_obj = CSS(string=css_string)
        logger.info("CSS object created successfully")

        logger.info("Creating HTML object...")
        html_obj = HTML(string=content.html)
        logger.info("HTML object created successfully")

        logger.info("Attempting to write PDF...")
        logger.info(f"write_pdf method signature: {html_obj.write_pdf.__doc__}")

        # Try the write_pdf call
        html_obj.write_pdf(pdf_path, stylesheets=[css_obj])
        logger.info("PDF written successfully!")

        filesize = os.path.getsize(pdf_path)
        logger.info(f"PDF filesize: {filesize} bytes")

        logger.info("Inserting file record into database...")
        insert_file_record(file_id, filename, filesize)
        logger.info("File record inserted successfully")

        result = {
            "success": True,
            "file_id": file_id,
            "filename": filename,
            "url": f"/assets/{file_id}",
            "filesize": filesize
        }
        logger.info(f"Returning result: {result}")
        return result

    except Exception as e:
        logger.error(f"ERROR in PDF conversion: {type(e).__name__}: {str(e)}")
        logger.exception("Full traceback:")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/update-pdf")
async def update_pdf(request: Request):
    """Delete existing PDF and create a new one with updated content"""
    logger.info("=== Starting PDF update ===")

    try:
        body = await request.body()
        body_str = body.decode('utf-8')
        logger.debug(f"Received body length: {len(body_str)}")

        try:
            data = json.loads(body_str)
            if isinstance(data, str):
                data = json.loads(data)
        except json.JSONDecodeError as je:
            logger.warning(f"JSON decode error, attempting to clean: {je}")
            body_str = body_str.replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
            data = json.loads(body_str)
            if isinstance(data, str):
                data = json.loads(data)

        content = UpdatePDFContent(**data)
        logger.info(f"Parsed content - file_id: {content.file_id}, filename: {content.filename}, orientation: {content.orientation}")
    except Exception as e:
        logger.error(f"Failed to parse request: {e}")
        raise HTTPException(status_code=422, detail=f"Invalid JSON format: {str(e)}")

    try:
        # Delete old file record and get filename
        logger.info(f"Deleting old file record for file_id: {content.file_id}")
        old_filename = delete_file_record(content.file_id)

        if old_filename:
            # Delete physical file
            old_pdf_path = os.path.join(UPLOADS_PATH, old_filename)
            if os.path.exists(old_pdf_path):
                os.remove(old_pdf_path)
                logger.info(f"Deleted old PDF file: {old_pdf_path}")
            else:
                logger.warning(f"Old PDF file not found: {old_pdf_path}")
        else:
            logger.warning(f"No existing file record found for file_id: {content.file_id}")

        # Generate new file_id
        new_file_id = str(uuid.uuid4())
        logger.info(f"Generated new file_id: {new_file_id}")

        # Determine filename
        if content.filename and content.filename != "undefined" and content.filename.strip():
            filename = f"{content.filename}.pdf"
        else:
            filename = f"lesson-plan-{datetime.now().strftime('%Y%m%d-%H%M%S')}.pdf"

        logger.info(f"Using filename: {filename}")

        pdf_path = os.path.join(UPLOADS_PATH, filename)
        os.makedirs(UPLOADS_PATH, exist_ok=True)
        logger.info(f"PDF path: {pdf_path}")

        # CSS for landscape orientation and proper table formatting
        css_string = '''
            @page {
                size: A4 landscape;
                margin: 0.5cm;
            }

            body {
                font-family: Arial, sans-serif;
                font-size: 9pt;
                line-height: 1.3;
            }

            table {
                width: 100%;
                border-collapse: collapse;
                font-size: 8pt;
            }

            tr {
                page-break-inside: avoid;
            }

            th, td {
                border: 1px solid #000;
                padding: 4px;
                vertical-align: top;
                text-align: left;
            }

            th {
                background-color: #f0f0f0;
                font-weight: bold;
            }

            h2 {
                font-size: 14pt;
                margin: 0.3em 0;
                text-align: center;
            }

            h3 {
                font-size: 11pt;
                margin: 0.5em 0 0.3em 0;
            }

            p {
                margin: 0.2em 0;
            }

            ul {
                margin: 0.2em 0;
                padding-left: 1.2em;
            }

            li {
                margin: 0.1em 0;
            }
        '''

        logger.info("Creating CSS object...")
        css_obj = CSS(string=css_string)
        logger.info("CSS object created successfully")

        logger.info("Creating HTML object...")
        html_obj = HTML(string=content.html)
        logger.info("HTML object created successfully")

        logger.info("Attempting to write PDF...")
        html_obj.write_pdf(pdf_path, stylesheets=[css_obj])
        logger.info("PDF written successfully!")

        filesize = os.path.getsize(pdf_path)
        logger.info(f"PDF filesize: {filesize} bytes")

        logger.info("Inserting new file record into database...")
        insert_file_record(new_file_id, filename, filesize)
        logger.info("File record inserted successfully")

        result = {
            "success": True,
            "file_id": new_file_id,
            "old_file_id": content.file_id,
            "filename": filename,
            "url": f"/assets/{new_file_id}",
            "filesize": filesize
        }
        logger.info(f"Returning result: {result}")
        return result

    except Exception as e:
        logger.error(f"ERROR in PDF update: {type(e).__name__}: {str(e)}")
        logger.exception("Full traceback:")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {"status": "healthy"}