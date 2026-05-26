import json
import os

class ConfigLoader:
    def __init__(self):
        self.config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
        self.config = self.load_config()
    
    def load_config(self):
        config_path = os.path.join(self.config_dir, 'config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self.get_default_config()
    
    def get_default_config(self):
        return {
            "equipment_types": {
                "粉碎机": {
                    "default_capacity": "100-500kg/h",
                    "default_power": "5-15kW",
                    "default_voltage": "380V"
                },
                "混合机": {
                    "default_capacity": "50-200L",
                    "default_power": "3-7.5kW",
                    "default_voltage": "380V"
                },
                "制粒机": {
                    "default_capacity": "30-150kg/h",
                    "default_power": "2-5kW",
                    "default_voltage": "380V"
                },
                "压片机": {
                    "default_capacity": "5000-10000片/h",
                    "default_power": "2-4kW",
                    "default_voltage": "380V"
                },
                "包装机": {
                    "default_capacity": "30-100盒/min",
                    "default_power": "2-3kW",
                    "default_voltage": "220V/380V"
                }
            },
            "materials": ["SUS304", "SUS316L", "钛合金", "搪瓷"],
            "certifications": ["GMP", "CE", "FDA", "ISO9001", "3A认证"]
        }
    
    def get_equipment_config(self, equipment_type):
        return self.config.get("equipment_types", {}).get(equipment_type, {})
    
    def get_material_options(self):
        return self.config.get("materials", [])
    
    def get_certification_options(self):
        return self.config.get("certifications", [])
