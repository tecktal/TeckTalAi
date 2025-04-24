from directus_sdk_py import DirectusClient


client = DirectusClient(url="https://lms.tecktal.ai/")
client.login(email="sidyndao@gmail.com", password="admin")


collection = "lms_courses"
items = client.get_items(collection)

print(items[0]['title'])
