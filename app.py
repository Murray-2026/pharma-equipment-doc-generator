import streamlit as st
import os
from io import BytesIO
from datetime import datetime
from utils.document_utils import parse_uploaded_file
from utils.generator import DocumentGenerator

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
    
    st.sidebar.subheader("法规标准")
    regulation = st.sidebar.selectbox(
        "选择目标法规",
        ["中国GMP", "FDA", "EU GMP", "PIC/S"],
        index=0
    )
    
    st.markdown("### 步骤 1: 上传客户文档")
    uploaded_file = st.file_uploader(
        "上传客户询盘或URS文档（PDF/Word/文本）",
        type=["pdf", "docx", "doc", "txt"]
    )
    
    requirements = None
    text = ""
    
    if uploaded_file is not None:
        st.success(f"已成功上传文件: {uploaded_file.name}")
        
        with st.spinner("正在解析文档..."):
            text, requirements = parse_uploaded_file(uploaded_file)
        
        st.markdown("### 提取的信息")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("设备类型")
            if requirements["equipment_type"]:
                st.info(f"检测到: {requirements['equipment_type']}")
            else:
                st.warning("未检测到明确的设备类型，请在左侧手动选择")
            
            st.subheader("合规要求")
            if requirements["compliance"]:
                for req in requirements["compliance"][:5]:
                    st.markdown(f"- {req}")
            else:
                st.info("未提取到明确的合规要求")
        
        with col2:
            st.subheader("技术规格")
            if requirements["specifications"]:
                for spec in requirements["specifications"][:5]:
                    st.markdown(f"- {spec}")
            else:
                st.info("未提取到明确的技术规格")
            
            st.subheader("关键需求点")
            if requirements["key_points"]:
                for point in requirements["key_points"][:5]:
                    st.markdown(f"- {point}")
            else:
                st.info("未提取到明确的需求点")
        
        with st.expander("查看完整文档内容"):
            st.text_area("文档内容", text, height=300)
    
    st.markdown("---")
    st.markdown("### 步骤 2: 生成文档")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 生成URS回复", use_container_width=True):
            with st.spinner("正在生成URS回复..."):
                generator = DocumentGenerator(equipment_type, regulation)
                st.session_state.generated_documents = {
                    "urs_response": generator.generate_urs_response(requirements)
                }
            st.success("URS回复生成成功！")
    
    with col2:
        if st.button("📋 生成技术方案", use_container_width=True):
            with st.spinner("正在生成技术方案..."):
                generator = DocumentGenerator(equipment_type, regulation)
                st.session_state.generated_documents = {
                    "technical_spec": generator.generate_technical_spec()
                }
            st.success("技术方案生成成功！")
    
    with col3:
        if st.button("💰 生成报价文档", use_container_width=True):
            with st.spinner("正在生成报价文档..."):
                generator = DocumentGenerator(equipment_type, regulation)
                st.session_state.generated_documents = {
                    "quotation_basic": generator.generate_quotation("basic"),
                    "quotation_standard": generator.generate_quotation("standard"),
                    "quotation_premium": generator.generate_quotation("premium")
                }
            st.success("报价文档生成成功！")
    
    if st.button("✨ 一键生成全部文档", type="primary", use_container_width=True):
        with st.spinner("正在生成全套文档..."):
            generator = DocumentGenerator(equipment_type, regulation)
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
                label="下载 Markdown 格式",
                data=content.encode("utf-8"),
                file_name=filename,
                mime="text/markdown",
                use_container_width=True
            )
        
        with col2:
            generator = DocumentGenerator(equipment_type, regulation)
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
                    label="下载 Word 格式",
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
    1. 选择设备类型和法规标准
    2. 上传客户询盘或URS文档
    3. 查看提取的信息
    4. 生成所需文档
    5. 预览和下载文档
    """)

if __name__ == "__main__":
    main()
