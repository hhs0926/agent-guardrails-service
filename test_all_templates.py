"""
Agent 护栏模板测试脚本（官方API版本）
测试 3 个典型场景：客服 / 数据分析 / 自动化办公
"""

from agent_os.policies import PolicyEvaluator
from pathlib import Path


def test_customer_service():
    """测试客服 Agent 护栏"""
    print("\n" + "=" * 60)
    print("【客服 Agent 护栏测试】")
    print("=" * 60)

    evaluator = PolicyEvaluator()
    evaluator.load_policies(Path(__file__).parent / "templates")

    test_cases = [
        {"tool_name": "send_email", "desc": "发送外部邮件"},
        {"tool_name": "export_excel", "desc": "导出客户数据"},
        {"tool_name": "database_query", "desc": "查询客户数据"},
        {"tool_name": "update_customer", "desc": "修改客户信息"},
        {"tool_name": "search", "token_count": 500, "desc": "普通搜索"},
        {"tool_name": "search", "token_count": 5000, "desc": "大量Token搜索"},
    ]

    for case in test_cases:
        decision = evaluator.evaluate(case)
        status = "ALLOW" if decision.allowed else "BLOCK"
        if decision.action == "audit":
            status = "AUDIT"

        print(f"\n{case['desc']}")
        print(f"  工具: {case.get('tool_name')}")
        print(f"  结果: {status}")
        if decision.reason:
            print(f"  原因: {decision.reason}")


def test_data_analyst():
    """测试数据分析 Agent 护栏"""
    print("\n" + "=" * 60)
    print("【数据分析 Agent 护栏测试】")
    print("=" * 60)

    evaluator = PolicyEvaluator()
    evaluator.load_policies(Path(__file__).parent / "templates")

    test_cases = [
        {"tool_name": "database_update", "desc": "修改数据源"},
        {"tool_name": "database_query", "params": {"table": "users"}, "desc": "访问敏感表（用户）"},
        {"tool_name": "database_query", "params": {"table": "orders"}, "desc": "访问普通表（订单）"},
        {"tool_name": "send_email", "desc": "发送数据到外部"},
        {"tool_name": "database_query", "params": {"result_count": 1500}, "desc": "大批量查询"},
    ]

    for case in test_cases:
        decision = evaluator.evaluate(case)
        status = "ALLOW" if decision.allowed else "BLOCK"
        if decision.action == "audit":
            status = "AUDIT"

        print(f"\n{case['desc']}")
        print(f"  工具: {case.get('tool_name')}")
        print(f"  结果: {status}")
        if decision.reason:
            print(f"  原因: {decision.reason}")


def test_office_automation():
    """测试自动化办公 Agent 护栏"""
    print("\n" + "=" * 60)
    print("【自动化办公 Agent 护栏测试】")
    print("=" * 60)

    evaluator = PolicyEvaluator()
    evaluator.load_policies(Path(__file__).parent / "templates")

    test_cases = [
        {"tool_name": "delete_file", "params": {"path": "/data/report.xlsx"}, "desc": "删除文件"},
        {"tool_name": "read_file", "params": {"path": "/salary/2026.xlsx"}, "desc": "访问薪资目录"},
        {"tool_name": "read_file", "params": {"path": "/data/report.xlsx"}, "desc": "读取普通文件"},
        {"tool_name": "execute_bash", "desc": "执行Bash脚本"},
        {"tool_name": "http_request", "desc": "外部网络请求"},
        {"tool_name": "write_file", "params": {"path": "/data/output.xlsx"}, "desc": "写入文件"},
    ]

    for case in test_cases:
        decision = evaluator.evaluate(case)
        status = "ALLOW" if decision.allowed else "BLOCK"
        if decision.action == "audit":
            status = "AUDIT"

        print(f"\n{case['desc']}")
        print(f"  工具: {case.get('tool_name')}")
        print(f"  结果: {status}")
        if decision.reason:
            print(f"  原因: {decision.reason}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Agent 护栏模板完整测试")
    print("=" * 60)

    try:
        test_customer_service()
        test_data_analyst()
        test_office_automation()

        print("\n" + "=" * 60)
        print("所有测试完成！")
        print("=" * 60)

    except Exception as e:
        print(f"\n测试失败: {e}")
        import traceback
        traceback.print_exc()
