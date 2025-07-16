from google import genai
import gradio as gr

def ai(input):
    
    client = genai.Client(api_key="AIzaSyB1_J3DlIgNJvb8aXtUCsOUdklGf_PhXrU")

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=input
    )

    print(response.text)
    return response.text

demo = gr.Interface(fn=ai, inputs="textbox", outputs="textbox")

if __name__ == "__main__":
    demo.launch()