from dotenv import load_dotenv
from google import genai
from google.genai import types
import os
import json
load_dotenv()
key=os.getenv("GEMINI_AI_API_KEY")
client=genai.Client(api_key=key)

def main():
    prompt="Top 10 Companies in the world"
    model="gemini-2.5-flash-preview-05-20"
    contents=[
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt)
            ]
        )
    ]
    response_format=types.GenerateContentConfig(
        response_mime_type="application/json"
    )
    response=client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=response_format
    )
    response_text=""
    for i in response:
        response_text+=i.text
    result=[]
    data=json.loads(response_text)
    result.extend(data)
    print(result)

if __name__=="__main__":
    main()


