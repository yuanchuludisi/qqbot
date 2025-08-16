from latency_monitor import LatencyMonitor

# 创建监控器实例
monitor = LatencyMonitor(save_dir=r"D:\QQbot\QQbot3\yuanchu\yuanchu\plugins\foo")

# 如果需要，可以启动监控
# monitor.start_monitoring()

# 生成延迟图表
graph_file = monitor.generate_latency_graph("latency_graph.png",last_hours=8)  # 生成最近24小时的延迟图
print(f"图表已生成: {graph_file}")