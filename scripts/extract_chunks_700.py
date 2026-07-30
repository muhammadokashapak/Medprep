import fitz
import os

pdf_path = r"E:\USAMA\MBBS Books\First Aid for the USMLE Step 1 2023, 33e.pdf"
out_dir = r"E:\USAMA\MBBS Books\MCQ_Generator\chunks_700"

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

start_page = 270
pages_per_chunk = 15
num_chunks = 14

doc = fitz.open(pdf_path)

for i in range(num_chunks):
    chunk_text = ""
    for j in range(pages_per_chunk):
        page_num = start_page + (i * pages_per_chunk) + j
        if page_num < len(doc):
            chunk_text += doc[page_num].get_text() + "\n"
    
    # We will number them 9 to 22
    chunk_index = i + 9
    out_file = os.path.join(out_dir, f"chunk_{chunk_index}.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(chunk_text)
    print(f"Generated {out_file}")

doc.close()
print("700 MCQs Chunk extraction complete.")
