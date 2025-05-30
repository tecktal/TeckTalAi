import os
import json
from directus_sdk_py import DirectusClient

# Initialize Directus client
client = DirectusClient(url="https://lms.tecktal.ai/", token="gE-Rd6oO2pbkolA8keNtihRnBs7qbU7m")

# Define collection names
course_collection_name = "lms_courses"
module_collection_name = "lms_modules"
lesson_collection_name = "lms_lessons"
assignment_collection_name = "lms_assignment"
resource_collection_name = "lms_resources"

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
        "live_preview": selected_course["live_preview"],
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
            "live_preview": module["live_preview"],
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
                "content": lesson["content"],
                "live_preview": lesson["live_preview"]
            }
                    # Fetch assignments related to this lesson
            assignment_filter = {
                "query": {
                    "filter": {
                        "lesson": {
                            "_eq": lesson["id"]
                        }
                    }
                }
            }
            resource_filter = {
                "query": {
                    "filter": {
                        "lesson": {
                            "_eq": lesson["id"]
                        }
                    }
                }
            }

            assignments = client.get_items(assignment_collection_name, assignment_filter)
            print(assignments)
            resources = client.get_items(resource_collection_name, resource_filter)
            
            # Add assignments data
            lesson_data["assignments"] = []
            if assignments and isinstance(assignments, list):  # Check if it's a valid list
                for assignment in assignments:
                    if isinstance(assignment, dict):  # Only process if it's a valid dictionary
                        assignment_data = {
                            "id": assignment.get("id", ""),
                            "title": assignment.get("title", ""), 
                            "description": assignment.get("description", ""),
                            "instructions": assignment.get("instructions", ""),
                            "file": assignment.get("file", ""),
                            "live_preview": assignment.get("live_preview", "")
                        }
                        lesson_data["assignments"].append(assignment_data)

            # Add resources data
            lesson_data["resources"] = []
            if resources and isinstance(resources, list):  # Check if it's a valid list
                for resource in resources:
                    if isinstance(resource, dict):  # Only process if it's a valid dictionary
                        resource_data = {
                            "id": resource.get("id", ""),
                            "resource_type": resource.get("resource_type", ""),
                            "url": resource.get("url", ""),
                            "file": resource.get("file", ""),
                            "title": resource.get("title", ""),
                            "description": resource.get("description", ""),
                            "live_preview": resource.get("live_preview", "")
                        }
                        lesson_data["resources"].append(resource_data)

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
