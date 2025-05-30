import requests
import json

def test_api_connection(api_key, base_url):
    """Test if the API is accessible"""
    test_url = f"{base_url}/api/v1/system"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        print(f"Testing API connection to: {test_url}")
        response = requests.get(test_url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Content: {response.text[:500]}")
        return response.status_code == 200
    except Exception as e:
        print(f"Connection test failed: {e}")
        return False

def upload_only_debug(file_path, api_key, base_url, workspace_slug=None):
    # First test the connection
    if not test_api_connection(api_key, base_url):
        print("API connection test failed. Check your base URL and API key.")
        return
    
    upload_url = f"{base_url}/api/v1/document/upload"  # Note: singular 'document'
    headers = {
        "Authorization": f"Bearer {api_key}"
        # Don't set Content-Type for multipart/form-data - requests will set it automatically
    }
    
    print(f"Upload URL: {upload_url}")
    print(f"File path: {file_path}")
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path.split('/')[-1], f, 'application/json')}
            data = {}
            if workspace_slug:
                data['addToWorkspaces'] = workspace_slug

            print("Uploading file...")
            print(f"Headers: {headers}")
            
            
            response = requests.post(upload_url, headers=headers, files=files, data=data)

        print(f"Response Status Code: {response.status_code}")
        
        

        if response.status_code == 200:
            try:
                json_response = response.json()
                print("Upload success:")
                
            except ValueError:
                print("Upload may have succeeded, but response is not valid JSON.")
        else:
            print(f"Upload failed with status code: {response.status_code}")
            
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Upload failed with exception: {e}")

# Alternative endpoint to try (with folder specification)
def upload_to_folder(file_path, api_key, base_url, folder_name="custom-documents", workspace_slug=None):
    upload_url = f"{base_url}/api/v1/document/upload/{folder_name}"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    print(f"Upload URL: {upload_url}")
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path.split('/')[-1], f, 'application/json')}
            data = {}
            if workspace_slug:
                data['addToWorkspaces'] = workspace_slug

            print("Uploading file to folder...")
            response = requests.post(upload_url, headers=headers, files=files, data=data)

        print(f"Response Status Code: {response.status_code}")
       
        if response.status_code == 200:
            try:
                json_response = response.json()
                print("Upload success:")
                #print(json.dumps(json_response, indent=2))
            except ValueError:
                print("Upload may have succeeded, but response is not valid JSON.")
        else:
            print(f"Upload failed with status code: {response.status_code}")
            
    except Exception as e:
        print(f"Upload failed with exception: {e}")

# Bulk upload all files in directory
if __name__ == "__main__":
    import os
    
    # Configuration
    documents_dir = "../../knowledge_database_layer/python_scripts/from_directus_to_documents/generated_documents"
    api_key = "Q4X4QCM-3ES4HKA-JT13TE9-V5P243E"
    base_url = "https://tecktal-anything-llm.d8lkps.easypanel.host"
    workspace_slug = "tecktal-teach"
    folder_name = "LMS_Content"
    
    # Get all files in the directory
    try:
        files_in_dir = [f for f in os.listdir(documents_dir) if os.path.isfile(os.path.join(documents_dir, f))]
        print(f"Found {len(files_in_dir)} files in directory: {documents_dir}")
        print(f"Files: {files_in_dir}")
        
        if not files_in_dir:
            print("No files found in the directory.")
        else:
            # Upload each file
            successful_uploads = 0
            failed_uploads = 0
            
            for filename in files_in_dir:
                file_path = os.path.join(documents_dir, filename)
                print(f"\n{'='*60}")
                print(f"Uploading file {successful_uploads + failed_uploads + 1}/{len(files_in_dir)}: {filename}")
                print(f"{'='*60}")
                
                try:
                    upload_to_folder(file_path, api_key, base_url, folder_name, workspace_slug)
                    successful_uploads += 1
                    print(f" Successfully processed: {filename}")
                except Exception as e:
                    failed_uploads += 1
                    print(f" Failed to process: {filename} - Error: {e}")
            
            print(f"\n{'='*60}")
            print(f"UPLOAD SUMMARY")
            print(f"{'='*60}")
            print(f"Total files: {len(files_in_dir)}")
            print(f"Successful uploads: {successful_uploads}")
            print(f"Failed uploads: {failed_uploads}")
            print(f"Success rate: {(successful_uploads/len(files_in_dir)*100):.1f}%")
            
    except FileNotFoundError:
        print(f"Directory not found: {documents_dir}")
        print("Please check the path and make sure the directory exists.")
    except Exception as e:
        print(f"Error accessing directory: {e}")