from mcstatus import JavaServer
from mcstatus.status_response import JavaStatusResponse

with open("mc.txt","r") as mc_url:
    mc_txt=mc_url.read()
mc_list=mc_txt.split(":")

def get_server_info(host: str = "localhost", port: int = int(mc_list[1])) -> dict:
    """
    获取Minecraft服务器完整状态信息
    返回包含以下字段的字典：
    - online: 是否在线
    - error: 错误信息（当online=False时存在）
    - players: 玩家信息字典
    - version: 版本信息
    - latency: 服务器延迟
    - motd: 服务器描述
    """
    result = {
        "online": False,
        "latency": 0,
    }

    try:
        # 创建服务器对象
        server = JavaServer(host, port)
        
        # 获取基础状态信息
        status: JavaStatusResponse = server.status()
        result.update({
            "online": True,
            "latency": round(status.latency, 2),
        })

        return result

    except Exception as main_error:
        result["error"] = f"连接失败: {str(main_error)}"
        return result

# 使用示例
if __name__ == "__main__":
    server_info = get_server_info(str(mc_list[0]))  # 替换为你的服务器地址
    
    if server_info["online"]:
        print(f"{server_info['latency']}")
    else:
        print(f"服务器离线: {server_info.get('error', '未知错误')}")