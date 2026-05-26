import streamlit as st
import os
from io import BytesIO
from datetime import datetime
import json
from utils.document_utils import parse_uploaded_file, extract_requirements, fill_template

st.set_page_config(
    page_title="制药隔离器售前文档生成器",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_from_local_storage(key, default=None):
    try:
        data = st.session_state.get(f"local_{key}")
        if data is None:
            data_str = st.query_params.get(key)
            if data_str:
                data = json.loads(data_str)
                st.session_state[f"local_{key}"] = data
        return data if data is not None else default
    except:
        return default

def save_to_local_storage(key, value):
    st.session_state[f"local_{key}"] = value

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
    if "custom_template_files" not in st.session_state:
        st.session_state.custom_template_files = {
            "urs_response": None,
            "technical_spec": None,
            "quotation": None
        }
    if "history" not in st.session_state:
        saved_history = load_from_local_storage("history", [])
        st.session_state.history = saved_history
    if "customers" not in st.session_state:
        saved_customers = load_from_local_storage("customers", [])
        st.session_state.customers = saved_customers
    if "templates" not in st.session_state:
        saved_templates = load_from_local_storage("templates", {})
        st.session_state.templates = saved_templates

def main():
    init_session_state()
    
    st.title("🏭 制药隔离器售前文档生成器")
    st.markdown("---")
    
    tabs = st.tabs(["📝 URS处理", "💰 快速报价", "📊 历史记录", "👥 客户档案", "📁 模板库"])
    
    with tabs[0]:
        show_urs_processing()
    
    with tabs[1]:
        show_quick_quotation()
    
    with tabs[2]:
        show_history()
    
    with tabs[3]:
        show_customers()
    
    with tabs[4]:
        show_templates()

def show_urs_processing():
    st.markdown("### 📝 URS智能解析与逐条回复")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 选择设备类型")
        equipment_type = st.selectbox(
            "设备类型",
            ["单体无菌隔离器", "VHP传递窗", "整线隔离器", "单体负压隔离器"],
            index=0,
            key="urs_equipment"
        )
        
        st.markdown("#### 选择法规体系（可多选）")
        regulations = st.multiselect(
            "法规标准",
            ["中国GMP 2010版", "FDA 21 CFR Part 11", "EU GMP Annex 1", "WHO GMP", "PIC/S GMP"],
            default=["中国GMP 2010版"],
            key="urs_regulations"
        )
    
    with col2:
        st.markdown("#### URS文档输入")
        urs_input = st.text_area(
            "粘贴URS内容",
            height=200,
            placeholder="粘贴客户URS文档内容...\n\n例如：\n1. 设备要求：单体无菌隔离器\n2. 尺寸要求：1200×800×1000mm\n3. 法规要求：符合中国GMP",
            key="urs_text_input"
        )
        
        uploaded_file = st.file_uploader(
            "或上传URS文件（PDF/Word/Excel/TXT）",
            type=["pdf", "docx", "xlsx", "txt"]
        )
        if uploaded_file:
            text, _ = parse_uploaded_file(uploaded_file)
            urs_input = text
    
    if urs_input.strip():
        with st.spinner("正在智能解析URS..."):
            requirements = extract_requirements(urs_input)
        
        st.markdown("---")
        st.markdown("### 🤖 智能解析结果")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("📦 设备类型")
            if requirements["equipment_type"]:
                st.success(f"✅ 检测到: **{requirements['equipment_type']}**")
            else:
                st.info(f"当前选择: **{equipment_type}**")
        
        with col2:
            st.subheader("📋 合规要求")
            if requirements["compliance"]:
                st.markdown(f"检测到 {len(requirements['compliance'])} 条合规要求")
            else:
                st.info(f"已选法规: {', '.join(regulations)}")
        
        with col3:
            st.subheader("🎯 关键需求")
            st.markdown(f"提取到 {len(requirements['key_points'])} 条关键需求")
        
        if st.button("📄 生成URS逐条回复", type="primary", use_container_width=True):
            generate_urs_response(equipment_type, regulations, requirements, urs_input)

def show_quick_quotation():
    st.markdown("### 💰 快速报价单生成")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        equipment_type = st.selectbox(
            "设备类型",
            ["单体无菌隔离器", "VHP传递窗", "整线隔离器", "单体负压隔离器"],
            index=0,
            key="quote_equipment"
        )
        
        regulations = st.multiselect(
            "法规标准",
            ["中国GMP 2010版", "FDA 21 CFR Part 11", "EU GMP Annex 1", "WHO GMP", "PIC/S GMP"],
            default=["中国GMP 2010版"],
            key="quote_regulations"
        )
        
        config_level = st.select_slider(
            "配置等级",
            options=["基础", "标准", "高级"],
            value="标准",
            key="quote_config"
        )
    
    with col2:
        customer_name = st.text_input("客户名称")
        project_name = st.text_input("项目名称")
        contact_person = st.text_input("联系人")
    
    if st.button("✨ 一键生成报价单", type="primary", use_container_width=True):
        generate_quotation(equipment_type, regulations, config_level, customer_name, project_name, contact_person)

def show_history():
    st.markdown("### 📊 历史记录")
    
    if not st.session_state.history:
        st.info("暂无历史记录")
        return
    
    for i, record in enumerate(reversed(st.session_state.history), 1):
        with st.expander(f"📄 {record['type']} - {record['equipment']} - {record['date']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**客户**: {record.get('customer', '未知')}")
                st.markdown(f"**法规**: {record.get('regulations', '')}")
            with col2:
                st.markdown(f"**配置**: {record.get('config', '标准')}")
                st.markdown(f"**金额**: {record.get('amount', '')}")
            
            if "content" in record:
                st.download_button(
                    "下载文档",
                    data=record["content"].encode("utf-8"),
                    file_name=f"document_{i}.md"
                )

def show_customers():
    st.markdown("### 👥 客户档案")
    
    tab1, tab2 = st.tabs(["客户列表", "新建客户"])
    
    with tab1:
        if not st.session_state.customers:
            st.info("暂无客户档案")
        else:
            for customer in st.session_state.customers:
                with st.expander(f"🏢 {customer['name']}"):
                    st.markdown(f"**联系人**: {customer.get('contact', '')}")
                    st.markdown(f"**电话**: {customer.get('phone', '')}")
                    st.markdown(f"**邮箱**: {customer.get('email', '')}")
                    st.markdown(f"**备注**: {customer.get('notes', '')}")
    
    with tab2:
        name = st.text_input("客户名称", key="customer_name")
        contact = st.text_input("联系人", key="customer_contact")
        phone = st.text_input("联系电话", key="customer_phone")
        email = st.text_input("邮箱", key="customer_email")
        notes = st.text_area("备注", key="customer_notes")
        
        if st.button("保存客户", type="primary", key="save_customer_btn"):
            customer = {
                "name": name,
                "contact": contact,
                "phone": phone,
                "email": email,
                "notes": notes,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.session_state.customers.append(customer)
            save_to_local_storage("customers", st.session_state.customers)
            st.success("客户保存成功")

def show_templates():
    st.markdown("### 📁 模板库")
    
    st.markdown("#### 占位符说明")
    placeholders = [
        "{设备类型}", "{法规标准}", "{生成日期}", "{年份}",
        "{URS文档编号}", "{技术文档编号}", "{报价文档编号}",
        "{关键需求点}", "{技术规格}", "{客户名称}", "{项目名称}"
    ]
    
    st.code("\n".join(placeholders))
    
    uploaded_template = st.file_uploader("上传自定义模板", type=["docx", "xlsx", "md", "txt"])
    if uploaded_template:
        template_name = st.text_input("模板名称")
        if st.button("保存模板"):
            st.session_state.templates[template_name] = uploaded_template.read()
            save_to_local_storage("templates", st.session_state.templates)
            st.success("模板保存成功")
    
    if st.session_state.templates:
        st.markdown("#### 已保存模板")
        for name in st.session_state.templates.keys():
            st.write(f"- {name}")

def generate_urs_response(equipment_type, regulations, requirements, urs_text):
    regulation_text = ", ".join(regulations)
    doc_number = datetime.now().strftime("%Y%m%d")
    
    content = f"""# {equipment_type} - URS逐条回复

**文档编号**: PHARMA-URS-{doc_number}
**生成日期**: {datetime.now().strftime("%Y年%m月%d日")}
**适用法规**: {regulation_text}

---

## 一、概述

本回复文档针对贵公司提出的{equipment_type}用户需求说明（URS）进行逐条响应，确保方案符合{regulation_text}要求。

## 二、URS逐条回复

"""
    
    for i, point in enumerate(requirements["key_points"], 1):
        content += f"""### {i}. {point}

**我方响应**: 我方完全理解并满足此项要求，将在IQ/OQ/PQ验证中予以确认。
**法规依据**: 符合{regulation_text}相关要求。
**验证方式**: IQ/OQ/PQ

"""
    
    content += """---

## 三、合规声明

我方保证所提供设备符合上述法规要求，并提供完整的验证文件包。

**回复单位**: [贵公司名称]
**技术负责人**: [负责人姓名]
**联系电话**: [联系电话]
**日期**: """ + datetime.now().strftime("%Y年%m月%d日")
    
    st.session_state.generated_documents = {"urs_response": content}
    
    with st.expander("📖 预览文档", expanded=True):
        st.markdown(content)
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("📝 复制到剪贴板", content, "text/plain")
    with col2:
        st.download_button("📄 下载Markdown", content.encode("utf-8"), f"URS回复_{doc_number}.md")
    
    save_to_history("URS回复", equipment_type, regulations, content=content)

def generate_quotation(equipment_type, regulations, config_level, customer_name, project_name, contact_person):
    prices = {
        "单体无菌隔离器": {"基础": 300000, "标准": 500000, "高级": 800000},
        "VHP传递窗": {"基础": 150000, "标准": 250000, "高级": 400000},
        "整线隔离器": {"基础": 1500000, "标准": 2500000, "高级": 4000000},
        "单体负压隔离器": {"基础": 400000, "标准": 600000, "高级": 1000000}
    }
    
    price = prices[equipment_type][config_level]
    tax = price * 0.13
    total = price + tax
    
    doc_number = datetime.now().strftime("%Y%m%d")
    
    content = f"""# {equipment_type} - 报价单

**报价编号**: PHARMA-QUOTE-{doc_number}
**报价日期**: {datetime.now().strftime("%Y年%m月%d日")}
**有效期**: 30天

---

## 客户信息

| 项目 | 内容 |
|------|------|
| 客户名称 | {customer_name} |
| 项目名称 | {project_name} |
| 联系人 | {contact_person} |
| 设备类型 | {equipment_type} |
| 配置等级 | {config_level} |
| 适用法规 | {', '.join(regulations)} |

---

## 报价明细

| 项目 | 金额（元） |
|------|------------|
| 设备主机 | ¥{price:,} |
| 标准配件 | ¥{int(price * 0.15):,} |
| 运输保险 | ¥{int(price * 0.03):,} |
| 安装调试 | ¥{int(price * 0.08):,} |
| 培训服务 | ¥{int(price * 0.02):,} |
| **小计** | **¥{int(price * 1.28):,}** |
| 增值税(13%) | ¥{int(tax):,} |
| **总计** | **¥{int(total * 1.28):,}** |

---

## 配置清单

**{config_level}配置包含**:
- 主机系统 ×1
- HEPA过滤器 ×2
- 备用手套 ×2副
- 专用工具包 ×1
- 操作手册 ×1
- 验证文件包 ×1

---

## 商务条款

- **付款方式**: 预付款30%，发货款60%，质保金10%
- **交货期**: 收到预付款后45-60天
- **质保期**: 12个月

**报价单位**: [贵公司名称]
**联系人**: [联系人姓名]
**联系电话**: [联系电话]
"""
    
    st.session_state.generated_documents = {"quotation": content}
    
    with st.expander("📖 预览报价单", expanded=True):
        st.markdown(content)
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("📝 复制到剪贴板", content, "text/plain")
    with col2:
        st.download_button("📄 下载Markdown", content.encode("utf-8"), f"报价单_{doc_number}.md")
    
    save_to_history("报价单", equipment_type, regulations, config_level, f"¥{int(total * 1.28):,}", customer_name, content=content)

def save_to_history(doc_type, equipment, regulations, config="标准", amount="", customer="", content=""):
    record = {
        "type": doc_type,
        "equipment": equipment,
        "regulations": ", ".join(regulations),
        "config": config,
        "amount": amount,
        "customer": customer,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "content": content
    }
    st.session_state.history.append(record)
    save_to_local_storage("history", st.session_state.history)

if __name__ == "__main__":
    main()
