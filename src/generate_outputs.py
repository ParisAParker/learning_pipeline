import json
import re
import pandas as pd
import streamlit as st
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

QUIZ_DIR = Path(__file__).resolve().parent.parent / 'outputs/quizzes'

def clean_raw_quiz_data(raw_quiz):
    output = raw_quiz['choices'][0]['message']['content']

    if "```json" in output:
        json_output = output.split("```json")[1].split("```")[0].strip()

    else:
        raise ValueError("JSON block not found")

    data = json.loads(json_output)

    return data

def export_pdf(data, video_id, output_dir=QUIZ_DIR):
    """
    Export a quiz PDF with:
    - Section 1: Questions only (spaced out)
    - Section 2: Questions + Answers + Explanations

    Args:
        data (str | list): JSON string (raw OpenAI output) or parsed list of dicts
        video_id (str): YouTube video ID, used for filename
        output_dir (Path | str): Directory where PDF will be saved
    """
    with st.spinner("Exporting PDF..."):
        try:
            # If data is a string, extract JSON array
            if isinstance(data, str):
                match = re.search(r"\[.*\]", data, re.DOTALL)
                if not match:
                    raise ValueError("Could not find valid JSON array in string")
                data = json.loads(match.group(0))

            # Ensure it's a list of dicts
            if not isinstance(data, list) or not isinstance(data[0], dict):
                raise TypeError("Data must be a list of dicts with 'question', 'answer', 'explanation'")

            # Ensure output directory exists
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            file_path = output_dir / f"{video_id}.pdf"

            # Build PDF
            doc = SimpleDocTemplate(str(file_path))
            styles = getSampleStyleSheet()
            flowables = []

            # -----------------------------
            # Section 1: Student Version
            # -----------------------------
            flowables.append(Paragraph("Open-Ended Quiz (Student Version)", styles["Title"]))
            flowables.append(Spacer(1, 20))

            for i, d in enumerate(data, 1):
                flowables.append(Paragraph(f"{i}. {d['question']}", styles["Normal"]))
                flowables.append(Spacer(1, 84))  # add extra blank space for writing

            flowables.append(PageBreak())

            # -----------------------------
            # Section 2: Teacher Version
            # -----------------------------
            flowables.append(Paragraph("Open-Ended Quiz (Teacher Version)", styles["Title"]))
            flowables.append(Spacer(1, 20))

            for i, d in enumerate(data, 1):
                flowables.append(Paragraph(f"{i}. {d['question']}", styles["Normal"]))
                flowables.append(Paragraph(f"Answer: {d['answer']}", styles["Italic"]))
                flowables.append(Paragraph(f"Explanation: {d['explanation']}", styles["Normal"]))
                flowables.append(Spacer(1, 12))

            doc.build(flowables)
        
        except Exception as e:
            st.error(f"Error exporting PDF to {file_path}: {str(e)}")
    
    st.success(f"Exported PDF to {file_path}!")

    return file_path