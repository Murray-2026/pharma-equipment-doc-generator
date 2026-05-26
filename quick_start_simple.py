
import streamlit as st
import os
from datetime import datetime

# 设置页面配置
st.set_page_config(
    page_title="制药设备售前文档生成器",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 应用标题
st.title("🏭 制药设备售前文档生成器")
st.markdown("---")

# 侧边栏配置
st.sidebar.title("配置设置")

# 设备类型选择
equipment_type = st.sidebar.selectbox(
    "选择设备类型",
    ["单体无菌隔离器", "VHP传递窗", "整线隔离器", "单体负压隔离器"],
    index=0
)

# 法规标准选择
regulation = st.sidebar.selectbox(
    "选择目标法规",
    ["中国GMP", "FDA", "EU GMP", "PIC/S"],
    index=0
)

# 主界面内容
st.markdown("### 📄 设备信息")
st.info(f"您选择的设备：**{equipment_type}**")
st.info(f"适用法规标准：**{regulation}**")

st.markdown("---")

# 文档生成部分
st.markdown("### 🚀 文档生成")
st.write("选择您要生成的文档类型：")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📋 生成URS回复", use_container_width=True):
        st.success(f"✅ URS回复文档生成成功！")
        st.info("文档内容预览：")
        st.markdown(f"""
        # {equipment_type} - URS逐条回复
        
        **生成日期：{datetime.now().strftime('%Y年%m月%d日')}**
        
        ## 概述
        感谢贵公司对我们{equipment_type}的关注！
        
        ## 法规符合
        本设备完全符合{regulation}要求。
        
        ## 技术规格
        - 材质：316L不锈钢
        - 表面粗糙度：Ra ≤ 0.8μm
        - 洁净度：ISO 5级
        
        *（完整功能版本包含更详细的内容和模板）*
        """)

with col2:
    if st.button("📘 生成技术方案", use_container_width=True):
        st.success(f"✅ 技术方案文档生成成功！")
        st.info("文档内容预览：")
        st.markdown(f"""
        # {equipment_type} - 技术方案
        
        **适用法规：{regulation}**
        
        ## 设备概述
        {equipment_type}是专为制药行业设计的高端设备。
        
        ## 技术参数
        - 材质：316L不锈钢
        - 控制系统：PLC + 触摸屏
        - 安全认证：符合{regulation}
        
        ## 配置清单
        - 主机 1套
        - 标准配件 1套
        
        *（完整功能版本包含更详细的内容和模板）*
        """)

with col3:
    if st.button("💰 生成报价单", use_container_width=True):
        st.success(f"✅ 报价文档生成成功！")
        st.info("文档内容预览：")
        st.markdown(f"""
        # {equipment_type} - 报价单
        
        **报价日期：{datetime.now().strftime('%Y年%m月%d日')}**
        
        ## 方案配置
        ### 基础配置：¥300,000 - ¥400,000
        ### 标准配置：¥500,000 - ¥600,000
        ### 高级配置：¥800,000 - ¥1,000,000
        
        ## 包含服务
        - 安装调试
        - 操作培训
        - 12个月质保
        
        *（完整功能版本包含更详细的报价和配置清单）*
        """)

st.markdown("---")

# 关于和帮助
st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 使用说明")
st.sidebar.info("1. 在侧边栏选择设备类型和法规标准\n2. 点击相应按钮生成文档\n3. 查看生成的文档内容\n\n(完整功能版本支持文档上传解析、Word导出和GitHub集成！)")

st.sidebar.markdown("### 📚 关于")
st.sidebar.info("制药设备售前文档生成器\n\n版本：1.0")

st.success("✅ 应用成功运行！如需完整功能版本，请按照部署指南部署到Streamlit Cloud！")
