# Base libraries
import json
import re
from pathlib import Path

# 3rd party packages
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

from utils.logger import get_logger
from config.paths import PDF_OUTPUTS_DIR

logger = get_logger(__name__)

def export_pdf(data, source_id, output_dir=PDF_OUTPUTS_DIR):
    """
    Export a quiz PDF with:
    - Section 1: Questions only (spaced out)
    - Section 2: Questions + Answers + Explanations

    Args:
        data (str | list): JSON string (raw OpenAI output) or parsed list of dicts
        source_id (str): YouTube video ID or txt file source id
        output_dir (Path | str): Directory where PDF will be saved
    """

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
        file_path = output_dir / f"{source_id}.pdf"

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
        logger.info(f"Exported PDF to {file_path}")
    
    except Exception as e:
        logger.error(f"Error exporting PDF to {file_path}: {str(e)}")

    return file_path