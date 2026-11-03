# -*- coding: utf-8 -*-
"""
Python requests 库调用公开 API 教程
====================================

本脚本使用 3 个免费、无需 Key 的公开 API 做演示：
  1. JSONPlaceholder  —— 假数据 API（最适合新手练习）
  2. httpbin.org      —— 请求/响应调试工具
  3. Open-Meteo       —— 免费天气预报 API（真·实用）

运行方式：在终端里执行  python requests_tutorial.py
"""

import requests
import json


# ============================================================
# 第 1 步：安装 requests（你已经装好了，这行是给小白留的注释）
#   pip install requests
# ============================================================


# ============================================================
# 示例 1：最简单的 GET 请求
# ------------------------------------------------------------
# GET 就是"向服务器要数据"，就像在浏览器地址栏输入网址。
# ============================================================
def demo_get_simple():
    print("=" * 60)
    print("示例 1：最简单的 GET 请求（获取一条假的待办事项）")
    print("=" * 60)

    # 这是一个免费公开的假数据 API，专门用来测试和学习
    url = "https://jsonplaceholder.typicode.com/todos/1"

    # 发起请求，.get() 就是告诉 requests 用 GET 方法
    response = requests.get(url)

    # 打印一些有用的信息
    print(f"请求 URL：    {url}")
    print(f"状态码：      {response.status_code}   （200 表示成功，404 表示找不到，500 表示服务器出错）")
    print(f"响应头 Content-Type：{response.headers.get('Content-Type')}")
    print(f"原始文本前 100 字：{response.text[:100]}")

    # response.text 是字符串，response.json() 可以直接转成 Python 字典
    data = response.json()
    print(f"\n解析后的 JSON（Python 字典）：")
    print(json.dumps(data, indent=2, ensure_ascii=False))  # indent=2 让它缩进好看点

    # 像用字典一样取值
    print(f"\n这条待办的标题是：{data['title']}")
    print(f"完成了吗？{'是的 ✓' if data['completed'] else '还没 ✗'}")


# ============================================================
# 示例 2：GET 请求带参数（就像网址里的 ?page=2&limit=10）
# ------------------------------------------------------------
# params 参数会自动帮你拼接到 URL 后面，不用自己手写
# ============================================================
def demo_get_with_params():
    print("\n" + "=" * 60)
    print("示例 2：GET 请求带参数（筛选数据）")
    print("=" * 60)

    url = "https://jsonplaceholder.typicode.com/posts"

    # 把参数放字典里，requests 会自动拼成 ?userId=1&_limit=3
    params = {
        "userId": 1,       # 只要 userId=1 的帖子
        "_limit": 3,       # 只要前 3 条
    }

    response = requests.get(url, params=params)

    print(f"实际请求的 URL：{response.url}")   # 你会看到参数已经拼好了
    print(f"状态码：{response.status_code}")

    posts = response.json()
    print(f"\n拿到 {len(posts)} 条帖子：")
    for i, post in enumerate(posts, 1):
        print(f"  {i}. [{post['id']}] {post['title']}")


# ============================================================
# 示例 3：POST 请求（向服务器提交数据）
# ------------------------------------------------------------
# POST 就像"填表单提交"，比如注册账号、发一条微博。
# 用 json= 参数传字典，requests 会自动帮你转成 JSON 格式。
# ============================================================
def demo_post_json():
    print("\n" + "=" * 60)
    print("示例 3：POST 请求（提交一条新帖子）")
    print("=" * 60)

    url = "https://jsonplaceholder.typicode.com/posts"

    # 要提交的数据（Python 字典）
    payload = {
        "title": "我是小白，这是我的第一条帖子",
        "body": "大家好，我正在学习 Python requests 库！",
        "userId": 1,
    }

    # json= 会自动把字典转成 JSON 字符串，并设置 Content-Type: application/json
    response = requests.post(url, json=payload)

    print(f"状态码：{response.status_code}  （POST 成功通常返回 201）")
    print(f"服务器返回：")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))


# ============================================================
# 示例 4：带请求头 headers（模拟浏览器 / 带鉴权）
# ------------------------------------------------------------
# 有些 API 需要特殊的 headers，比如 User-Agent、Authorization。
# ============================================================
def demo_with_headers():
    print("\n" + "=" * 60)
    print("示例 4：自定义请求头 headers")
    print("=" * 60)

    url = "https://httpbin.org/get"  # httpbin 会把你发的所有东西原样返回

    # 模拟一个浏览器（有些 API 会拦截没有 User-Agent 的请求）
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    print(f"我们发送的 User-Agent 被服务器收到了：")
    print(f"  {data['headers']['User-Agent']}")


