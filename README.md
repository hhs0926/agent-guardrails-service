# Agent 安全护栏配置服务

> 让 AI Agent 安全可控，企业放心用 AI

🌐 **在线演示**: https://hhs0926.github.io/agent-guardrails-service/

---

## 📊 为什么需要 Agent 安全护栏？

| 数据 | 说明 |
|------|------|
| **80%** | 企业已在使用 AI Agent |
| **仅20%** | 有成熟的安全治理措施 |
| **57%** | 已在生产环境运行 Agent |

**安全隐患：**
- 🚨 代码执行失控 - Agent 可能自动执行危险代码
- 🚨 数据泄露风险 - 敏感数据被发送到外部
- 🚨 API 调用超限 - 产生巨额账单
- 🚨 合规审计缺失 - 操作无法追溯

---

## 🛡️ 我们提供的解决方案

### 1. 策略拦截
- 禁止危险代码执行
- 禁止直接访问数据库
- 禁止访问敏感文件路径
- 禁止发送数据到外部服务器

### 2. 资源限制
- Token 使用上限
- API 调用频率限制
- 单次执行时间限制

### 3. 审计追踪
- 完整操作日志记录
- 敏感操作自动标记
- 违规行为实时告警

---

## 📦 服务套餐

| 套餐 | 价格 | 包含内容 |
|------|------|----------|
| **入门版** | ¥999 | 3个核心防护规则 + 7天支持 |
| **标准版** | ¥2,999 | 10+防护规则 + 审计系统 + 30天支持 |
| **企业版** | ¥9,999+ | 无限制规则 + 私有化部署 + 全年支持 |

---

## 🚀 快速开始

### 安装依赖
```bash
pip install agent-os-kernel
```

### 使用示例
```python
from agent_os.policies import PolicyEvaluator

# 加载护栏策略
evaluator = PolicyEvaluator()
evaluator.load_policies("templates/customer-service.yaml")

# 检查 Agent 操作
decision = evaluator.evaluate({
    "tool_name": "send_email",
    "params": {"to": "user@example.com"}
})

if not decision.allowed:
    print(f"🚫 拦截: {decision.reason}")
```

---

## 📁 项目结构

```
project2-agent-guardrails/
├── templates/              # 护栏策略模板
│   ├── customer-service.yaml    # 客服 Agent
│   ├── data-analyst.yaml        # 数据分析 Agent
│   └── office-automation.yaml   # 自动化办公 Agent
├── demo/                   # 演示代码
├── test_all_templates.py   # 测试脚本
└── index.html             # 服务介绍页
```

---

## 📞 联系我们

- **Gmail**: hhs7788369@gmail.com
- **QQ邮箱**: 1320496528@qq.com
- **微信**: 18159886379

提供免费安全评估，帮你找出 Agent 部署的安全漏洞。

---

## 🏗️ 技术栈

- [Microsoft Agent Governance Toolkit](https://github.com/microsoft/agent-governance-toolkit)
- Python 3.8+
- YAML 策略配置

---

## 📄 License

MIT License
