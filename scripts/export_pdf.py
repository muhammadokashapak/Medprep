import sqlite3
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY

def export_mcqs_to_pdf(db_path, output_pdf_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT question, option_a, option_b, option_c, option_d, option_e, correct_answer, explanation FROM mcqs")
    rows = c.fetchall()
    conn.close()

    if not rows:
        print("No MCQs found in the database.")
        return

    doc = SimpleDocTemplate(output_pdf_path, pagesize=letter,
                            rightMargin=50, leftMargin=50,
                            topMargin=50, bottomMargin=50)

    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = styles['Title']
    question_style = ParagraphStyle(
        'Question',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=10,
        fontName='Helvetica-Bold'
    )
    option_style = ParagraphStyle(
        'Option',
        parent=styles['Normal'],
        fontSize=11,
        leftIndent=20,
        spaceAfter=5,
        fontName='Helvetica'
    )
    answer_style = ParagraphStyle(
        'Answer',
        parent=styles['Normal'],
        fontSize=11,
        spaceBefore=10,
        spaceAfter=5,
        fontName='Helvetica-Bold',
        textColor='green'
    )
    explanation_style = ParagraphStyle(
        'Explanation',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=20,
        fontName='Helvetica-Oblique'
    )

    story = []
    
    # Title
    story.append(Paragraph("FCPS Part 1 Generated MCQs", title_style))
    story.append(Spacer(1, 20))

    for i, row in enumerate(rows, 1):
        question, opt_a, opt_b, opt_c, opt_d, opt_e, correct, explanation = row
        
        # Question Text
        story.append(Paragraph(f"Q{i}. {question}", question_style))
        
        # Options
        options = [
            f"A) {opt_a}",
            f"B) {opt_b}",
            f"C) {opt_c}",
            f"D) {opt_d}",
            f"E) {opt_e}"
        ]
        for opt in options:
            if opt.endswith('None') or opt.strip() == "A) " or opt.strip() == "B) " or opt.strip() == "C) " or opt.strip() == "D) " or opt.strip() == "E) ":
                continue # Skip empty options if any
            story.append(Paragraph(opt, option_style))
            
        # Correct Answer
        story.append(Paragraph(f"Correct Answer: {correct}", answer_style))
        
        # Explanation
        story.append(Paragraph(f"Explanation: {explanation}", explanation_style))
        story.append(Spacer(1, 15))

    try:
        doc.build(story)
        print(f"Successfully generated PDF: {output_pdf_path} with {len(rows)} MCQs.")
    except Exception as e:
        print(f"Error generating PDF: {e}")

if __name__ == '__main__':
    db_file = r"E:\USAMA\MBBS Books\MCQ_Generator\fcps_mcqs.db"
    pdf_out = r"E:\USAMA\MBBS Books\MCQ_Generator\FCPS_Part1_MCQs.pdf"
    export_mcqs_to_pdf(db_file, pdf_out)
