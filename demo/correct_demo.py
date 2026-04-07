"""
Agent Governance Toolkit - 正确用法演示
基于官方教程：https://github.com/microsoft/agent-governance-toolkit

场景：客服 Agent 安全护栏
- 禁止执行代码
- 禁止访问敏感工具
- Token 限制
"""

from agent_os.policies import PolicyEvaluator
from rich.console import Console
from rich.table import Table

console = Console()

# ============================================
# 1. 创建策略文件（YAML）
# ============================================

POLICY_YAML = """
version: "1.0"
name: customer-service-guardrails
description: Customer Service Agent Security Guardrails

rules:
  # 禁止执行代码
  - name: block-code-execution
    condition:
      field: tool_name
      operator: eq
      value: execute_code
    action: block
    priority: 100
    message: "[BLOCK] Code execution is forbidden in production"

  # 禁止访问数据库
  - name: block-database-access
    condition:
      field: tool_name
      operator: eq
      value: database_query
    action: deny
    priority: 90
    message: "[DENY] Database direct access is forbidden"

  # Token 限制
  - name: token-limit
    condition:
      field: token_count
      operator: gt
      value: 4000
    action: block
    priority: 80
    message: "[BLOCK] Token count exceeds limit (max 4000)"

  # 审计所有文件操作
  - name: audit-file-ops
    condition:
      field: tool_name
      operator: in
      value: ["read_file", "write_file", "delete_file"]
    action: audit
    priority: 70
    message: "[AUDIT] File operation logged"

  # 限制 API 调用次数
  - name: rate-limit-api
    condition:
      field: api_call_count
      operator: gte
      value: 100
    action: deny
    priority: 60
    message: ⏳ API 调用次数超限

defaults:
  action: allow
  max_tokens: 4096
  max_tool_calls: 50
"""

# ============================================
# 2. 保存策略文件
# ============================================

import tempfile
import os

def save_policy_file():
    """保存策略到临时文件"""
    policy_dir = tempfile.mkdtemp()
    policy_file = os.path.join(policy_dir, "guardrails.yaml")
    
    with open(policy_file, "w", encoding="utf-8", newline="") as f:
        f.write(POLICY_YAML)
    
    return policy_dir

# ============================================
# 3. 测试护栏
# ============================================

def test_guardrails():
    """测试护栏效果"""
    
    console.print("\n[bold cyan]=== Agent Guardrails Test (Official API) ===[/bold cyan]\n")
    
    # 保存策略
    policy_dir = save_policy_file()
    
    # 创建评估器
    evaluator = PolicyEvaluator()
    evaluator.load_policies(policy_dir)
    
    # 测试用例
    test_cases = [
        {"tool_name": "execute_code", "token_count": 100},
        {"tool_name": "database_query", "token_count": 500},
        {"tool_name": "search", "token_count": 5000},
        {"tool_name": "read_file", "token_count": 200},
        {"tool_name": "search", "token_count": 1000, "api_call_count": 150},
        {"tool_name": "send_email", "token_count": 300},  # 正常请求
    ]
    
    # 创建结果表格
    table = Table(title="护栏测试结果")
    table.add_column("工具", style="cyan")
    table.add_column("Token", style="white")
    table.add_column("决策", style="yellow")
    table.add_column("原因", style="dim")
    
    for ctx in test_cases:
        decision = evaluator.evaluate(ctx)
        
        tool_str = ctx["tool_name"]
        token_str = str(ctx.get("token_count", "-"))
        
        if decision.allowed:
            decision_str = "[green]ALLOW[/green]" if decision.action != "audit" else "[yellow]AUDIT[/yellow]"
        else:
            decision_str = "[red]BLOCK[/red]"
        
        reason_str = decision.reason[:50] + "..." if len(decision.reason) > 50 else decision.reason
        
        table.add_row(tool_str, token_str, decision_str, reason_str)
    
    console.print(table)
    
    # Display audit log
    console.print("\n[bold yellow]Audit Log Entries:[/bold yellow]")
    console.print("[dim]All audit actions are logged to the audit trail system[/dim]")

# ============================================
# 4. 运行演示
# ============================================

if __name__ == "__main__":
    console.print("[bold magenta]Agent Governance Toolkit Demo[/bold magenta]")
    console.print("[dim]Microsoft Open Source - Policy Engine Example[/dim]\n")
    
    try:
        test_guardrails()
        console.print("\n[bold green]Demo Complete![/bold green]")
    except Exception as e:
        console.print(f"\n[bold red]Error: {e}[/bold red]")
        console.print("[dim]Make sure installed: pip install agent-os-kernel[full][/dim]")
    
    console.print("\n[dim]Docs: https://github.com/microsoft/agent-governance-toolkit[/dim]")
