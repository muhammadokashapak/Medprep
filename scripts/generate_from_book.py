import os
import sys
import json
import re

# Try importing pypdf
try:
    import pypdf
except ImportError:
    print("Error: 'pypdf' package is not installed.")
    print("Please install it using: pip install pypdf")
    sys.exit(1)

# Try importing google-generativeai
try:
    import google.generativeai as genai
except ImportError:
    print("Warning: 'google-generativeai' package is not installed.")
    print("Please install it to use AI generation features: pip install google-generativeai")
    genai = None

def extract_text_from_pdf(pdf_path, start_page=1, end_page=None):
    """Extracts text from a given PDF path between specified pages."""
    print(f"Reading {pdf_path}...")
    reader = pypdf.PdfReader(pdf_path)
    total_pages = len(reader.pages)
    
    end_page = end_page or total_pages
    start_page = max(1, start_page)
    end_page = min(total_pages, end_page)
    
    extracted_text = ""
    for page_num in range(start_page - 1, end_page):
        page = reader.pages[page_num]
        text = page.extract_text()
        if text:
            extracted_text += f"\n--- Page {page_num + 1} ---\n" + text
            
    print(f"Successfully extracted text from pages {start_page} to {end_page}.")
    return extracted_text

def generate_mcqs_with_ai(text, api_key, exam_name, num_mcqs=5):
    """Sends the extracted text to Gemini API to generate structured clinical MCQs."""
    if not genai:
        print("Error: Gemini library not installed. Install with 'pip install google-generativeai'.")
        return []
        
    genai.configure(api_key=api_key)
    
    prompt = f"""
You are an expert medical educator preparing high-quality clinical multiple choice questions for the {exam_name} exam.
Using the clinical/academic text provided below, generate {num_mcqs} clinical vignette questions.

Each question MUST strictly follow this JSON format:
{{
  "category": "Subject - System, Topic",
  "question": "A detailed clinical scenario introducing a patient, presenting symptoms, lab values, followed by a clear question stem.",
  "option_a": "Distractor A",
  "option_b": "Distractor B",
  "option_c": "Distractor C",
  "option_d": "Distractor D",
  "option_e": "Correct option or distractor",
  "correct_answer": "A" or "B" or "C" or "D" or "E",
  "explanation": "A thorough explanation of why the correct option is correct, and why other distractors are incorrect based on the textbook guidelines."
}}

Ensure that all returned items are contained inside a standard JSON list (e.g. `[ ... ]`).
Return ONLY the raw JSON output. Do not include markdown code block syntax (like ```json).

Medical Text:
\"\"\"
{text}
\"\"\"
"""
    
    print("Calling Gemini API to generate MCQs...")
    # Initialize the Gemini Flash model
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    
    raw_text = response.text.strip()
    
    # Strip markdown block wrappers if present
    if raw_text.startswith("```"):
        raw_text = re.sub(r"^```(?:json)?\n", "", raw_text)
        raw_text = re.sub(r"\n```$", "", raw_text)
        
    try:
        mcqs = json.loads(raw_text)
        return mcqs
    except json.JSONDecodeError as e:
        print("Error: Failed to parse JSON returned from the model.")
        print("Raw response:")
        print(raw_text)
        return []

def main():
    print("====================================================")
    print("          MedPrep Pro MCQ Generator from Books      ")
    print("====================================================")
    
    books_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "books")
    if not os.path.exists(books_dir):
        os.makedirs(books_dir)
        
    book_files = [f for f in os.listdir(books_dir) if f.lower().endswith((".pdf", ".txt"))]
    
    if not book_files:
        print(f"No PDF or TXT files found in: {books_dir}")
        print("Please place your medical textbooks or study guides in the 'books' folder and run this script again.")
        return
        
    print("Available Books:")
    for idx, f in enumerate(book_files):
        print(f" [{idx + 1}] {f}")
        
    try:
        choice = int(input("\nSelect a book index: ")) - 1
        selected_book = book_files[choice]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return
        
    book_path = os.path.join(books_dir, selected_book)
    
    exam_name = input("Target Exam (e.g. USMLE Step 1, PLAB, NEET PG, FCPS Part 1): ") or "USMLE Step 1"
    
    try:
        num_questions = int(input("Number of MCQs to generate: "))
    except ValueError:
        num_questions = 5
        
    api_key = input("Enter your Gemini API Key (or set GEMINI_API_KEY environment variable): ")
    api_key = api_key or os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        print("Error: API Key is required to generate MCQs using AI.")
        return
        
    if selected_book.lower().endswith(".pdf"):
        try:
            start_page = int(input("Start page number: "))
            end_page = int(input("End page number: "))
        except ValueError:
            print("Invalid page numbers. Defaulting to first few pages.")
            start_page = 1
            end_page = 5
        extracted_text = extract_text_from_pdf(book_path, start_page, end_page)
    else:
        print(f"Reading text file: {selected_book}...")
        try:
            with open(book_path, "r", encoding="utf-8") as f:
                extracted_text = f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return
            
    if not extracted_text.strip():
        print("Error: No text content could be extracted.")
        return
        
    mcqs = generate_mcqs_with_ai(extracted_text, api_key, exam_name, num_questions)
    
    if mcqs:
        # Load existing questions to assign new IDs
        questions_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
            "src", "data", "questions.json"
        )
        
        existing_questions = []
        if os.path.exists(questions_file):
            try:
                with open(questions_file, "r", encoding="utf-8") as f:
                    existing_questions = json.load(f)
            except json.JSONDecodeError:
                pass
                
        next_id = max([q.get("id", 0) for q in existing_questions] + [0]) + 1
        
        for q in mcqs:
            q["id"] = next_id
            next_id += 1
            existing_questions.append(q)
            
        # Write back
        with open(questions_file, "w", encoding="utf-8") as f:
            json.dump(existing_questions, f, indent=2, ensure_ascii=False)
            
        print(f"\nSuccess! Successfully appended {len(mcqs)} new questions to questions.json.")
        print(f"The QBank now contains {len(existing_questions)} total questions.")
    else:
        print("No MCQs were generated.")

if __name__ == "__main__":
    main()
