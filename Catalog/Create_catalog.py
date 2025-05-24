from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
import csv
import json

load_dotenv()

key=os.getenv("GEMINI_AI_API_KEY")
client=genai.Client(api_key=key)
def generate_ai_response(country):
    prompt=f"""
    Give me Top 10 industry and industry sub category for the given {country}\n
    Please output them in Country,Industry,Industry_Sub_Category 
"""
    model="gemini-2.5-flash-preview-05-20"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="application/json",
    )
    response_text=""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        response_text+=chunk.text
    print(response_text)
    data=json.loads(response_text)
    return data

        
def main():
    country=input("Enter country name:")
    records=generate_ai_response(country)
    with open("Catalog.csv","w",newline="") as f:
        fieldnames=["Country","Industry","Industry_Sub_Category"]
        writer=csv.DictWriter(f,fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


if __name__=="__main__":
    main()