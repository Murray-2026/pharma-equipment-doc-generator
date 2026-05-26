from datetime import datetime


class TemplateManager:
    def __init__(self, equipment_type, regulation):
        self.equipment_type = equipment_type
        self.regulation = regulation
        self.current_date = datetime.now().strftime("%Y年%m月%d日")
    
    def get_urs_response_template(self, requirements=None):
        template = f"""# {self.equipment_type} - URS逐条回复

**文档编号**: URS-RESP-{datetime.now().strftime("%Y%m%d")}
**生成日期**: {self.current_date}
**适用法规**: {self.regulation}

---

## 1. 概述

### 1.1 项目背景
感谢贵公司对我们{self.equipment_type}的关注。我们非常重视此次合作机会，并将根据贵公司的URS要求，提供专业、合规的技术方案。

### 1.2 回复说明
本文件针对贵公司提供的用户需求说明（URS）进行逐条回复，确保我们的方案完全满足您的需求，并符合{self.regulation}的要求。

---

## 2. URS逐条回复

### 2.1 通用要求

| 序号 | URS要求 | 我方回复 | 符合性 | 备注 |
|------|---------|----------|--------|------|
| 1 | 设备应符合现行GMP要求 | 我方设备完全符合{self.regulation}要求，提供完整的验证文件 | ✅ 完全符合 | - |
| 2 | 设备应具备必要的安全防护装置 | 设备配备完整的安全联锁系统，确保操作人员安全 | ✅ 完全符合 | - |
| 3 | 设备材料应符合医药级要求 | 与产品接触部分采用316L不锈钢，表面粗糙度Ra≤0.8μm | ✅ 完全符合 | - |

### 2.2 技术规格要求

| 序号 | URS要求 | 我方回复 | 符合性 | 备注 |
|------|---------|----------|--------|------|
| 1 | 工作舱尺寸应满足生产需求 | 提供标准尺寸，并可根据客户需求定制 | ✅ 完全符合 | 详见配置清单 |
| 2 | 隔离器应具备良好的密封性 | 采用双门联锁设计，泄漏率符合ISO 14644-7标准 | ✅ 完全符合 | - |
| 3 | 温度控制精度应满足要求 | 温度控制精度±0.5℃，均匀性±1.0℃ | ✅ 完全符合 | - |

### 2.3 控制系统要求

| 序号 | URS要求 | 我方回复 | 符合性 | 备注 |
|------|---------|----------|--------|------|
| 1 | PLC控制系统，带触摸屏操作 | 采用西门子/欧姆龙PLC，10英寸彩色触摸屏 | ✅ 完全符合 | - |
| 2 | 数据记录和审计追踪功能 | 具备完善的审计追踪功能，数据存储时间≥5年 | ✅ 完全符合 | 符合21 CFR Part 11 |
| 3 | 报警功能 | 完备的声光报警系统，记录所有报警事件 | ✅ 完全符合 | - |

### 2.4 验证要求

| 序号 | URS要求 | 我方回复 | 符合性 | 备注 |
|------|---------|----------|--------|------|
| 1 | 提供完整的验证文件 | 提供IQ/OQ/PQ验证方案及报告模板 | ✅ 完全符合 | - |
| 2 | 支持现场验证服务 | 可提供专业的验证工程师进行现场验证支持 | ✅ 完全符合 | 可选服务 |

---

## 3. 补充说明

### 3.1 可选配置
我方还可提供多种可选配置，以进一步满足贵公司的特殊需求，详见报价文档中的配置清单。

### 3.2 售后服务
我们提供完善的售后服务体系，包括安装调试、培训、维护保养等，确保设备长期稳定运行。

---

**回复单位**: [贵公司名称]
**技术负责人**: [负责人姓名]
**联系电话**: [联系电话]
**日期**: {self.current_date}
"""
        return template
    
    def get_technical_spec_template(self):
        template = f"""# {self.equipment_type} - 技术方案

**文档编号**: TECH-SPEC-{datetime.now().strftime("%Y%m%d")}
**生成日期**: {self.current_date}
**适用法规**: {self.regulation}

---

## 1. 设备简介

### 1.1 产品概述
{self._get_equipment_description()}

### 1.2 应用领域
- 药品生产
- 生物制品制备
- 无菌检测
- 细胞治疗

---

## 2. 技术参数

### 2.1 主要技术参数
| 参数名称 | 规格指标 |
|----------|----------|
| 外部尺寸 | 按需定制 |
| 工作舱尺寸 | 按需定制 |
| 材质 | 316L不锈钢 |
| 表面粗糙度 | Ra≤0.8μm |
| 电源要求 | 380V/50Hz/三相 |
| 功率 | 按需定制 |

### 2.2 性能参数
| 性能指标 | 标准值 |
|----------|--------|
| 洁净度等级 | ISO 5级 (A级) |
| 温度控制范围 | 18-25℃ |
| 温度控制精度 | ±0.5℃ |
| 相对湿度 | 40-60%RH |
| 压差控制 | 10-20Pa |

---

## 3. 系统组成

### 3.1 主体结构
- 316L不锈钢箱体
- 透明视窗（丙烯酸或钢化玻璃）
- 手套接口系统
- 传递舱/传递门

### 3.2 空调净化系统
- 高效过滤器（HEPA H14）
- 风机单元
- 温湿度控制系统
- 压差监测系统

### 3.3 控制系统
- PLC控制器
- 彩色触摸屏操作界面
- 数据记录与审计追踪
- 报警系统

{self._get_specific_components()}

---

## 4. 合规性说明

### 4.1 法规符合
本设备完全符合以下法规要求：
- {self.regulation}
- ISO 14644（洁净室及相关受控环境）
- ISO 13485（医疗器械质量管理体系）
- GAMP 5（良好自动化生产规范）

### 4.2 验证文件
提供完整的验证文件包：
- 设计确认（DQ）
- 安装确认（IQ）
- 运行确认（OQ）
- 性能确认（PQ）
- 维护保养SOP

---

## 5. 技术支持与服务

### 5.1 安装调试
- 专业工程师现场安装
- 设备调试与试运行
- 性能验证

### 5.2 培训服务
- 操作人员培训
- 维护保养培训
- 验证知识培训

### 5.3 售后服务
- 质保期：设备验收合格后12个月
- 终身技术支持
- 备件供应
- 定期维护保养服务

---

**编制**: [技术部]
**审核**: [质量部]
**批准**: [技术负责人]
**日期**: {self.current_date}
"""
        return template
    
    def get_quotation_template(self, config_type="standard"):
        price_info = self._get_price_info(config_type)
        
        template = f"""# {self.equipment_type} - 报价单

**报价编号**: QUO-{datetime.now().strftime("%Y%m%d")}
**报价日期**: {self.current_date}
**有效期**: 30天
**适用法规**: {self.regulation}
**配置类型**: {config_type}配置

---

## 1. 报价汇总

| 项目 | 金额（人民币） |
|------|----------------|
| 设备主机 | ¥{price_info['equipment_price']:,} |
| 标准配件 | ¥{price_info['accessories_price']:,} |
| 运输保险 | ¥{price_info['shipping_price']:,} |
| 安装调试 | ¥{price_info['installation_price']:,} |
| 培训服务 | ¥{price_info['training_price']:,} |
| **小计** | **¥{price_info['subtotal']:,}** |
| 增值税 (13%) | ¥{price_info['tax']:,} |
| **总计** | **¥{price_info['total']:,}** |

---

## 2. 详细配置清单

### 2.1 设备主机
| 序号 | 配置名称 | 规格/型号 | 数量 | 备注 |
|------|----------|-----------|------|------|
| 1 | {self.equipment_type}主机 | 标准/定制 | 1台 | 详见技术方案 |
{self._get_config_items(config_type)}

### 2.2 标准配件
| 序号 | 配件名称 | 规格 | 数量 |
|------|----------|------|------|
| 1 | 备用手套 | 标准 | 2副 |
| 2 | 过滤器备件 | H14 | 1套 |
| 3 | 专用工具 | - | 1套 |
{self._get_accessory_items(config_type)}

### 2.3 可选配置（另行报价）
| 序号 | 可选配置名称 | 参考价格 |
|------|--------------|----------|
| 1 | 在线VHP灭菌系统 | ¥80,000-150,000 |
| 2 | 粒子计数器 | ¥50,000-100,000 |
| 3 | 额外验证服务 | ¥30,000-50,000 |
| 4 | 延长质保期 | ¥20,000-40,000/年 |

---

## 3. 预算区间

根据贵公司需求，我们提供以下预算参考：

| 配置等级 | 预算区间（人民币） | 说明 |
|----------|-------------------|------|
| 基础配置 | ¥{price_info['budget_low']:,} - ¥{int(price_info['budget_low'] * 1.1):,} | 满足基本生产需求 |
| 标准配置 | ¥{price_info['budget_mid']:,} - ¥{int(price_info['budget_mid'] * 1.1):,} | 推荐配置，性价比最优 |
| 高级配置 | ¥{price_info['budget_high']:,} - ¥{int(price_info['budget_high'] * 1.1):,} | 功能齐全，满足高端需求 |

---

## 4. 商务条款

### 4.1 付款方式
- 预付款：30%
- 发货款：60%
- 质保金：10%（验收合格后6个月支付）

### 4.2 交货期
- 标准配置：收到预付款后45-60天
- 定制配置：双方协商确定

### 4.3 质保期
- 设备验收合格后12个月
- 消耗品除外

### 4.4 售后服务
- 7×24小时电话技术支持
- 48小时内现场响应（国内）
- 定期回访服务

---

## 5. 附录

### 5.1 法规符合性声明
我方保证所提供设备符合{self.regulation}及相关法规要求。

### 5.2 报价说明
- 以上报价为参考价格，最终价格以正式合同为准
- 如有特殊需求，请另行协商
- 本报价有效期30天

---

**报价单位**: [贵公司名称]
**联系人**: [联系人姓名]
**联系电话**: [联系电话]
**电子邮箱**: [邮箱地址]
**日期**: {self.current_date}
"""
        return template
    
    def _get_equipment_description(self):
        descriptions = {
            "单体无菌隔离器": "本单体无菌隔离器是专为药品生产、生物制品制备等无菌操作环境设计的高端设备，采用先进的隔离技术，为操作人员和产品提供双向保护，确保生产过程的无菌性和安全性。",
            "VHP传递窗": "本VHP（汽化过氧化氢）传递窗是用于洁净区与非洁净区之间物品传递的专用设备，内置VHP灭菌系统，可对传递物品进行高效的生物去污处理，确保交叉污染的有效控制。",
            "整线隔离器": "本整线隔离器系统集成了无菌隔离器、传递窗、灌装机、轧盖机等设备，形成完整的无菌生产线，广泛应用于生物制品、注射剂等产品的无菌生产过程。",
            "单体负压隔离器": "本单体负压隔离器主要用于高活性药物、细胞毒性药物等特殊产品的处理，通过负压控制技术，有效防止有害物质泄漏，保护操作人员和环境安全。"
        }
        return descriptions.get(self.equipment_type, "本设备是专为制药行业设计的专业设备，符合GMP要求。")
    
    def _get_specific_components(self):
        components = {
            "单体无菌隔离器": "\n### 3.4 特殊系统\n- 双门联锁传递系统\n- 在线清洗系统（CIP）\n- 在线灭菌系统（SIP，可选）",
            "VHP传递窗": "\n### 3.4 VHP灭菌系统\n- 过氧化氢发生器\n- 汽化系统\n- 浓度监测系统\n- 催化分解系统",
            "整线隔离器": "\n### 3.4 生产线集成\n- 灌装机集成接口\n- 轧盖机集成接口\n- 在线检测系统接口\n- 自动化控制系统",
            "单体负压隔离器": "\n### 3.4 安全防护系统\n- 高效负压控制\n- 袋进袋出（BIBO）过滤系统\n- 气体监测报警系统\n- 应急防护装置"
        }
        return components.get(self.equipment_type, "")
    
    def _get_price_info(self, config_type):
        base_prices = {
            "单体无菌隔离器": {"low": 300000, "mid": 500000, "high": 800000},
            "VHP传递窗": {"low": 150000, "mid": 250000, "high": 400000},
            "整线隔离器": {"low": 1500000, "mid": 2500000, "high": 4000000},
            "单体负压隔离器": {"low": 400000, "mid": 600000, "high": 1000000}
        }
        
        base = base_prices.get(self.equipment_type, {"low": 300000, "mid": 500000, "high": 800000})
        
        if config_type == "basic":
            equipment = base["low"]
        elif config_type == "premium":
            equipment = base["high"]
        else:
            equipment = base["mid"]
        
        accessories = int(equipment * 0.15)
        shipping = int(equipment * 0.03)
        installation = int(equipment * 0.08)
        training = int(equipment * 0.02)
        subtotal = equipment + accessories + shipping + installation + training
        tax = int(subtotal * 0.13)
        total = subtotal + tax
        
        return {
            "equipment_price": equipment,
            "accessories_price": accessories,
            "shipping_price": shipping,
            "installation_price": installation,
            "training_price": training,
            "subtotal": subtotal,
            "tax": tax,
            "total": total,
            "budget_low": base["low"],
            "budget_mid": base["mid"],
            "budget_high": base["high"]
        }
    
    def _get_config_items(self, config_type):
        items = {
            "basic": "\n| 2 | 控制系统 | 基础PLC + 触摸屏 | 1套 |\n| 3 | 空调净化系统 | 标准配置 | 1套 |",
            "standard": "\n| 2 | 控制系统 | 高端PLC + 10寸触摸屏 | 1套 |\n| 3 | 空调净化系统 | 高效节能配置 | 1套 |\n| 4 | 温湿度控制系统 | 精密控制 | 1套 |",
            "premium": "\n| 2 | 控制系统 | 高端PLC + 15寸触摸屏 + SCADA | 1套 |\n| 3 | 空调净化系统 | 顶级配置 | 1套 |\n| 4 | 温湿度控制系统 | 超精密控制 | 1套 |\n| 5 | 在线VHP灭菌系统 | 集成式 | 1套 |\n| 6 | 粒子监测系统 | 在线监测 | 1套 |"
        }
        return items.get(config_type, items["standard"])
    
    def _get_accessory_items(self, config_type):
        if config_type == "premium":
            return "\n| 4 | 额外过滤器备件 | H14 | 2套 |\n| 5 | 备用手套 | 标准 | 4副 |"
        return ""
