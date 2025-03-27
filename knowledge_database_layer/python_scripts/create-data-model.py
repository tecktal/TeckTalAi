from directus_sdk_py import DirectusClient
from lms_data_schema.lms_folder_schema import *

# Initialize the Directus client and authenticate using admin credentials
client = DirectusClient(url="http://localhost:8060/")
client.login(email="admin@example.com", password="your-admin-password")

# Create folders
if not client.collection_exists(lms_schema['collection']):
    nested_response = client.post('/collections', json=lms_schema)
    print(f"{lms_schema['collection']} created successfully")
else:
    print(f"{lms_schema['collection']} already exists")

for sub_folder in [lms_content_schema, lms_quizz_and_exams_schema, lms_data_schema, lms_metadata_schema]:
    if not client.collection_exists(sub_folder['collection']):
        response = client.post('/collections', json=sub_folder)
        print(f"{sub_folder['collection']} sub-folder Created Succesfully")
    else:
        print(f"{sub_folder['collection']} already exits")


# 3. Create Collection

def create_collections(list_of_collections):
    for collection in list_of_collections:
        collection_name = collection["collection"]

        try:
            # Check if the collection exists
            if client.collection_exists(collection_name):
                print(f"✅ Collection '{collection_name}' already exists, skipping...")
                continue

            # If not, create it
            response = client.post("/collections", json=collection)
            print(f"✅ Collection '{collection_name}' created successfully.")

        except AssertionError as e:
            error_message = str(e)

            # Handle "permission denied" error
            if "FORBIDDEN" in error_message:
                print(f"⚠️ Permission denied: Cannot check or create collection '{collection_name}'.")
                continue

            print(f"❌ Unexpected error for '{collection_name}': {error_message}")

        except Exception as e:
            print(f"❌ Failed to create collection '{collection_name}': {str(e)}")


# 3.1 content
create_collections([lms_course, lms_module, lms_lesson, lms_instructor, lms_lessons_resources])

# 3.2 quizz and exams
create_collections([lms_question_bank, lms_quizz])

# 3.3 data
create_collections([lms_enrollement, lms_courses_reviews, lms_comments])

# 3.4 metadata
create_collections([lms_tracks, lms_topic, lms_settings])


# Create Fields
def create_multiple_fields_in_collection(list_of_fields):
    for field in list_of_fields:
        collection = field["collection"]
        field_name = field["field"]

        try:
            # Check if the field exists
            response = client.get(f"/fields/{collection}/{field_name}")

            # If the request succeeds, the field exists
            print(f"✅ Field '{field_name}' already exists in '{collection}', skipping...")
            continue

        except AssertionError as e:
            error_message = str(e)

            # If 403 Forbidden, assume the field does not exist (Directus limitation)
            if "FORBIDDEN" in error_message:
                print(
                    f"⚠️ Field '{field_name}' might not exist in '{collection}' (403 Forbidden). Proceeding to create it.")

            # If other errors occur, print them and skip this field
            elif "NOT_FOUND" not in error_message:
                print(f"❌ Unexpected error while checking field '{field_name}': {error_message}")
                continue

        except Exception as e:
            print(f"❌ Failed to check field '{field_name}': {str(e)}")
            continue

        # Create the field since it does not exist
        try:
            create_response = client.post(f"/fields/{collection}", json=field)
            print(f"✅ Field '{field_name}' created successfully in '{collection}'.")

        except Exception as e:
            print(f"❌ Failed to creat field '{field_name}': {str(e)}")


# Create Fields for lms_content collections
create_multiple_fields_in_collection(lms_course_fields)
create_multiple_fields_in_collection(lms_modules_fields)
create_multiple_fields_in_collection(lms_lessons_fields)
create_multiple_fields_in_collection(lms_instructors_fields)
create_multiple_fields_in_collection(lms_lessons_ressources_fields)

# Create Fields for lms_quizz_and_exams collections
create_multiple_fields_in_collection(lms_question_bank_fields)
create_multiple_fields_in_collection(lms_quizz_fields)

# Create Fields for lms_data collections
create_multiple_fields_in_collection(lms_comments_fields)
create_multiple_fields_in_collection(lms_enrollments_fields)
create_multiple_fields_in_collection(lms_course_reviews_fields)

# Create Fields for lms_metadata collections
create_multiple_fields_in_collection(lms_settings_fields)
create_multiple_fields_in_collection(lms_track_fields)
create_multiple_fields_in_collection(lms_topics_fields)

# Create Relationships