# ============================================================
# 示例 5：实战！调用真实的免费天气 API
# ------------------------------------------------------------
# Open-Meteo 完全免费、无需注册、无需 API Key。
# ============================================================
def demo_real_weather_api():
    print("\n" + "=" * 60)
    print("示例 5：实战 —— 查询北京今天的天气预报")
    print("=" * 60)

    # Open-Meteo 的 API 文档：https://open-meteo.com/
    # 北京经纬度：纬度 39.9042, 经度 116.4074
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 39.9042,
        "longitude": 116.4074,
        "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
        "timezone": "Asia/Shanghai",
        "forecast_days": 1,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # 如果状态码不是 2xx，会抛出异常

        data = response.json()
        current = data["current"]

        # WMO 天气代码对照表（简化版）
        weather_desc = {
            0: "晴", 1: "大部晴朗", 2: "局部多云", 3: "阴天",
            45: "有雾", 48: "雾凇",
            51: "小毛毛雨", 53: "中毛毛雨", 55: "大毛毛雨",
            61: "小雨", 63: "中雨", 65: "大雨",
            71: "小雪", 73: "中雪", 75: "大雪",
            80: "阵雨", 81: "中阵雨", 82: "大阵雨",
            95: "雷暴", 96: "雷暴伴冰雹", 99: "强雷暴伴冰雹",
        }

        code = current.get("weather_code", 0)
        desc = weather_desc.get(code, f"未知({code})")

        print(f"📍 北京 当前天气：")
        print(f"  🌡️  温度：{current['temperature_2m']}°C")
        print(f"  💧 湿度：{current['relative_humidity_2m']}%")
        print(f"  🌬️  风速：{current['wind_speed_10m']} km/h")
        print(f"  ☁️  天气：{desc}")
        print(f"  🕐 更新时间：{current['time']}")

    except requests.exceptions.Timeout:
        print("❌ 请求超时了，检查一下网络？")
    except requests.exceptions.ConnectionError:
        print("❌ 连不上服务器，可能是网络问题")
    except requests.exceptions.HTTPError as e:
        print(f"❌ 服务器返回了错误：{e}")
    except Exception as e:
        print(f"❌ 出了点别的问题：{e}")


# ============================================================
# 示例 6：错误处理（超实用！）
# ------------------------------------------------------------
# 网络请求一定会遇到各种坑，写好错误处理很重要。
# ============================================================
def demo_error_handling():
    print("\n" + "=" * 60)
    print("示例 6：错误处理（请求一个不存在的 URL）")
    print("=" * 60)

    url = "https://jsonplaceholder.typicode.com/nonexistent"  # 不存在

    try:
        # timeout=(连接超时, 读取超时)，单位秒；只写一个数字就是两者一样
        response = requests.get(url, timeout=(3, 10))

        # 下面这行很关键！状态码不是 2xx 就会抛出 HTTPError
        # 不写的话，404 也会被当成"成功执行"
        response.raise_for_status()

    except requests.exceptions.Timeout:
        print("⏰ 超时了")
    except requests.exceptions.ConnectionError:
        print("📡 网络连不上")
    except requests.exceptions.HTTPError as e:
        print(f"🚫 HTTP 错误：{e}")           # 会显示 404 Client Error
        print(f"   状态码：{response.status_code}")  # 也可以自己看
    except requests.exceptions.RequestException as e:
        print(f"❓ 其他请求异常：{e}")
    else:
        print("✅ 一切顺利！")


# ============================================================
# 示例 7：会话 Session（批量请求时更高效）
# ------------------------------------------------------------
# Session 会自动保持 Cookie，并且复用 TCP 连接，速度更快。
# ============================================================
def demo_session():
    print("\n" + "=" * 60)
    print("示例 7：用 Session 发多次请求（更高效）")
    print("=" * 60)

    # 创建一个会话
    with requests.Session() as session:
        # 可以给 Session 设置默认的 headers / timeout / auth
        session.headers.update({
            "User-Agent": "MyApp/1.0",
        })

        # 连续发 3 个请求，Session 会复用连接
        for i in range(1, 4):
            resp = session.get(f"https://jsonplaceholder.typicode.com/posts/{i}")
            title = resp.json()["title"][:50]
            print(f"  #{i}: {title}...")

    # with 块结束后 Session 自动关闭


# ============================================================
# 主函数：依次运行所有示例
# ============================================================
if __name__ == "__main__":
    print("\n🚀 requests 库小白教程 —— 开始运行！\n")

    demo_get_simple()
    demo_get_with_params()
    demo_post_json()
    demo_with_headers()
    demo_error_handling()    # 先跑错误处理，因为 weather API 可能偶尔连不上
    demo_session()
    demo_real_weather_api()  # 放最后，因为需要外网访问

    print("\n" + "=" * 60)
    print("🎉 所有示例跑完啦！回到代码里慢慢研究吧～")
    print("=" * 60)
