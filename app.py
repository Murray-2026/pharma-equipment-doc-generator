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
    
    st.markdown("#### 基本信息")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        quote_number = st.text_input("报价单编号", value=f"QT-{datetime.now().strftime('%Y%m')}-{str(hash(datetime.now())).strip('-')[:3]}", key="quote_number")
    with col2:
        quote_date = st.date_input("日期", value=datetime.now(), key="quote_date")
    with col3:
        valid_until = st.date_input("有效期至", key="quote_valid_until")
    with col4:
        contact_person = st.text_input("联系人", key="quote_contact")
    
    st.markdown("#### 客户与供应商信息")
    col1, col2 = st.columns(2)
    with col1:
        customer_name = st.text_input("客户名称", key="quote_customer")
        project_name = st.text_input("项目名称", key="quote_project")
    with col2:
        supplier_name = st.text_input("供应商名称", value="XX隔离器技术有限公司", key="quote_supplier")
        equipment_model = st.text_input("设备型号", key="quote_model")
    
    st.markdown("#### 设备与法规信息")
    col1, col2, col3 = st.columns(3)
    with col1:
        equipment_type = st.selectbox(
            "设备类型",
            ["单体无菌隔离器", "VHP传递窗", "整线隔离器", "单体负压隔离器"],
            index=0,
            key="quote_equipment"
        )
    with col2:
        config_level = st.select_slider(
            "配置等级",
            options=["基础", "标准", "高级"],
            value="标准",
            key="quote_config"
        )
    with col3:
        regulations = st.multiselect(
            "适用法规",
            ["中国GMP", "FDA 21 CFR", "EU GMP Annex 1", "WHO GMP", "PIC/S"],
            default=["中国GMP", "EU GMP Annex 1", "WHO GMP"],
            key="quote_regulations"
        )
    
    st.markdown("#### 技术参数确认")
    with st.expander("展开技术参数", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            inner_dimensions = st.text_input("内部尺寸", value="L600×D600×H600mm", key="tech_dimensions")
        with col2:
            vhp_concentration = st.text_input("VHP浓度范围", value="2-6 mg/L", key="tech_vhp")
        with col3:
            sterilization_time = st.text_input("灭菌时间", value="60-120min", key="tech_time")
        with col4:
            temperature_range = st.text_input("灭菌温度范围", value="25-45°C", key="tech_temp")
    
    st.markdown("#### 服务选项")
    col1, col2, col3 = st.columns(3)
    with col1:
        include_installation = st.checkbox("包含安装调试", value=True, key="service_install")
    with col2:
        include_validation = st.checkbox("包含IQ/OQ/PQ验证", value=True, key="service_validation")
    with col3:
        include_training = st.checkbox("包含技术培训", value=True, key="service_training")
    
    if st.button("✨ 一键生成报价单", type="primary", use_container_width=True):
        generate_quotation(equipment_type, regulations, config_level, customer_name, project_name, contact_person,
                          quote_number, quote_date, valid_until, supplier_name, equipment_model,
                          inner_dimensions, vhp_concentration, sterilization_time, temperature_range,
                          include_installation, include_validation, include_training)

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

def generate_quotation(equipment_type, regulations, config_level, customer_name, project_name, contact_person,
                      quote_number="", quote_date=datetime.now(), valid_until=None, supplier_name="XX隔离器技术有限公司", 
                      equipment_model="", inner_dimensions="", vhp_concentration="", sterilization_time="", 
                      temperature_range="", include_installation=True, include_validation=True, include_training=True):
    
    prices = {
        "单体无菌隔离器": {"基础": [80, 150], "标准": [100, 200], "高级": [180, 320]},
        "VHP传递窗": {"基础": [30, 60], "标准": [40, 80], "高级": [80, 150]},
        "整线隔离器": {"基础": [300, 600], "标准": [400, 800], "高级": [700, 1500]},
        "单体负压隔离器": {"基础": [100, 200], "标准": [120, 250], "高级": [250, 450]}
    }
    
    price_range = prices[equipment_type][config_level]
    base_price = (price_range[0] + price_range[1]) / 2
    
    quote_date_str = quote_date.strftime("%Y-%m-%d") if hasattr(quote_date, 'strftime') else str(quote_date)
    valid_until_str = valid_until.strftime("%Y-%m-%d") if valid_until else ""
    
    content = f"""# 快速报价单
## Quick Quotation

---

## 报价单信息

| 项目 | 内容 |
|------|------|
| 报价单编号 | {quote_number} |
| 日期 | {quote_date_str} |
| 有效期至 | {valid_until_str} |
| 客户名称 | {customer_name or '待填写'} |
| 项目名称 | {project_name or '待填写'} |
| 供应商 | {supplier_name} |
| 设备类型 | {equipment_type} |
| 设备型号 | {equipment_model or 'VHP Pass-Through (Airlock) Chamber'} |
| 适用法规 | {', '.join(regulations)} |

---

## A. 设备概述

{equipment_type}是一种基于汽化过氧化氢（VHP）灭菌原理的物料传递设备，用于洁净区与非洁净区（或不同洁净等级区域）之间的物料、工具传递。设备采用双门互锁安全设计，配置集成式VHP发生器，灭菌循环可编程控制（除湿-灭菌-排残-通风），灭菌效果达到SAL 10⁻⁶，残气经催化分解后H₂O₂残留浓度<1ppm，保障操作人员安全，适用于制药企业物料、工器具、耗材的在线灭菌传递。

### 系统描述

**工作原理**: {equipment_type}传递窗由两个互锁舱室组成，操作时仅一侧门可开启。物料放入后关闭门，启动VHP灭菌循环（除湿→灭菌→排残）。VHP通过雾化过氧化氢，均匀分布整个舱室，完成后经催化分解残气至安全浓度，方可开启对侧门取出物料。双门互锁系统确保两侧门不同时开启，防止交叉污染。

---

## B. 关键技术参数

| 参数项目 | 标准配置 | 高级配置 |
|----------|----------|----------|
| 传递舱内尺寸 | {inner_dimensions or 'L600×D600×H600mm'} | L800×D800×H800mm |
| VHP浓度范围 | {vhp_concentration or '2-6 mg/L'} | 2-8 mg/L |
| 灭菌时间 | {sterilization_time or '60-120min'} | 60-180min |
| 灭菌温度范围 | {temperature_range or '25-45°C'} | 25-50°C |
| 灭菌效果 | SAL 10⁻⁶ | SAL 10⁻⁶ |
| 残气浓度 | <1ppm | <1ppm |
| 双门互锁 | 机械+电气联锁 | 机械+PLC三重联锁 |
| 内壁材质 | 316L不锈钢 Ra≤0.4μm | 316L不锈钢 Ra≤0.4μm |
| 控制系统 | PLC+7寸触摸屏 | PLC+SCADA+10寸触摸屏 |
| 数据记录 | 数据自动记录 | 完整审计追踪记录 |

---

## C. 报价明细

### C.1 {config_level}方案报价

| 序号 | 项目 | 金额（万元） | 备注 |
|------|------|--------------|------|
| 1 | 设备本体 | {base_price * 0.7:.1f} | 含主体结构、手套、视窗等 |
| 2 | 安装调试 | {base_price * 0.08:.1f if include_installation else 0} | 含现场安装、调试、开机验证 |
| 3 | 验证服务（IQ/OQ/PQ） | {base_price * 0.1:.1f if include_validation else 0} | 含验证方案编制及执行 |
| 4 | 培训服务 | {base_price * 0.02:.1f if include_training else 0} | 操作+维护培训，{3 if config_level == '标准' else 5}天 |
| 5 | 备件包（首年） | {base_price * 0.02:.1f} | 易损件及推荐备件 |
| 6 | 技术文件包 | {base_price * 0.02:.1f} | 含手册、图纸、证书 |
| 7 | 国内运输+保险 | {base_price * 0.06:.1f} | 含运输一切险 |
| 8 | **{config_level}方案合计** | **{(base_price * 1.1).round(1)}** | 含13%增值税 |

---

## D. 配置清单

### {config_level}配置包含:
- {equipment_type}主机系统 ×1
- HEPA过滤器（H14级） ×2
- 备用手套（丁腈） ×2副
- 专用工具包 ×1
- 操作手册（中文/英文） ×1
- 验证文件包（IQ/OQ/PQ） ×1
- 备件清单及报价 ×1

---

## E. 交货周期

| 方案 | 预计周期 | 说明 |
|------|----------|------|
| {config_level}方案 | {16 if config_level == '标准' else 20}-28周 | 自合同签订及预付款到账之日起计算；含额外系统集成交付与调试时间 |

> *交货周期受客户现场准备情况影响，如现场不具备安装条件可能相应顺延。

---

## F. 售后服务条款

| 项目 | 标准方案 | 高级方案 |
|------|----------|----------|
| 质保期 | 12个月（自SAT验收签署之日起） | 24个月（自SAT验收签署之日起） |
| 远程响应时间 | 48小时内 | 24小时内 |
| 现场响应时间 | 48小时内 | 24小时内 |
| 年度保养 | 1次/年 | 2次/年 |
| 软件升级 | 质保期内免费 | 质保期内免费+质保期后3年优惠 |
| 设备备件 | 设备停产10年 | 设备停产10年 |
| 技术培训 | 3天（操作+维护） | 5天（操作+维护+验证） |

---

## 声明

1. 本报价有效期为30天，逾期价格可能调整。
2. 本报价不含土建、公用工程接口以外的工作。
3. 最终价格以双方签订的正式合同为准。
4. 如客户有重大变更，供应商保留调整报价的权利。

**报价单位**: {supplier_name}  
**联系人**: {contact_person or '待填写'}  
**日期**: {quote_date_str}
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
