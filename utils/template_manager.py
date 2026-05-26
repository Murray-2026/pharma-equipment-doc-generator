import os
import json
from datetime import datetime

class TemplateManager:
    def __init__(self):
        self.template_dir = os.path.dirname(os.path.dirname(__file__))
        self.templates = self.load_templates()
    
    def load_templates(self):
        templates = {}
        template_info_path = os.path.join(self.template_dir, 'templates', 'template_info.json')
        
        if os.path.exists(template_info_path):
            with open(template_info_path, 'r', encoding='utf-8') as f:
                templates = json.load(f)
        else:
            templates = self.get_default_templates()
        
        return templates
    
    def get_default_templates(self):
        return {
            "技术方案书": {
                "sections": [
                    "项目概述",
                    "设备选型依据",
                    "技术规格参数",
                    "设备特点与优势",
                    "质量保证措施",
                    "售后服务承诺",
                    "工程案例"
                ],
                "structure": "standard"
            },
            "产品介绍": {
                "sections": [
                    "产品概述",
                    "技术参数",
                    "工作原理",
                    "应用领域",
                    "选型指南"
                ],
                "structure": "compact"
            },
            "招标参数": {
                "sections": [
                    "基本要求",
                    "技术规格要求",
                    "材质要求",
                    "认证要求",
                    "验收标准"
                ],
                "structure": "detailed"
            },
            "报价单": {
                "sections": [
                    "设备清单",
                    "价格明细",
                    "交货期",
                    "付款方式",
                    "技术培训",
                    "售后服务"
                ],
                "structure": "table"
            }
        }
    
    def get_template(self, doc_type):
        return self.templates.get(doc_type, self.get_default_templates()["技术方案书"])
    
    def get_sections(self, doc_type):
        template = self.get_template(doc_type)
        return template.get("sections", [])
    
    def get_structure(self, doc_type):
        template = self.get_template(doc_type)
        return template.get("structure", "standard")
