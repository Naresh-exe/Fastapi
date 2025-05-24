from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
import csv
import json

load_dotenv()

key=os.getenv("GEMINI_AI_API_KEY")
client=genai.Client(api_key=key)


def process_csv(input_csv):
    file=open(input_csv,"r")
    reader=csv.DictReader(file)
    data=list(reader)
    return data
def process_data(rows):
    BATCHSIZE=5
    output_rows=[]
    for row in range(0,len(rows),BATCHSIZE):
        batch=rows[row:row+BATCHSIZE]
        response=generate_ai_response(batch)
        data=json.loads(response)
        output_rows.extend(data)
    return output_rows
    


def generate_ai_response(batch):
    prompt="""
    Given the following company data,For each Job titles generate one suitable interview-type (eg.,One-on-one,Panel,Phone,Virtual,Behavioral,Case,Screening) and suitable answer format(eg.,STAR,PAR,) based on interview-type. 
    Please output them in Company,Industry,Industry_Sub_Category,Country,Job_Title,Interview_type,Answer_Format
    Data:
"""
    for i,row in enumerate(batch):
        prompt+=f"Company:{row['Company']},Industry:{row['Industry']},Industry Sub Category:{row['Industry_Sub_Category']},Country:{row['Country']},Job title:{row["Job_Title"]}\n"
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
    response=""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text)
        response+=chunk.text
    return response
   
def main():
    print("Entered main")
    input_csv="input.csv"
    rows=process_csv(input_csv)
    records=process_data(rows)
    with open("Final_output.csv","+a",newline="") as output:
        fieldNames=["Company","Industry","Industry_Sub_Category","Country","Job_Title","Interview_type","Answer_Format"]
        writer=csv.DictWriter(output,fieldnames=fieldNames)
        writer.writeheader()
        writer.writerows(records)


if __name__=="__main__":
    main()
