import os
import json
from directus_sdk_py import DirectusClient

# Initialize Directus client
client = DirectusClient(url="https://lms.tecktal.ai/", token="6HZNyNOEL4d-oKLbHRafYbliDEZ3LIWj")

# Define collection names
course_collection_name = "lms_courses"
module_collection_name = "lms_modules"
lesson_collection_name = "lms_lessons"

# Fetch all courses
courses = client.get_items(course_collection_name)

for selected_course in courses:
    # Structure the course data
    course_data = {
        "id": selected_course["id"],
        "title": selected_course["title"],
        "slug": selected_course["slug"],
        "status": selected_course["status"],
        "description": selected_course["description"],
        "description_long": selected_course["description_long"],
        "modules": []
    }

    # Fetch modules related to the selected course
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

    for module in modules:
        module_data = {
            "id": module["id"],
            "title": module["title"],
            "description": module["description"],
            "lessons": []
        }

        # Fetch lessons related to this module
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

        for lesson in lessons:
            lesson_data = {
                "id": lesson["id"],
                "title": lesson["title"],
                "slug": lesson["slug"],
                "video_url": lesson["video_url"],
                "video_duration": lesson["video_duration"],
                "video_transcript": lesson["video_transcript"],
                "content": lesson["content"]
            }
            module_data["lessons"].append(lesson_data)

        course_data["modules"].append(module_data)

    # === Save to generated_documents folder ===

    # Create the folder if it doesn't exist
    output_folder = os.path.join(os.path.dirname(__file__), "generated_documents")
    os.makedirs(output_folder, exist_ok=True)

    # Define the output file path
    output_file_path = os.path.join(output_folder, f"{selected_course['slug']}.json")

    # Write JSON
    with open(output_file_path, "w", encoding="utf-8") as json_file:
        json.dump(course_data, json_file, indent=4, ensure_ascii=False)

    print(f"Course data saved to {output_file_path}")
