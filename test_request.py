import requests
import hmac
import hashlib
import urllib.parse
from datetime import datetime

def baidu_search(query: str, api_key: str, secret_key: str) -> dict:
    """
    使用百度搜索开放平台 API 查询搜索结果
    
    参数:
        query: 搜索关键词（如 "Python 教程"）
        api_key: 百度开放平台申请的 API Key
        secret_key: 百度开放平台申请的 Secret Key
    
    返回:
        dict: 百度 API 返回的搜索结果（JSON 格式）
    """
    # 百度搜索 API 的端点（根据文档确认最新地址）
    url = "https://aip.baidubce.com/rpc/2.0/antiproduct/v1/search/query"
    
    # 固定参数（根据 API 文档调整）
    params = {
        "query": query,          # 搜索关键词
        "rn": 10,                # 返回结果数量（最多 100）
        "pn": 0,                 # 偏移量（从第 0 条开始）
        "ie": "utf-8",           # 输入编码
        "oe": "utf-8",           # 输出编码
        "timestamp": int(datetime.now().timestamp()),  # 当前时间戳（秒）
    }
    
    # 生成签名（关键步骤，需严格按照百度文档要求）
    # 1. 对参数按字典序排序，拼接成字符串
    sorted_params = sorted(params.items(), key=lambda x: x[0])
    raw_str = urllib.parse.urlencode(sorted_params)
    
    # 2. 使用 Secret Key 对原始字符串进行 HMAC-SHA256 加密
    signature = hmac.new(
        secret_key.encode("utf-8"),
        raw_str.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    
    # 3. 将签名添加到请求参数中
    params["sign"] = signature
    
    try:
        # 发送 GET 请求
        response = requests.get(url, params=params)
        response.raise_for_status()  # 检查 HTTP 错误（如 404、500）
        return response.json()       # 返回 JSON 格式的搜索结果
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return {}
    except ValueError as e:
        print(f"解析 JSON 失败: {e}")
        return {}

if __name__ == "__main__":
    # 替换为你自己的 API Key 和 Secret Key
    YOUR_API_KEY = "你的API Key"
    YOUR_SECRET_KEY = "你的Secret Key"
    
    # 搜索关键词（示例："Python 开发者 薪资水平"）
    search_query = "Python 开发者 薪资水平"
    
    # 执行搜索
    result = baidu_search(search_query, YOUR_API_KEY, YOUR_SECRET_KEY)
    
    # 打印结果（根据实际返回结构调整）
    if result.get("error_code") == 0:
        print("搜索成功！结果如下：")
        for item in result.get("result", []):
            print(f"标题: {item.get('title')}")
            print(f"链接: {item.get('url')}")
            print(f"摘要: {item.get('abstract')}\n")
    else:
        print(f"搜索失败，错误码: {result.get('error_code')}, 错误信息: {result.get('error_msg')}")
