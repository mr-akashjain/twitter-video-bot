import os
import time
import csv
import json
from groq import Groq
from config import GROQ_API_KEY, WORKING_DIR

client = Groq(api_key=GROQ_API_KEY)

def extract_json_from_response(response_text):
    start_index = response_text.find('{')
    end_index = response_text.rfind('}')
    if start_index != -1 and end_index != -1 and start_index < end_index:
        return json.loads(response_text[start_index:end_index+1])
    return None

def generate_comment(video_title, transcription):
    messages = [
        {"role": "system", "content": (
            "Create a detailed and insightful analysis based on the transcription shared below. "
            "Ensure that the content is full of compassion and respectful towards all castes, religions, individuals, "
            "including Indian Leaders, Bureaucrats, and respects Indian culture. "
            "If the content relates to Indian culture, emphasize praise and respect. "
            "Focus on the most important topic, provide an in-depth analysis, and present it as personal reactions. "
            "Include hashtags at the end. Return in JSON format: {'tweet': 'Your analysis here'}"
        )},
        {"role": "user", "content": f"Title: {video_title}\nTranscription: {transcription}"}
    ]
    try:
        completion = client.chat.completions.create(model="llama3-70b-8192", messages=messages)
        response_text = completion.choices[0].message.content
        extracted_json = extract_json_from_response(response_text)
        return extracted_json['tweet'] if extracted_json and 'tweet' in extracted_json else "What do you think of this??"
    except Exception as e:
        print(f"Error generating comment: {e}")
        return "What do you think of this??"

def generate_comments(csv_file):
    rows = []
    with open(csv_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    for row in rows:
        if row['Status'] != 'transcribed':
            continue
        row['Tweet'] = generate_comment(row['Title'], row['Transcription'])
        row['Status'] = 'comment_generated'
        print(f"Generated comment for: {row['Title']}")
        time.sleep(30)

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
