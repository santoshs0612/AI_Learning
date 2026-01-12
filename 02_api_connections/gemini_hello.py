from google import genai

client = genai.Client(
    api_key= "AIzaSyBxfNfumG2MWtl8njFRRMML8ALd-JK_6VQ"
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain how AI works in a few words",
)

print(response.text)