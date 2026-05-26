import streamlit as st
import json
from datetime import datetime

st.set_page_config(
    page_title="隔离器售前文档生成系统",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_data(key, default=None):
    try:
        data = st.session_state.get(f"local_{key}")
        if data is None:
            data = st.query_params.get(key)
            if data:
                data = json.loads(data)
                st.session_state[f"local_{key}"] = data
        return data if data is not None else default
    except:
        return default

def save_data(key, value):
    st.session_state[f"local_{key}"] = value

def init_session():
    if "urs_text" not in st.session_state:
        st.session_state.urs_text = ""
    if "selected_equipment" not in st.session_state:
        st.session_state.selected_equipment = []
    if "key_params" not in st.session_state:
        st.session_state.key_params = ""
    if "budget_level" not in st.session_state:
        st.session_state.budget_level = "标准型"
    if "language" not in st.session_state:
        st.session_state.language = "中文"
    if "history" not in st.session_state:
        st.session_state.history = load_data("history", [])
    if "customers" not in st.session_state:
        st.session_state.customers = load_data("customers", [])
    if "templates" not in st.session_state:
        st.session_state.templates = load_data("templates", [])
    if "generated_docs" not in st.session_state:
        st.session_state.generated_docs = {"urs": "", "quotation": ""}

def parse_urs(text):
    result = {
        "equipment": [],
        "specs": [],
        "compliance": [],
        "key_points": []
    }
    
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if not line: continue
        
        if '隔离器' in line:
            if '负压' in line:
                result['equipment'].append('单体负压隔离器')
            elif '整线' in line:
                result['equipment'].append('整线隔离器')
            else:
                result['equipment'].append('单体无菌隔离器')
        if 'VHP' in line or '传递窗' in line:
            result['equipment'].append('VHP传递窗')
        
        if 'GMP' in line or 'FDA' in line or 'EU' in line or 'WHO' in line or 'PIC/S' in line:
            result['compliance'].append(line)
        
        if '要求' in line or '规格' in line or '尺寸' in line or '参数' in line:
            result['key_points'].append(line)
    
    result['equipment'] = list(set(result['equipment']))
    return result

def generate_urs_response():
    customer_name = st.session_state.get('customer_name', '')
    project_name = st.session_state.get('project_name', '')
    contact = st.session_state.get('contact', '')
    date_val = st.session_state.get('date')
    date = date_val.strftime('%Y-%m-%d') if hasattr(date_val, 'strftime') else str(date_val) if date_val else datetime.now().strftime('%Y-%m-%d')
    regulations = [r for r in ['中国GMP', 'FDA 21 CFR', 'EU GMP Annex 1', 'WHO GMP', 'PIC/S'] if st.session_state.get(f"reg_{r}")]
    equipment = st.session_state.selected_equipment
    key_points = st.session_state.key_params.split('\n') if st.session_state.key_params else []
    
    content = f"""# 用户需求说明（URS）逐条回复

**客户名称**: {customer_name or '待填写'}  
**项目名称**: {project_name or '待填写'}  
**联系人**: {contact or '待填写'}  
**日期**: {date}  
**设备类型**: {', '.join(equipment) if equipment else '待确认'}  
**适用法规**: {', '.join(regulations) if regulations else '待确认'}

---

## 一、概述

本回复文档针对贵公司提出的设备需求进行逐条响应，确保方案符合相关法规要求。

## 二、URS逐条回复

"""
    
    for i, point in enumerate(key_points[:10] if key_points else ['请输入URS需求'], 1):
        content += f"""### URS-{str(i).zfill(3)} {point}

**回复**: 满足  
**技术说明**: 本设备可完全满足客户该项需求，具体技术方案详见技术规格书。  
**法规依据**: 符合{', '.join(regulations)}相关要求。  
**验证方式**: IQ/OQ/PQ

"""
    
    content += f"""## 三、合规声明

我方保证所提供设备符合上述法规要求，并提供完整的验证文件包。

---

**回复单位**: XX隔离器技术有限公司  
**技术负责人**: 待填写  
**联系电话**: 待填写  
**日期**: {date}"""
    
    return content

def generate_quotation():
    customer_name = st.session_state.get('customer_name', '')
    project_name = st.session_state.get('project_name', '')
    contact = st.session_state.get('contact', '')
    date_val = st.session_state.get('date')
    date = date_val.strftime('%Y-%m-%d') if hasattr(date_val, 'strftime') else str(date_val) if date_val else datetime.now().strftime('%Y-%m-%d')
    equipment = st.session_state.selected_equipment
    budget = st.session_state.budget_level
    regulations = [r for r in ['中国GMP', 'FDA 21 CFR', 'EU GMP Annex 1', 'WHO GMP', 'PIC/S'] if st.session_state.get(f"reg_{r}")]
    
    prices = {
        '单体无菌隔离器': {'经济型': [80, 150], '标准型': [100, 200], '高端型': [180, 320]},
        'VHP传递窗': {'经济型': [30, 60], '标准型': [40, 80], '高端型': [80, 150]},
        '整线隔离器': {'经济型': [300, 600], '标准型': [400, 800], '高端型': [700, 1500]},
        '单体负压隔离器': {'经济型': [100, 200], '标准型': [120, 250], '高端型': [250, 450]}
    }
    
    eq = equipment[0] if equipment else '单体无菌隔离器'
    price_range = prices[eq][budget]
    
    content = f"""# 快速报价单

**报价编号**: QT-{datetime.now().strftime('%Y%m')}-{str(hash(datetime.now())).strip('-')[:3]}  
**日期**: {date}  
**有效期**: 30天  
**客户名称**: {customer_name or '待填写'}  
**项目名称**: {project_name or '待填写'}  
**设备类型**: {eq}  
**配置等级**: {budget}  
**适用法规**: {', '.join(regulations)}

---

## A. 设备概述

{equipment_desc(eq)}

## B. 关键技术参数

| 参数 | 配置 |
|------|------|
| 灭菌效果 | SAL 10⁻⁶ |
| 残气浓度 | <1ppm |
| 材质 | 316L不锈钢 |

## C. 报价明细

| 项目 | 金额（万元） |
|------|--------------|
| 设备本体 | {price_range[0]} - {price_range[1]} |
| 安装调试 | 含 |
| 验证服务 | 含 |
| 技术培训 | 含 |
| **总计** | **{price_range[0]} - {price_range[1]}** |

## D. 配置清单

- 主机系统 ×1
- HEPA过滤器 ×2
- 备用手套 ×2副
- 验证文件包 ×1

## E. 售后服务

| 项目 | 内容 |
|------|------|
| 质保期 | 12个月 |
| 响应时间 | 48小时 |

---

**供应商**: XX隔离器技术有限公司  
**联系人**: {contact or '待填写'}  
**日期**: {date}
"""
    
    return content

def equipment_desc(eq):
    descs = {
        '单体无菌隔离器': '无菌分装、无菌检测、称量操作的理想选择，正压运行，ISO 5级洁净度。',
        'VHP传递窗': '物料/工具VHP灭菌传递，双门互锁，灭菌效果≥6-log。',
        '整线隔离器': '灌装+轧盖+称重全线隔离，适用于无菌制剂生产线。',
        '单体负压隔离器': '有毒/高活性药品OEL防护，负压运行，OEL控制<1μg/m³。'
    }
    return descs.get(eq, '')

def main():
    init_session()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 📋 客户基本信息")
        st.text_input("客户公司名称", key="customer_name")
        st.text_input("项目名称", key="project_name")
        
        row1 = st.columns(2)
        row1[0].text_input("联系人", key="contact")
        row1[1].date_input("日期", key="date", value=datetime.now())
        
        st.markdown("**适用法规（多选）**")
        regs = ['中国GMP', 'FDA 21 CFR', 'EU GMP Annex 1', 'WHO GMP', 'PIC/S']
        for reg in regs:
            st.checkbox(reg, key=f"reg_{reg}", value=True if reg == '中国GMP' else False)
        
        st.text_input("供应商名称", value="XX隔离器技术有限公司", key="supplier_name")
        
        st.markdown("---")
        st.markdown("### 📝 客户URS/询盘输入")
        st.text_area("请粘贴客户URS内容...", height=150, key="urs_text",
                     placeholder="1. 设备需满足无菌隔离要求，正压运行\n2. 操作区洁净度ISO 5级\n3. VHP灭菌，灭菌效果≥6-log")
        
        row2 = st.columns(3)
        if row2[0].button("🔍 智能解析"):
            parsed = parse_urs(st.session_state.urs_text)
            st.session_state.selected_equipment = parsed['equipment']
            st.session_state.key_params = '\n'.join(parsed['key_points'])
            st.success(f"解析完成！识别到: {', '.join(parsed['equipment'])}")
        
        if row2[1].button("📄 加载示例"):
            st.session_state.urs_text = """1. VHP灭菌传递窗，双门互锁
2. 灭菌循环可调（浓度、时间、温度）
3. 灭菌效果≥6-log SAL
4. VHP残气排除至<1ppm
5. 内腔尺寸不小于L800×W800×H900mm
6. 需满足中国GMP及EU GMP Annex 1要求"""
        
        if row2[2].button("🗑 清空"):
            st.session_state.urs_text = ""
            st.session_state.selected_equipment = []
            st.session_state.key_params = ""
        
        with st.expander("⚙️ 手动调整", expanded=True):
            st.markdown("**设备类型确认/修正（可多选）**")
            eqs = ['单体无菌隔离器', 'VHP传递窗', '整线隔离器', '单体负压隔离器']
            for eq in eqs:
                st.checkbox(eq, key=f"eq_{eq}", 
                           value=True if eq in st.session_state.selected_equipment else False)
            
            st.text_area("关键参数修正", height=100, key="key_params",
                        placeholder="解析URS后将自动填充，也可手动输入")
            
            st.selectbox("预算级别", ['经济型', '标准型', '高端型'], key="budget_level")
            st.selectbox("语言", ['中文', 'English', '中英双语'], key="language")
        
        st.markdown("---")
        st.markdown("### 💾 保存与加载")
        
        row3 = st.columns(2)
        if row3[0].button("💾 保存为报价单"):
            record = {
                'customer': st.session_state.customer_name,
                'equipment': st.session_state.selected_equipment,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'budget': st.session_state.budget_level
            }
            st.session_state.history.append(record)
            save_data("history", st.session_state.history)
            st.success("保存成功！")
        
        template_name = st.text_input("模板名称")
        if row3[1].button("📑 保存为模板"):
            st.session_state.templates.append({
                'name': template_name,
                'content': st.session_state.urs_text,
                'date': datetime.now().strftime('%Y-%m-%d')
            })
            save_data("templates", st.session_state.templates)
            st.success("模板保存成功！")
        
        st.selectbox("加载模板", [t['name'] for t in st.session_state.templates] + [''], key="load_template")
        st.selectbox("加载客户", [c['name'] for c in st.session_state.customers] + [''], key="load_customer")
        
        with st.expander("📁 历史报价单", expanded=False):
            if st.session_state.history:
                for record in st.session_state.history[:5]:
                    st.markdown(f"{record['date']} | {', '.join(record['equipment'])} | {record.get('customer', '')}")
            else:
                st.info("暂无历史报价单")
        
        with st.expander("👥 客户档案", expanded=False):
            if st.session_state.customers:
                for cust in st.session_state.customers[:5]:
                    st.markdown(f"🏢 {cust['name']} | {cust.get('contact', '')}")
            else:
                st.info("暂无客户记录")
        
        if st.button("🚀 生成文档（URS回复 + 快速报价）", use_container_width=True, type="primary"):
            st.session_state.generated_docs['urs'] = generate_urs_response()
            st.session_state.generated_docs['quotation'] = generate_quotation()
            st.success("文档生成成功！")
    
    with col2:
        tabs = st.tabs(["📋 URS逐条回复", "💰 快速报价单", "📚 模板库"])
        
        with tabs[0]:
            st.markdown("### 📋 URS逐条回复")
            if st.session_state.generated_docs['urs']:
                st.markdown(st.session_state.generated_docs['urs'])
            else:
                st.info("请在左侧输入客户URS内容并点击\"智能解析\"，然后点击\"生成文档\"")
        
        with tabs[1]:
            st.markdown("### 💰 快速报价单")
            if st.session_state.generated_docs['quotation']:
                st.markdown(st.session_state.generated_docs['quotation'])
            else:
                st.info("请在左侧输入信息并点击\"生成文档\"")
        
        with tabs[2]:
            st.markdown("### 📚 模板库")
            
            default_templates = [
                {
                    'name': '负压隔离器询盘（高活性药品）',
                    'equipment': '单体负压隔离器',
                    'regulations': '中国GMP、FDA 21 CFR',
                    'content': """1. 负压隔离器，用于高活性药品操作
2. OEL控制目标<1μg/m³
3. 双重HEPA排风过滤，在线扫描检漏
4. 袋进袋出(BIBO)过滤器更换
5. 工作区尺寸L1500×D900×H900mm"""
                },
                {
                    'name': 'VHP传递窗询盘',
                    'equipment': 'VHP传递窗',
                    'regulations': '中国GMP',
                    'content': """1. VHP灭菌传递窗，双门互锁
2. 灭菌循环可调（浓度、时间、温度）
3. 灭菌效果≥6-log SAL
4. VHP残气排除至<1ppm
5. 内腔尺寸不小于L800×W800×H900mm"""
                },
                {
                    'name': '标准无菌隔离器询盘',
                    'equipment': '单体无菌隔离器',
                    'regulations': '中国GMP、EU GMP',
                    'content': """1. 设备需满足无菌隔离要求，正压运行
2. 操作区洁净度ISO 5级
3. VHP灭菌，灭菌效果≥6-log
4. 配备手套检漏系统
5. 操作区尺寸不小于L1200×D800×H900mm"""
                }
            ]
            
            for template in default_templates:
                with st.expander(f"📄 {template['name']}"):
                    st.markdown(f"**设备类型**: {template['equipment']}")
                    st.markdown(f"**适用法规**: {template['regulations']}")
                    st.markdown(f"**内容**: \n{template['content']}")
                    if st.button(f"使用此模板", key=f"use_{template['name']}"):
                        st.session_state.urs_text = template['content']
                        st.session_state.selected_equipment = [template['equipment']]
                        st.success("模板已加载！")
        
        row4 = st.columns(2)
        if row4[0].button("📋 复制全文"):
            full_text = st.session_state.generated_docs['urs'] + '\n\n---\n\n' + st.session_state.generated_docs['quotation']
            st.write(full_text)
        
        if row4[1].button("🖨 打印/导出PDF"):
            st.write("打印功能已准备就绪")

if __name__ == "__main__":
    main()
