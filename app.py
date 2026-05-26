import streamlit as st
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(__file__))

from utils.template_manager import TemplateManager
from utils.document_generator import DocumentGenerator
from utils.config_loader import ConfigLoader

st.set_page_config(
    page_title="制药设备售前文档生成器",
    page_icon="🏭",
    layout="wide"
)

def main():
    st.title("🏭 制药设备售前文档生成器")
    st.markdown("---")
    
    config_loader = ConfigLoader()
    template_manager = TemplateManager()
    
    with st.sidebar:
        st.header("⚙️ 配置选项")
        equipment_type = st.selectbox(
            "选择设备类型",
            ["粉碎机", "混合机", "制粒机", "压片机", "包装机"]
        )
        doc_type = st.selectbox(
            "选择文档类型",
            ["技术方案书", "产品介绍", "招标参数", "报价单"]
        )
        
        st.markdown("---")
        st.markdown("### 📋 项目信息")
        project_name = st.text_input("项目名称", placeholder="例如：XX制药新工厂项目")
        customer_name = st.text_input("客户名称", placeholder="例如：XX制药有限公司")
    
    st.header("📝 基本参数输入")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("设备参数")
        capacity = st.text_input("产能", placeholder="例如：500kg/h")
        power = st.text_input("功率", placeholder="例如：15kW")
        voltage = st.text_input("电压", placeholder="例如：380V")
        dimensions = st.text_input("尺寸(长×宽×高)", placeholder="例如：2000×1500×1800mm")
        
        st.subheader("材质与认证")
        material = st.selectbox(
            "接触物料材质",
            ["SUS304", "SUS316L", "钛合金", "搪瓷"]
        )
        certification = st.multiselect(
            "认证要求",
            ["GMP", "CE", "FDA", "ISO9001", "3A认证"]
        )
    
    with col2:
        st.subheader("功能特性")
        features = st.text_area(
            "主要功能特性",
            placeholder="请描述设备的主要功能特性...",
            height=150
        )
        
        st.subheader("应用场景")
        application = st.text_area(
            "典型应用场景",
            placeholder="请描述设备的典型应用场景...",
            height=150
        )
        
        st.subheader("竞争优势")
        advantages = st.text_area(
            "竞争优势",
            placeholder="请描述设备的竞争优势...",
            height=100
        )
    
    st.markdown("---")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    
    with col_btn2:
        generate_btn = st.button("📄 生成文档", type="primary", use_container_width=True)
    
    if generate_btn:
        if not project_name or not customer_name:
            st.error("请填写项目名称和客户名称！")
            return
        
        with st.spinner("正在生成文档..."):
            doc_data = {
                "equipment_type": equipment_type,
                "doc_type": doc_type,
                "project_name": project_name,
                "customer_name": customer_name,
                "capacity": capacity,
                "power": power,
                "voltage": voltage,
                "dimensions": dimensions,
                "material": material,
                "certification": certification,
                "features": features,
                "application": application,
                "advantages": advantages,
                "date": datetime.now().strftime("%Y-%m-%d")
            }
            
            generator = DocumentGenerator(template_manager)
            docx_path = generator.generate(doc_data)
            
            if docx_path:
                st.success("✅ 文档生成成功！")
                
                with open(docx_path, "rb") as file:
                    st.download_button(
                        label="📥 下载文档",
                        data=file,
                        file_name=f"{project_name}_{equipment_type}_{doc_type}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                
                os.remove(docx_path)
            else:
                st.error("文档生成失败，请检查输入参数！")
    
    st.markdown("---")
    st.markdown("""
    ### 📌 使用说明
    
    1. **选择配置**: 在左侧边栏选择设备类型和文档类型
    2. **填写信息**: 根据提示填写项目信息和设备参数
    3. **生成文档**: 点击"生成文档"按钮，系统将自动生成专业文档
    4. **下载使用**: 点击"下载文档"按钮获取生成的Word文档
    
    ### ✨ 主要功能
    
    - 支持多种制药设备类型的文档生成
    - 自动填充技术参数和规格
    - 生成符合行业标准的专业文档
    - 支持GMP、FDA等认证要求文档
    """)

if __name__ == "__main__":
    main()
