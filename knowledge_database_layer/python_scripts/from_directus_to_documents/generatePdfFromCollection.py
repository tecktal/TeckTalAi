from fpdf import FPDF
import os
from directus_sdk_py import DirectusClient

# Initialize Directus client
client = DirectusClient(url="https://lms.tecktal.ai/", token="your-directus-token")

# Define collection names
course_collection_name = "lms_courses"
module_collection_name = "lms_modules"
lesson_collection_name = "lms_lessons"

# Path to your Unicode TrueType font
FONT_PATH = os.path.join(os.path.dirname(__file__), "fonts/DejaVuSans.ttf")

# Custom PDF class to format headers properly
class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font('DejaVu', '', FONT_PATH, uni=True)
        self.set_font('DejaVu', '', 14)

    def header(self):
        self.set_font('DejaVu', 'B', 16)

    def chapter_title(self, title):
        self.set_font('DejaVu', 'B', 16)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(10)

    def section_title(self, title):
        self.set_font('DejaVu', 'B', 14)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT", align="L")
        self.ln(5)

    def subsection_title(self, title):
        self.set_font('DejaVu', 'B', 12)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT", align="L")
        self.ln(3)

    def paragraph(self, text):
        self.set_font('DejaVu', '', 11)
        if text:  # Avoid crashing on None
            self.multi_cell(0, 6, text)
            self.ln(3)

# Create the output folder if it doesn't exist
output_folder = os.path.join(os.path.dirname(__file__), "generated_documents")
os.makedirs(output_folder, exist_ok=True)

# Fetch all courses
courses = client.get_items(course_collection_name)

for selected_course in courses:
    pdf = PDF()
    pdf.add_page()

    # Course title
    pdf.chapter_title(selected_course["title"])

    # Course information
    pdf.section_title("Course Information")
    pdf.paragraph(f"Slug: {selected_course.get('slug', '')}")
    pdf.paragraph(f"Status: {selected_course.get('status', '')}")
    pdf.paragraph(f"Description: {selected_course.get('description', '')}")
    pdf.paragraph(f"Long Description: {selected_course.get('description_long', '')}")

    # Fetch modules for this course
    module_filter = {
        "query": {
            "filter": {
                "course": {
                    "_eq": selected_course["id"]
                }
            }
        }
    }
    modules = client.get_items(module_collection_name, module_filter)

    if modules:
        # Sort modules by title
        modules = sorted(modules, key=lambda m: m.get('title', ''))

        pdf.section_title("Modules")
        for module in modules:
            pdf.subsection_title(f"Module: {module['title']}")
            pdf.paragraph(f"Description: {module.get('description', '')}")

            # Fetch lessons for this module
            lesson_filter = {
                "query": {
                    "filter": {
                        "module": {
                            "_eq": module["id"]
                        }
                    }
                }
            }
            lessons = client.get_items(lesson_collection_name, lesson_filter)

            if lessons:
                # Sort lessons by title
                lessons = sorted(lessons, key=lambda l: l.get('title', ''))

                for lesson in lessons:
                    pdf.subsection_title(f"Lesson: {lesson['title']}")
                    pdf.paragraph(f"Slug: {lesson.get('slug', '')}")
                    pdf.paragraph(f"Video URL: {lesson.get('video_url', '')}")
                    pdf.paragraph(f"Video Duration: {lesson.get('video_duration', '')}")
                    pdf.paragraph(f"Video Transcript: {lesson.get('video_transcript', '')}")
                    pdf.paragraph(f"Content: {lesson.get('content', '')}")

    # Save PDF
    output_file_path = os.path.join(output_folder, f"{selected_course['slug']}.pdf")
    pdf.output(output_file_path)

    print(f"Course PDF saved to {output_file_path}")
