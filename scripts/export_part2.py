import sqlite3

def export_to_html(db_path, output_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT question, option_a, option_b, option_c, option_d, option_e, correct_answer, explanation FROM mcqs")
    rows = c.fetchall()
    conn.close()

    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>FCPS Part 1 MCQs - Part 2</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; color: #333; line-height: 1.6; }
            h1 { text-align: center; color: #0056b3; border-bottom: 2px solid #0056b3; padding-bottom: 10px; }
            .mcq-container { background: #f9f9f9; border: 1px solid #ddd; padding: 20px; margin-bottom: 25px; border-radius: 8px; page-break-inside: avoid; }
            .question { font-size: 1.1em; font-weight: bold; margin-bottom: 15px; color: #222; }
            .options { margin-left: 20px; list-style-type: upper-alpha; }
            .options li { margin-bottom: 8px; }
            .answer { margin-top: 15px; font-weight: bold; color: #28a745; }
            .explanation { margin-top: 10px; font-style: italic; color: #555; background: #eef; padding: 10px; border-left: 4px solid #0056b3; }
        </style>
    </head>
    <body>
        <h1>FCPS Part 1 - High Yield MCQs (Part 2)</h1>
    """

    for i, row in enumerate(rows, 1):
        q, a, b, c, d, e, ans, exp = row
        html_content += f"""
        <div class="mcq-container">
            <div class="question">Q{i}. {q}</div>
            <ol class="options">
        """
        for opt in [a, b, c, d, e]:
            if opt and not opt.endswith("None"):
                html_content += f"<li>{opt}</li>"
        
        html_content += f"""
            </ol>
            <div class="answer">Correct Answer: Option {ans}</div>
            <div class="explanation"><strong>Explanation:</strong> {exp}</div>
        </div>
        """

    html_content += """
    </body>
    </html>
    """

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Successfully created {output_path} with {len(rows)} MCQs.")

if __name__ == '__main__':
    db_file = r"E:\USAMA\MBBS Books\MCQ_Generator\part2mcqs.db"
    html_out = r"E:\USAMA\MBBS Books\MCQ_Generator\part2mcqs.html"
    export_to_html(db_file, html_out)
