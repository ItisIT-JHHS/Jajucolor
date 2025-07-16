from google import genai

def ai(str):
    client = genai.Client(api_key="AIzaSyAB6eXDziZ0S7ZH71J_e2NSsVYg9za9yjQ")

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=str,
    )
    return response.text

print(ai(input()))