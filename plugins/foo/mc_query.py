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
        "host": f"{host}:{port}",
        "players": {
            "online": 0,
            "max": 0,
            "list": []
        },
        "version": None,
        "latency": 0,
        "motd": "",
        "icon": None
    }

    try:
        # 创建服务器对象
        server = JavaServer(host, port)
        
        # 获取基础状态信息
        status: JavaStatusResponse = server.status()
        result.update({
            "online": True,
            "players": {
                "online": status.players.online,
                "max": status.players.max,
                "list": []  # 基础状态不包含玩家列表
            },
            "version": status.version.name,
            "latency": round(status.latency, 2),
            "motd": status.motd.to_plain(),
            #"icon": status.favicon  # Base64编码的服务器图标
        })

        # 尝试获取详细玩家列表（需要服务器启用query）
        return result

    except Exception as main_error:
        result["error"] = f"连接失败: {str(main_error)}"
        return result

# 使用示例
if __name__ == "__main__":
    server_info = get_server_info(str(mc_list[0]))  # 替换为你的服务器地址
    
    if server_info["online"]:
        print(f"服务器 {server_info['host']} 在线")
        print(f"版本: {server_info['version']}")
        print(f"最新延迟: {server_info['latency']}ms")
        print(f"玩家: {server_info['players']['online']}/{server_info['players']['max']}")
    else:
        print(f"服务器离线: {server_info.get('error', '未知错误')}")