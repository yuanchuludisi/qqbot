import subprocess
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
from threading import Thread
import matplotlib
from matplotlib.font_manager import FontProperties
matplotlib.use('Agg')  # 使用非交互式后端，适合服务器环境

latency_time=0
latency_sum=0

class LatencyMonitor:
    def __init__(self, data_file="latency_data.txt",save_dir=None):
        self.save_dir =save_dir if save_dir else os.getcwd()
        os.makedirs(self.save_dir, exist_ok=True)
        
        # 如果data_file是相对路径，将其放在save_dir下
        if not os.path.isabs(data_file):
            self.data_file = os.path.join(self.save_dir, data_file)
        else:
            self.data_file = data_file
        self.running = False
        self.monitoring_thread = None
        
        # 如果数据文件不存在，创建一个空文件
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w') as f:
                f.write("timestamp,latency\n")
    
    def get_latency(self):
        """调用mc.py获取当前延迟"""
        try:
            result = subprocess.run(['python', 'mc.py'], 
                                   capture_output=True, 
                                   text=True, 
                                   check=True)
            latency = result.stdout.strip()
            return float(latency)
        except (subprocess.SubprocessError, ValueError) as e:
            print(f"获取延迟时出错: {e}")
            return None
    
    def record_latency(self):
        """记录延迟数据到文件"""
        latency = self.get_latency()
        if latency is not None:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.data_file, 'a') as f:
                f.write(f"{timestamp},{latency}\n")
            global latency_time
            global latency_sum
            latency_time += 1
            latency_sum += latency
            if latency_time >= 10:
                latency_sum /= latency_time
                latency_sum = round(latency_sum,2)
                print(f"[{timestamp}] 十分钟平均延迟: {latency_sum}ms")
                latency_sum=0
                latency_time=0

    
    def start_monitoring(self):
        """开始监控延迟"""
        if self.running:
            print("监控已经在运行中")
            return
        
        self.running = True
        self.monitoring_thread = Thread(target=self._monitoring_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
        print("延迟监控已启动")
    
    def _monitoring_loop(self):
        """监控循环，每分钟记录一次延迟"""
        while self.running:
            self.record_latency()
            # 等待一分钟
            time.sleep(60)
    
    def stop_monitoring(self):
        """停止监控延迟"""
        self.running = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=1)
        print("延迟监控已停止")
    
    def generate_latency_graph(self, output_file="latency_graph.png", last_hours=None):
        """生成延迟折线图
        
        参数:
            output_file: 输出图片文件名
            last_hours: 如果设置，只显示最近几小时的数据
        """
        timestamps = []
        latencies = []
        
        # 读取数据
        with open(self.data_file, 'r') as f:
            # 跳过标题行
            next(f)
            for line in f:
                if line.strip():
                    parts = line.strip().split(',')
                    if len(parts) == 2:
                        timestamp_str, latency_str = parts
                        try:
                            timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                            latency = float(latency_str)
                            timestamps.append(timestamp)
                            latencies.append(latency)
                        except (ValueError, TypeError) as e:
                            print(f"解析数据行时出错: {line}, 错误: {e}")
        
        if not timestamps:
            print("没有可用的延迟数据")
            return None
        
        # 如果指定了last_hours，只保留最近几小时的数据
        if last_hours is not None and timestamps:
            cutoff_time = datetime.datetime.now() - datetime.timedelta(hours=last_hours)
            valid_data = [(t, l) for t, l in zip(timestamps, latencies) if t >= cutoff_time]
            if valid_data:
                timestamps, latencies = zip(*valid_data)
            else:
                timestamps, latencies = [], []
        
        #配置中文字体
        self._setup_chinese_font()

        # 创建图表
        plt.figure(figsize=(12, 6))
        plt.plot(timestamps, latencies, marker='o', linestyle='-', markersize=3)
        plt.title('详细延迟波动时间表')
        plt.xlabel('时间')
        plt.ylabel('延迟 (ms)')
        plt.grid(True)
        
        # 设置x轴日期格式
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
        plt.gcf().autofmt_xdate()  # 自动格式化日期标签
        
         # 处理输出文件路径
        if not os.path.isabs(output_file):
            # 如果是相对路径，则保存到指定的保存目录
            full_output_path = os.path.join(self.save_dir, output_file)
        else:
            # 如果已经是绝对路径，则直接使用
            full_output_path = output_file
        
        # 确保输出文件的目录存在
        os.makedirs(os.path.dirname(full_output_path), exist_ok=True)
        
        # 保存图表
        plt.tight_layout()
        plt.savefig(full_output_path, dpi=100)
        plt.close()
        
        return full_output_path
    
    def _setup_chinese_font(self):
    # 指定一个绝对路径的中文字体文件
        font_path = "C:/Windows/Fonts/simkai.ttf"  # 例如: "C:/Windows/Fonts/simhei.ttf"
        if os.path.exists(font_path):
            font_prop = FontProperties(fname=font_path)
            plt.rcParams['font.family'] = font_prop.get_name()
        else:
            print(f"找不到指定的字体文件: {font_path}")

# 如果直接运行此脚本，则开始监控
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='服务器延迟监控工具')
    parser.add_argument('--save-dir', type=str, default=None, 
                        help='保存数据和图表的目录路径，例如 "D:\\file"')
    parser.add_argument('--data-file', type=str, default="latency_data.txt",
                        help='延迟数据文件名')
    parser.add_argument('--generate-graph', action='store_true',
                        help='只生成图表而不进行监控')
    parser.add_argument('--hours', type=int, default=None,
                        help='生成图表时只显示最近N小时的数据')
    
    args = parser.parse_args()
    
    monitor = LatencyMonitor(data_file=args.data_file, save_dir=args.save_dir)
    
    if args.generate_graph:
        # 只生成图表
        output_file = "latency_graph.png"
        monitor.generate_latency_graph(output_file=output_file, last_hours=args.hours)
    else:
        # 开始监控
        try:
            monitor.start_monitoring()
            print("按 Ctrl+C 停止监控")
            # 保持主线程运行
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            monitor.stop_monitoring()
            print("监控已停止")