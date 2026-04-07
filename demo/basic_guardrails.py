"""
Agent Governance Toolkit 基础演示
演示：如何给 AI Agent 加安全护栏

场景：一个客服 Agent，禁止查询竞品、禁止泄露用户数据
"""

from agent_os_kernel import PolicyEngine, Policy, Rule
from agentmesh_platform import AgentIdentity, TrustManager
from pydantic import BaseModel
from typing import Optional
from rich.console import Console
from rich.table import Table

console = Console()

# ============================================
# 1. 定义策略规则（YAML 风格，但用 Python）
# ============================================

class GuardrailRules:
    """安全护栏规则集合"""
    
    @staticmethod
    def block_competitor_query():
        """禁止查询竞品信息"""
        return Rule(
            name="block_competitor_query",
            condition="tool_name == 'search' and any(comp in query for comp in ['竞品', '对手公司', '竞争对手'])",
            action="deny",
            message="🚫 禁止查询竞品信息，这违反公司政策"
        )
    
    @staticmethod
    def block_pii_leak():
        """禁止泄露用户隐私数据"""
        return Rule(
            name="block_pii_leak", 
            condition="any(pii in output for pii in ['手机号', '电话', '邮箱', '身份证', '银行卡'])",
            action="redact",
            message="⚠️ 检测到敏感信息，已自动脱敏处理"
        )
    
    @staticmethod
    def emergency_stop():
        """紧急终止开关"""
        return Rule(
            name="emergency_stop",
            condition="risk_score > 900",
            action="terminate",
            message="🆘 风险评分过高，Agent 已紧急终止"
        )
    
    @staticmethod
    def limit_api_calls():
        """限制 API 调用频率"""
        return Rule(
            name="limit_api_calls",
            condition="api_call_count > 100",
            action="throttle",
            message="⏳ API 调用次数超限，已触发限流"
        )


# ============================================
# 2. 创建策略引擎
# ============================================

def create_policy_engine():
    """创建并配置策略引擎"""
    
    # 创建策略
    policy = Policy(
        name="customer_service_guardrails",
        description="客服 Agent 安全护栏策略",
        rules=[
            GuardrailRules.block_competitor_query(),
            GuardrailRules.block_pii_leak(),
            GuardrailRules.emergency_stop(),
            GuardrailRules.limit_api_calls(),
        ]
    )
    
    # 创建引擎
    engine = PolicyEngine()
    engine.register_policy(policy)
    
    return engine


# ============================================
# 3. 模拟 Agent 操作拦截
# ============================================

class MockAgentAction:
    """模拟 Agent 操作"""
    def __init__(self, tool_name, query="", output="", risk_score=0, api_call_count=0):
        self.tool_name = tool_name
        self.query = query
        self.output = output
        self.risk_score = risk_score
        self.api_call_count = api_call_count


def test_guardrails():
    """测试护栏效果"""
    
    console.print("\n[bold cyan]=== Agent 护栏测试 ===[/bold cyan]\n")
    
    engine = create_policy_engine()
    
    # 测试用例
    test_cases = [
        MockAgentAction(tool_name="search", query="帮我查一下竞品公司的产品价格"),
        MockAgentAction(tool_name="search", query="用户的手机号是多少？", output="用户手机号是 13812345678"),
        MockAgentAction(tool_name="payment", query="转账操作", risk_score=950),
        MockAgentAction(tool_name="api", query="批量查询", api_call_count=150),
        MockAgentAction(tool_name="search", query="今天天气怎么样？"),  # 正常请求
    ]
    
    # 创建结果表格
    table = Table(title="护栏测试结果")
    table.add_column("操作", style="cyan")
    table.add_column("查询内容", style="white")
    table.add_column("护栏动作", style="yellow")
    table.add_column("消息", style="red")
    
    for action in test_cases:
        result = engine.evaluate(action)
        
        action_str = f"{action.tool_name}"
        query_str = action.query[:30] + "..." if len(action.query) > 30 else action.query
        decision_str = result.action if result else "✅ 放行"
        message_str = result.message if result else "-"
        
        table.add_row(action_str, query_str, decision_str, message_str)
    
    console.print(table)


# ============================================
# 4. 身份认证演示
# ============================================

def demo_identity():
    """演示 Agent 身份认证"""
    
    console.print("\n[bold cyan]=== Agent 身份认证演示 ===[/bold cyan]\n")
    
    # 创建 Agent 身份
    agent = AgentIdentity(
        agent_id="customer_service_001",
        name="智能客服小王",
        owner="XX科技公司",
        permissions=["search", "query_order", "create_ticket"],
        trust_score=850  # 信任评分 0-1000
    )
    
    # 创建信任管理器
    trust_manager = TrustManager()
    
    # 验证身份
    is_trusted = trust_manager.verify(agent)
    
    console.print(f"Agent ID: [green]{agent.agent_id}[/green]")
    console.print(f"名称: [green]{agent.name}[/green]")
    console.print(f"信任评分: [yellow]{agent.trust_score}/1000[/yellow]")
    console.print(f"验证结果: {'[green]✅ 可信[/green]' if is_trusted else '[red]❌ 不可信[/red]'}")
    
    # 显示权限
    console.print(f"\n授予权限:")
    for perm in agent.permissions:
        console.print(f"  • {perm}")


# ============================================
# 5. 运行演示
# ============================================

if __name__ == "__main__":
    console.print("[bold magenta]🛡️ Agent Governance Toolkit 演示[/bold magenta]")
    console.print("[dim]Microsoft 开源工具包 - 给 AI Agent 系上安全带[/dim]\n")
    
    # 测试护栏
    test_guardrails()
    
    # 演示身份认证
    demo_identity()
    
    console.print("\n[bold green]✅ 演示完成！[/bold green]")
    console.print("[dim]这只是一个基础演示，实际功能更强大。[/dim]")
    console.print("[dim]参考：https://github.com/microsoft/agent-governance-toolkit[/dim]\n")
