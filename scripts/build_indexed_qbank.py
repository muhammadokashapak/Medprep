import os
import json
import re

def build_indexed_qbank():
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    questions_file = os.path.join(workspace_root, "src", "data", "questions.json")
    qbank_dir = os.path.join(workspace_root, "src", "data", "qbank")
    os.makedirs(qbank_dir, exist_ok=True)
    
    if not os.path.exists(questions_file):
        print("questions.json not found!")
        return

    with open(questions_file, "r", encoding="utf-8") as f:
        questions = json.load(f)

    print(f"Indexing {len(questions)} questions into modular book/category chunks...")

    book_chunks = {}
    category_chunks = {}

    for q in questions:
        book = str(q.get("book_source", "General Medical QBank")).strip()
        cat = str(q.get("category", "General")).strip()
        
        # Clean slug
        book_slug = re.sub(r'[^a-zA-Z0-9_]', '_', book.lower())[:30]
        cat_slug = re.sub(r'[^a-zA-Z0-9_]', '_', cat.lower())[:30]
        
        if book_slug not in book_chunks:
            book_chunks[book_slug] = {"name": book, "questions": []}
        book_chunks[book_slug]["questions"].append(q)

        if cat_slug not in category_chunks:
            category_chunks[cat_slug] = {"name": cat, "questions": []}
        category_chunks[cat_slug]["questions"].append(q)

    # Save indexed metadata overview
    index_meta = {
        "total_questions": len(questions),
        "books": [],
        "categories": []
    }

    for slug, data in book_chunks.items():
        chunk_filename = f"book_{slug}.json"
        chunk_path = os.path.join(qbank_dir, chunk_filename)
        with open(chunk_path, "w", encoding="utf-8") as f:
            json.dump(data["questions"], f, ensure_ascii=False)
        index_meta["books"].append({
            "slug": slug,
            "name": data["name"],
            "count": len(data["questions"]),
            "file": f"qbank/{chunk_filename}"
        })

    index_path = os.path.join(workspace_root, "src", "data", "qbank_index.json")
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index_meta, f, indent=2, ensure_ascii=False)

    print(f"Created index file: {index_path}")
    print(f"Split dataset into {len(book_chunks)} modular book files in {qbank_dir}.")

if __name__ == "__main__":
    build_indexed_qbank()
