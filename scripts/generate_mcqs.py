import os
import sqlite3
import time
import json
import fitz  # PyMuPDF
import requests
from tqdm import tqdm

API_KEY = "AQ.Ab8RN6LMKHY-FHxIFNTiI2Nfl3b4LIde2bXoYhisPHB-WQj1rw"
PDF_PATH_1 = r"E:\USAMA\MBBS Books\First Aid for the USMLE Step 1 2023, 33e.pdf"
PDF_PATH_2 = r"E:\USAMA\MBBS Books\first-aid-qa-for-the-usmle-step-1-third-edition.pdf"
TARGET_MCQS = 5000
DB_NAME = "fcps_mcqs.db"

def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mcqs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            option_e TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            explanation TEXT NOT NULL,
            source_context TEXT
        )
    ''')
    conn.commit()
    return conn

def extract_text_from_pdf(pdf_path, start_page, end_page):
    try:
        # Suppress MuPDF warnings by redirecting stderr if needed, but we'll just ignore them.
        fitz.TOOLS.mupdf_display_errors(False) 
        doc = fitz.open(pdf_path)
        text = ""
        end_page = min(end_page, len(doc))
        for page_num in range(start_page, end_page):
            try:
                page = doc.load_page(page_num)
                text += page.get_text("text") + "\n"
            except Exception as e:
                pass # Skip problematic pages
        doc.close()
        return text
    except Exception as e:
        return ""

def generate_mcqs_from_text(text_chunk, count=5):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={API_KEY}"
    
    prompt = f"""
    You are an expert medical professor generating exam questions for the FCPS Part 1 exam.
    Based on the following medical text, generate EXACTLY {count} highly difficult, multi-step reasoning multiple-choice questions.
    
    Requirements:
    1. The difficulty must be EXTREME, testing deep basic science concepts.
    2. Each question MUST have 5 options (A, B, C, D, E).
    3. Provide a detailed explanation for why the correct answer is correct AND why the others are wrong.
    4. You MUST output your response in valid JSON format ONLY. No markdown wrappers around the JSON, just the raw JSON array.
    
    Format EXACTLY like this:
    [
      {{
        "question": "A 45-year-old man presents with...",
        "option_a": "First distractor",
        "option_b": "Second distractor",
        "option_c": "Correct concept",
        "option_d": "Third distractor",
        "option_e": "Fourth distractor",
        "correct_answer": "C",
        "explanation": "The correct answer is C because... A is wrong because..."
      }}
    ]

    Here is the medical text to base the questions on:
    {text_chunk}
    """
    
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{"parts":[{"text": prompt}]}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            text_response = result['candidates'][0]['content']['parts'][0]['text'].strip()
            
            # Clean up markdown if model still adds it
            if text_response.startswith("```json"):
                text_response = text_response[7:]
            if text_response.endswith("```"):
                text_response = text_response[:-3]
                
            questions = json.loads(text_response)
            return questions
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"Error parsing MCQs: {e}")
        return []

def save_to_database(conn, mcq, source_context):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO mcqs (question, option_a, option_b, option_c, option_d, option_e, correct_answer, explanation, source_context)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            mcq['question'],
            mcq['option_a'],
            mcq['option_b'],
            mcq['option_c'],
            mcq['option_d'],
            mcq['option_e'],
            mcq['correct_answer'],
            mcq['explanation'],
            source_context
        ))
        conn.commit()
    except Exception as e:
        pass

def main():
    print("Starting FCPS Part 1 MCQ Generator (REST API Version)...")
    conn = setup_database()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM mcqs')
    current_count = cursor.fetchone()[0]
    
    print(f"Current MCQs in database: {current_count} / {TARGET_MCQS}")
    
    if current_count >= TARGET_MCQS:
        print("Target reached!")
        return

    pages_per_chunk = 5
    current_page = 50
    pbar = tqdm(total=TARGET_MCQS, initial=current_count, desc="Generating MCQs")
    
    while current_count < TARGET_MCQS:
        text_chunk = extract_text_from_pdf(PDF_PATH_1, current_page, current_page + pages_per_chunk)
        
        if len(text_chunk.strip()) > 500:
            success = False
            while not success:
                mcqs = generate_mcqs_from_text(text_chunk, count=5)
                
                if mcqs:
                    for mcq in mcqs:
                        if "question" in mcq and "correct_answer" in mcq:
                            source_context = f"First Aid Step 1, Pages {current_page}-{current_page + pages_per_chunk}"
                            save_to_database(conn, mcq, source_context)
                            current_count += 1
                            pbar.update(1)
                            
                            if current_count >= TARGET_MCQS:
                                break
                    success = True
                else:
                    print("Received error from Google (likely 503 High Demand). Waiting 60 seconds before retrying...")
                    time.sleep(60) # Wait a full minute before retrying the same chunk
                    
        current_page += pages_per_chunk
        
        # Standard wait to avoid hitting rate limits
        if current_count < TARGET_MCQS:
            time.sleep(15)

    pbar.close()
    conn.close()
    print("Complete!")

if __name__ == "__main__":
    main()
