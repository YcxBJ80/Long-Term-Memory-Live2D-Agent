#!/usr/bin/env python3
"""
memU 查询性能测试脚本

用于测试优化后的 memU 查询性能
"""

import time
import sys
from pathlib import Path

# 添加 memU 到路径
sys.path.insert(0, str(Path(__file__).parent / "memU"))

try:
    from memu.sdk.python.client import MemuClient
    print("✅ 成功导入 MemuClient")
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print("请确保 memU 已正确安装")
    sys.exit(1)


def test_query_performance():
    """测试查询性能"""
    print("\n" + "="*60)
    print("memU 查询性能测试")
    print("="*60)
    
    # 初始化客户端
    base_url = "http://localhost:8000"
    print(f"\n📡 连接到服务器: {base_url}")
    
    try:
        client = MemuClient(base_url=base_url)
        print("✅ 客户端初始化成功")
    except Exception as e:
        print(f"❌ 客户端初始化失败: {e}")
        print("请确保 memU 服务器正在运行:")
        print("  cd memU && python -m memu.server.cli start")
        return
    
    # 测试参数
    test_queries = [
        "你好",
        "今天天气怎么样",
        "帮我记住这个信息",
        "我们之前聊过什么",
        "最近有什么新消息"
    ]
    
    user_id = "test_user"
    agent_id = "test_agent"
    top_k = 10
    
    print(f"\n🔍 测试参数:")
    print(f"  - User ID: {user_id}")
    print(f"  - Agent ID: {agent_id}")
    print(f"  - Top K: {top_k}")
    print(f"  - 查询数量: {len(test_queries)}")
    
    # 执行测试
    print("\n" + "-"*60)
    print("开始测试...")
    print("-"*60)
    
    results = []
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n[{i}/{len(test_queries)}] 查询: \"{query}\"")
        
        try:
            start_time = time.time()
            
            result = client.retrieve_related_memory_items(
                user_id=user_id,
                agent_id=agent_id,
                query=query,
                top_k=top_k
            )
            
            elapsed = time.time() - start_time
            
            # 提取性能信息
            num_results = len(result.related_memories) if hasattr(result, 'related_memories') else 0
            
            results.append({
                'query': query,
                'elapsed': elapsed,
                'num_results': num_results,
                'success': True
            })
            
            print(f"  ✅ 耗时: {elapsed:.3f} 秒")
            print(f"  📊 找到: {num_results} 条记忆")
            
            # 如果是第一次查询，显示优化信息
            if i == 1:
                print(f"  🚀 优化状态:")
                if hasattr(result, '__dict__'):
                    result_dict = result.__dict__
                    if 'numpy_acceleration' in result_dict:
                        print(f"     - NumPy 加速: {result_dict.get('numpy_acceleration', 'N/A')}")
                    if 'cached_categories' in result_dict:
                        print(f"     - 缓存类别数: {result_dict.get('cached_categories', 'N/A')}")
            
        except Exception as e:
            elapsed = time.time() - start_time
            results.append({
                'query': query,
                'elapsed': elapsed,
                'num_results': 0,
                'success': False,
                'error': str(e)
            })
            print(f"  ❌ 查询失败: {e}")
    
    # 统计结果
    print("\n" + "="*60)
    print("测试结果统计")
    print("="*60)
    
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    if successful:
        times = [r['elapsed'] for r in successful]
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        total_results = sum(r['num_results'] for r in successful)
        
        print(f"\n✅ 成功查询: {len(successful)}/{len(results)}")
        print(f"\n⏱️  性能指标:")
        print(f"  - 平均耗时: {avg_time:.3f} 秒")
        print(f"  - 最快查询: {min_time:.3f} 秒")
        print(f"  - 最慢查询: {max_time:.3f} 秒")
        print(f"  - 总记忆数: {total_results}")
        
        # 性能评估
        print(f"\n📈 性能评估:")
        if avg_time < 0.5:
            print("  🌟 优秀！查询速度非常快")
        elif avg_time < 1.0:
            print("  ✅ 良好！查询速度符合预期")
        elif avg_time < 2.0:
            print("  ⚠️  一般，可能需要进一步优化")
        else:
            print("  ❌ 较慢，建议检查配置和数据量")
        
        # 首次查询 vs 后续查询对比
        if len(times) > 1:
            first_query_time = times[0]
            subsequent_avg = sum(times[1:]) / len(times[1:])
            speedup = first_query_time / subsequent_avg if subsequent_avg > 0 else 1
            
            print(f"\n🔄 缓存效果:")
            print(f"  - 首次查询: {first_query_time:.3f} 秒")
            print(f"  - 后续平均: {subsequent_avg:.3f} 秒")
            print(f"  - 加速倍数: {speedup:.2f}x")
            
            if speedup > 2:
                print("  ✅ 缓存效果显著！")
            elif speedup > 1.5:
                print("  ✅ 缓存有效")
            else:
                print("  ⚠️  缓存效果不明显")
    
    if failed:
        print(f"\n❌ 失败查询: {len(failed)}")
        for r in failed:
            print(f"  - \"{r['query']}\": {r.get('error', 'Unknown error')}")
    
    print("\n" + "="*60)
    print("测试完成！")
    print("="*60)


if __name__ == "__main__":
    try:
        test_query_performance()
    except KeyboardInterrupt:
        print("\n\n⚠️  测试被用户中断")
    except Exception as e:
        print(f"\n\n❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

