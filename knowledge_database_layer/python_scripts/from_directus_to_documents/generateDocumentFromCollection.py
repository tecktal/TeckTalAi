from directus_sdk_py import DirectusClient


client = DirectusClient(url="https://lms.tecktal.ai/")
client.login(email="your-admin-username@example.com", password="your-admin-username")


collection = "lms_courses"
items = client.get_items(collection)

print(items[0]['title'])
