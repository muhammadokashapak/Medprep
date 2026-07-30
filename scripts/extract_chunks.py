import fitz
import os

pdf_path = r"E:\USAMA\MBBS Books\First Aid for the USMLE Step 1 2023, 33e.pdf"
out_dir = r"E:\USAMA\MBBS Books\MCQ_Generator\chunks"

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

# Start from page 150 (past index/intro), extract 10 pages per chunk for 8 chunks
start_page = 150
pages_per_chunk = 15

doc = fitz.open(pdf_path)

for i in range(8):
    chunk_text = ""
    for j in range(pages_per_chunk):
        page_num = start_page + (i * pages_per_chunk) + j
        if page_num < len(doc):
            chunk_text += doc[page_num].get_text() + "\n"
    
    out_file = os.path.join(out_dir, f"chunk_{i+1}.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(chunk_text)
    print(f"Generated {out_file}")

doc.close()
print("Chunk extraction complete.")
