from slowapi import Limiter
from slowapi.util import get_remote_address

# 创建限流器
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200/minute"]  # 默认限制：每分钟200次请求
)

# 自定义限流策略
RATE_LIMITS = {
    "login": "5/minute",      # 登录：每分钟5次
    "register": "3/minute",   # 注册：每分钟3次
    "news_list": "100/minute", # 新闻列表：每分钟100次
    "search": "30/minute",     # 搜索：每分钟30次
}