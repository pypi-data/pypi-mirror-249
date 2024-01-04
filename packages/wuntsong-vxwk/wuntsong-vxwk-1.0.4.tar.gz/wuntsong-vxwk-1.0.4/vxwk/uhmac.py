import hmac
import hashlib
import base64


def string_calculate_hmac(key, data):
    # 将密钥和数据转换为字节串
    key_bytes = bytes(key, 'utf-8')
    data_bytes = bytes(data, 'utf-8')

    # 创建一个新的HMAC-SHA1哈希器，传入密钥
    h = hmac.new(key_bytes, data_bytes, hashlib.sha1)

    # 计算HMAC并返回结果，使用Base64编码
    return base64.b64encode(h.digest()).decode('utf-8')
