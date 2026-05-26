from docx import Document
from PyPDF2 import PdfReader
from io import BytesIO
import re


def read_pdf(file):
    text = ""
    pdf_reader = PdfReader(file)
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text


def read_docx(file):
    doc = Document(file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text


def read_text(file):
    return file.read().decode("utf-8")


def create_docx_template(content, output_path):
    doc = Document()
    doc.add_heading("制药设备技术文档", 0)
    for section in content:
        if section.get("type") == "heading":
            doc.add_heading(section.get("text"), level=section.get("level", 1))
        elif section.get("type") == "paragraph":
            doc.add_paragraph(section.get("text"))
    doc.save(output_path)


def extract_requirements(text):
    requirements = {
        "equipment_type": None,
        "specifications": [],
        "compliance": [],
        "key_points": []
    }
    
    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        line_lower = line.lower()
        
        if "隔离器" in line or "isolator" in line_lower:
            if "无菌" in line_lower:
                requirements["equipment_type"] = "单体无菌隔离器"
            elif "VHP" in line or "传递窗" in line:
                requirements["equipment_type"] = "VHP传递窗"
            elif "整线" in line_lower:
                requirements["equipment_type"] = "整线隔离器"
            elif "负压" in line_lower:
                requirements["equipment_type"] = "单体负压隔离器"
        
        if "规格" in line or "尺寸" in line or "参数" in line or "spec" in line_lower:
            requirements["specifications"].append(line)
        
        if "GMP" in line or "FDA" in line or "EU" in line or "合规" in line or "compliance" in line_lower:
            requirements["compliance"].append(line)
        
        if "要求" in line or "需求" in line or "必须" in line or "应" in line or "shall" in line_lower:
            requirements["key_points"].append(line)
    
    return requirements


def parse_uploaded_file(uploaded_file):
    file_type = uploaded_file.name.split(".")[-1].lower()
    
    if file_type == "pdf":
        text = read_pdf(uploaded_file)
    elif file_type in ["docx", "doc"]:
        text = read_docx(uploaded_file)
    elif file_type == "txt":
        text = read_text(uploaded_file)
    else:
        text = ""
    
    requirements = extract_requirements(text)
    return text, requirements
