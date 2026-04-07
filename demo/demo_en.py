# -*- coding: utf-8 -*-
"""
Agent Governance Toolkit Demo
Based on official tutorial: https://github.com/microsoft/agent-governance-toolkit

Scenario: Customer Service Agent Guardrails
- Block code execution
- Block sensitive tools
- Token limit enforcement
"""

import sys
import io
import tempfile
import os

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from agent_os.policies import PolicyEvaluator
from rich.console import Console
from rich.table import Table

console = Console()

# Policy YAML
POLICY_YAML = """
version: "1.0"
name: customer-service-guardrails
description: Customer Service Agent Security Guardrails

rules:
  - name: block-code-execution
    condition:
      field: tool_name
      operator: eq
      value: execute_code
    action: block
    priority: 100
    message: "[BLOCK] Code execution is forbidden in production"

  - name: block-database-access
    condition:
      field: tool_name
      operator: eq
      value: database_query
    action: deny
    priority: 90
    message: "[DENY] Database direct access is forbidden"

  - name: token-limit
    condition:
      field: token_count
      operator: gt
      value: 4000
    action: block
    priority: 80
    message: "[BLOCK] Token count exceeds limit (max 4000)"

  - name: audit-file-ops
    condition:
      field: tool_name
      operator: in
      value: ["read_file", "write_file", "delete_file"]
    action: audit
    priority: 70
    message: "[AUDIT] File operation logged"

  - name: rate-limit-api
    condition:
      field: api_call_count
      operator: gte
      value: 100
    action: deny
    priority: 60
    message: "[DENY] API call count exceeds limit"

defaults:
  action: allow
  max_tokens: 4096
  max_tool_calls: 50
"""

def save_policy_file():
    """Save policy to temp file"""
    policy_dir = tempfile.mkdtemp()
    policy_file = os.path.join(policy_dir, "guardrails.yaml")
    
    with open(policy_file, "w", encoding="utf-8", newline="") as f:
        f.write(POLICY_YAML)
    
    return policy_dir

def test_guardrails():
    """Test guardrails effect"""
    
    console.print("\n[bold cyan]=== Agent Guardrails Test (Official API) ===[/bold cyan]\n")
    
    # Save policy
    policy_dir = save_policy_file()
    
    # Create evaluator
    evaluator = PolicyEvaluator()
    evaluator.load_policies(policy_dir)
    
    # Test cases
    test_cases = [
        {"tool_name": "execute_code", "token_count": 100},
        {"tool_name": "database_query", "token_count": 500},
        {"tool_name": "search", "token_count": 5000},
        {"tool_name": "read_file", "token_count": 200},
        {"tool_name": "search", "token_count": 1000, "api_call_count": 150},
        {"tool_name": "send_email", "token_count": 300},  # Normal request
    ]
    
    # Create result table
    table = Table(title="Guardrails Test Results")
    table.add_column("Tool", style="cyan")
    table.add_column("Token", style="white")
    table.add_column("Decision", style="yellow")
    table.add_column("Reason", style="dim")
    
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
    
    # Display audit log info
    console.print("\n[bold yellow]Audit Log Entries:[/bold yellow]")
    console.print("[dim]All audit actions are logged to the audit trail system[/dim]")

if __name__ == "__main__":
    console.print("[bold magenta]Agent Governance Toolkit Demo[/bold magenta]")
    console.print("[dim]Microsoft Open Source - Policy Engine Example[/dim]\n")
    
    try:
        test_guardrails()
        console.print("\n[bold green]Demo Complete![/bold green]")
    except Exception as e:
        console.print(f"\n[bold red]Error: {e}[/bold red]")
        import traceback
        traceback.print_exc()
        console.print("[dim]Make sure installed: pip install agent-os-kernel[full][/dim]")
    
    console.print("\n[dim]Docs: https://github.com/microsoft/agent-governance-toolkit[/dim]")
