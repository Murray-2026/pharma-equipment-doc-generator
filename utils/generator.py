from templates.template_manager import TemplateManager
from datetime import datetime
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os


class DocumentGenerator:
    def __init__(self, equipment_type, regulation):
        self.template_manager = TemplateManager(equipment_type, regulation)
        self.equipment_type = equipment_type
        self.regulation = regulation
    
    def generate_urs_response(self, requirements=None):
        return self.template_manager.get_urs_response_template(requirements)
    
    def generate_technical_spec(self):
        return self.template_manager.get_technical_spec_template()
    
    def generate_quotation(self, config_type="standard"):
        return self.template_manager.get_quotation_template(config_type)
    
    def generate_all_documents(self, requirements=None):
        documents = {
            "urs_response": self.generate_urs_response(requirements),
            "technical_spec": self.generate_technical_spec(),
            "quotation_basic": self.generate_quotation("basic"),
            "quotation_standard": self.generate_quotation("standard"),
            "quotation_premium": self.generate_quotation("premium")
        }
        return documents
    
    def save_markdown(self, content, filename, output_dir="outputs"):
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return filepath
    
    def create_word_document(self, content, filename, output_dir="outputs"):
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        
        doc = Document()
        
        lines = content.split("\n")
        in_table = False
        table_headers = []
        table_rows = []
        
        for line in lines:
            line = line.rstrip()
            if not line:
                doc.add_paragraph()
                continue
            
            if line.startswith("# "):
                heading = doc.add_heading(line[2:], level=1)
                heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif line.startswith("## "):
                doc.add_heading(line[3:], level=2)
            elif line.startswith("### "):
                doc.add_heading(line[4:], level=3)
            elif line.startswith("**") and line.endswith("**"):
                p = doc.add_paragraph()
                run = p.add_run(line[2:-2])
                run.bold = True
            elif line.startswith("|") and "|" in line[1:]:
                in_table = True
                cells = [cell.strip() for cell in line.split("|") if cell.strip()]
                if not table_headers:
                    table_headers = cells
                else:
                    table_rows.append(cells)
            elif line.startswith("---") and in_table:
                continue
            elif line.startswith("- "):
                p = doc.add_paragraph(line[2:], style="List Bullet")
            else:
                if in_table and table_headers:
                    table = doc.add_table(rows=1, cols=len(table_headers))
                    table.style = "Table Grid"
                    
                    hdr_cells = table.rows[0].cells
                    for i, header in enumerate(table_headers):
                        hdr_cells[i].text = header
                        for paragraph in hdr_cells[i].paragraphs:
                            for run in paragraph.runs:
                                run.bold = True
                    
                    for row_cells in table_rows:
                        row_cells = row_cells + [""] * (len(table_headers) - len(row_cells))
                        row = table.add_row().cells
                        for i, cell in enumerate(row_cells):
                            row[i].text = cell
                    
                    table_headers = []
                    table_rows = []
                    in_table = False
                
                doc.add_paragraph(line)
        
        if table_headers and table_rows:
            table = doc.add_table(rows=1, cols=len(table_headers))
            table.style = "Table Grid"
            
            hdr_cells = table.rows[0].cells
            for i, header in enumerate(table_headers):
                hdr_cells[i].text = header
                for paragraph in hdr_cells[i].paragraphs:
                    for run in paragraph.runs:
                        run.bold = True
            
            for row_cells in table_rows:
                row_cells = row_cells + [""] * (len(table_headers) - len(row_cells))
                row = table.add_row().cells
                for i, cell in enumerate(row_cells):
                    row[i].text = cell
        
        doc.save(filepath)
        return filepath
