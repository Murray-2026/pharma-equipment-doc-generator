import streamlit as st
import os
from io import BytesIO
from datetime import datetime
from utils.document_utils import parse_uploaded_file, extract_requirements

st.set_page_config(
    page_title="制药设备售前文档生成器",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

def init_session_state():
    if "generated_documents" not in st.session_state:
        st.session_state.generated_documents = None
    if "selected_config" not in st.session_state:
        st.session_state.selected_config = "standard"
    if "urs_text" not in st.session_state:
        st.session_state.urs_text = ""
    if "custom_templates" not in st.session_state:
        st.session_state.custom_templates = {
            "urs_response": None,
            "technical_spec": None,
            "quotation": None
        }

def main():
    init_session_state()
    
    st.title("🏭 制药设备售前文档生成器")
    st.markdown("---")
    
    st.sidebar.title("配置")
    
    st.sidebar.subheader("设备类型")
    equipment_type = st.sidebar.selectbox(
        "选择设备类型",
        ["单体无菌隔离器", "VHP传递窗", "整线隔离器", "单体负压隔离器"],
        index=0
    )
    
    st.sidebar.subheader("法规标准（可多选）")
    regulations = st.sidebar.multiselect(
        "选择适用的法规标准",
        ["中国GMP 2010版", "FDA 21 CFR Part 11", "EU GMP Annex 1", "PIC/S GMP", "ISO 14644", "GAMP 5"],
        default=["中国GMP 2010版"],
        help="可以选择多个法规标准，生成的文档将涵盖所有选中的合规要求"
    )
    
    regulation_text = ", ".join(regulations) if regulations else "中国GMP 2010版"
    
    st.sidebar.subheader("📁 自定义模板")
    st.sidebar.markdown("上传您自己的文档模板（支持Excel/Word/Markdown格式）")
    
    template_type = st.sidebar.selectbox(
        "选择模板类型",
        ["URS回复模板", "技术方案模板", "报价单模板"]
    )
    
    uploaded_template = st.sidebar.file_uploader(
        "上传自定义模板",
        type=["xlsx", "xls", "docx", "md", "txt"]
    )
    
    if uploaded_template is not None:
        template_key = {
            "URS回复模板": "urs_response",
            "技术方案模板": "technical_spec",
            "报价单模板": "quotation"
        }[template_type]
        
        if uploaded_template.name.endswith((".xlsx", ".xls")):
            import pandas as pd
            df = pd.read_excel(uploaded_template)
            template_content = df.to_markdown(index=False)
        elif uploaded_template.name.endswith(".docx"):
            from docx import Document
            doc = Document(uploaded_template)
            template_content = "\n".join([p.text for p in doc.paragraphs])
        else:
            template_content = uploaded_template.read().decode("utf-8")
        
        st.session_state.custom_templates[template_key] = template_content
        st.sidebar.success(f"✅ {template_type}已上传")
    
    if st.sidebar.button("使用默认模板"):
        st.session_state.custom_templates = {
            "urs_response": None,
            "technical_spec": None,
            "quotation": None
        }
        st.sidebar.success("已切换到默认模板")
    
    st.markdown("### 步骤 1: 输入或上传URS文档")
    
    tab1, tab2 = st.tabs(["📝 直接输入URS文本", "📁 上传文档"])
    
    with tab1:
        st.markdown("#### 请输入客户的URS（用户需求说明）")
        st.markdown("您可以直接粘贴或输入完整的URS文本内容，系统将智能解析并生成详细的逐条响应")
        urs_input = st.text_area(
            "URS文本内容",
            value=st.session_state.urs_text,
            height=300,
            placeholder="请在此输入或粘贴客户的URS文档内容...\n\n例如：\n## 1. 概述\n本URS定义了无菌隔离器的技术要求，适用于注射剂无菌生产环境...\n\n## 2. 适用范围\n本URS适用于新建无菌车间的隔离器系统...\n\n## 3. 设备要求\n3.1 设备类型：单体无菌隔离器\n3.2 工作舱尺寸：不小于1200×800×1000mm（长×宽×高）\n3.3 材质要求：与产品接触部分为316L不锈钢\n\n## 4. 法规要求\n符合中国GMP 2010版附录1无菌药品要求...",
            help="支持任意长度的文本输入，系统将自动解析关键需求点"
        )
        st.session_state.urs_text = urs_input
    
    with tab2:
        uploaded_file = st.file_uploader(
            "上传客户询盘或URS文档（PDF/Word/Excel/文本）",
            type=["pdf", "docx", "doc", "xlsx", "xls", "txt"]
        )
        if uploaded_file is not None:
            st.success(f"已成功上传文件: {uploaded_file.name}")
            with st.spinner("正在解析文档..."):
                text, _ = parse_uploaded_file(uploaded_file)
                st.session_state.urs_text = text
    
    requirements = None
    
    if st.session_state.urs_text.strip():
        with st.spinner("正在智能解析URS..."):
            requirements = extract_requirements(st.session_state.urs_text)
        
        st.markdown("---")
        st.markdown("### 🤖 智能解析结果")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📦 设备类型识别")
            if requirements["equipment_type"]:
                st.success(f"✅ 检测到设备类型: **{requirements['equipment_type']}**")
                if requirements["equipment_type"] != equipment_type:
                    if st.button(f"使用检测到的设备类型: {requirements['equipment_type']}"):
                        st.success("设备类型已更新，请刷新页面")
            else:
                st.info("💡 未检测到明确的设备类型，请在左侧手动选择")
            
            st.subheader("📋 合规要求提取")
            if requirements["compliance"]:
                st.markdown("**检测到以下合规要求：**")
                for i, req in enumerate(requirements["compliance"], 1):
                    st.markdown(f"{i}. {req}")
            else:
                st.info("未提取到明确的合规要求")
        
        with col2:
            st.subheader("⚙️ 技术规格提取")
            if requirements["specifications"]:
                st.markdown("**检测到以下技术规格：**")
                for i, spec in enumerate(requirements["specifications"], 1):
                    st.markdown(f"{i}. {spec}")
            else:
                st.info("未提取到明确的技术规格")
            
            st.subheader("🎯 关键需求点")
            if requirements["key_points"]:
                st.markdown("**检测到以下关键需求：**")
                for i, point in enumerate(requirements["key_points"], 1):
                    st.markdown(f"{i}. {point}")
            else:
                st.info("未提取到明确的需求点")
        
        with st.expander("📄 查看完整URS内容"):
            st.text_area("完整内容", st.session_state.urs_text, height=200)
    
    st.markdown("---")
    st.markdown("### 步骤 2: 生成文档")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        template_used = "自定义" if st.session_state.custom_templates["urs_response"] else "默认"
        if st.button(f"📄 生成URS逐条回复 ({template_used})", use_container_width=True):
            from utils.generator import DocumentGenerator
            with st.spinner("正在生成URS逐条回复..."):
                generator = DocumentGenerator(equipment_type, regulation_text, st.session_state.custom_templates, regulations)
                st.session_state.generated_documents = {
                    "urs_response": generator.generate_urs_response(requirements)
                }
            st.success("URS逐条回复生成成功！")
    
    with col2:
        template_used = "自定义" if st.session_state.custom_templates["technical_spec"] else "默认"
        if st.button(f"📋 生成技术方案 ({template_used})", use_container_width=True):
            from utils.generator import DocumentGenerator
            with st.spinner("正在生成技术方案..."):
                generator = DocumentGenerator(equipment_type, regulation_text, st.session_state.custom_templates, regulations)
                st.session_state.generated_documents = {
                    "technical_spec": generator.generate_technical_spec()
                }
            st.success("技术方案生成成功！")
    
    with col3:
        template_used = "自定义" if st.session_state.custom_templates["quotation"] else "默认"
        if st.button(f"💰 生成报价文档 ({template_used})", use_container_width=True):
            from utils.generator import DocumentGenerator
            with st.spinner("正在生成报价文档..."):
                generator = DocumentGenerator(equipment_type, regulation_text, st.session_state.custom_templates, regulations)
                st.session_state.generated_documents = {
                    "quotation_basic": generator.generate_quotation("basic"),
                    "quotation_standard": generator.generate_quotation("standard"),
                    "quotation_premium": generator.generate_quotation("premium")
                }
            st.success("报价文档生成成功！")
    
    if st.button("✨ 一键生成全部文档", type="primary", use_container_width=True):
        from utils.generator import DocumentGenerator
        with st.spinner("正在生成全套文档..."):
            generator = DocumentGenerator(equipment_type, regulation_text, st.session_state.custom_templates, regulations)
            st.session_state.generated_documents = generator.generate_all_documents(requirements)
        st.success("全套文档生成成功！")
    
    if st.session_state.generated_documents:
        st.markdown("---")
        st.markdown("### 步骤 3: 预览和下载")
        
        doc_types = list(st.session_state.generated_documents.keys())
        
        if len(doc_types) > 1:
            selected_doc = st.selectbox(
                "选择要预览的文档",
                doc_types,
                format_func=lambda x: {
                    "urs_response": "📄 URS逐条回复",
                    "technical_spec": "📋 技术方案",
                    "quotation_basic": "💰 报价单（基础配置）",
                    "quotation_standard": "💰 报价单（标准配置）",
                    "quotation_premium": "💰 报价单（高级配置）"
                }.get(x, x)
            )
        else:
            selected_doc = doc_types[0]
        
        content = st.session_state.generated_documents[selected_doc]
        
        with st.expander("📖 预览文档内容", expanded=True):
            st.markdown(content)
        
        st.markdown("#### 📥 下载文档")
        
        col1, col2 = st.columns(2)
        
        with col1:
            filename = f"{selected_doc}.md"
            st.download_button(
                label="📝 下载 Markdown 格式",
                data=content.encode("utf-8"),
                file_name=filename,
                mime="text/markdown",
                use_container_width=True
            )
        
        with col2:
            from utils.generator import DocumentGenerator
            generator = DocumentGenerator(equipment_type, regulation_text, st.session_state.custom_templates, regulations)
            doc_buffer = BytesIO()
            try:
                import tempfile
                with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
                    doc_path = generator.create_word_document(content, os.path.basename(tmp.name), os.path.dirname(tmp.name))
                    with open(doc_path, "rb") as f:
                        doc_buffer.write(f.read())
                    os.unlink(doc_path)
                
                doc_buffer.seek(0)
                filename = f"{selected_doc}.docx"
                st.download_button(
                    label="📄 下载 Word 格式 (.docx)",
                    data=doc_buffer.getvalue(),
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"生成Word文档时出错: {e}")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 关于")
    st.sidebar.info("制药设备售前文档生成器 v1.0")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 使用说明")
    st.sidebar.markdown("""
    1. 选择设备类型和法规标准（可多选）
    2. （可选）上传自定义模板（支持Excel/Word/Markdown）
    3. 输入URS文本或上传文档
    4. 系统自动智能解析关键需求
    5. 生成所需文档
    6. 预览并下载Markdown或Word格式文档
    """)

if __name__ == "__main__":
    main()
