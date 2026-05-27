
# 新闻资讯平台后端系统

基于 FastAPI 构建的高性能新闻资讯平台后端 API 服务。

## 技术栈

- **框架**: FastAPI 0.109.0
- **数据库**: MySQL 8.0 + SQLAlchemy 2.0 (Async)
- **缓存**: Redis 7.0
- **认证**: JWT (JSON Web Token)
- **密码加密**: bcrypt
- **异步驱动**: aiomysql
- **测试**: pytest + httpx

## 核心功能

### 用户系统
- 用户注册/登录（JWT 认证）
- Access Token + Refresh Token 双令牌机制
- 用户信息管理
- 密码修改

### 新闻系统
- 新闻分类管理
- 新闻列表（分页 + 缓存）
- 新闻详情（浏览量统计）
- 相关新闻推荐

### 互动功能
- 收藏/取消收藏
- 收藏列表
- 浏览历史
- 历史记录管理

### 性能优化
- Redis 二级缓存
- 数据库索引优化
- API 限流保护
- 异步数据库操作

## 快速开始

### 1. 环境要求

- Python 3.11+
- MySQL 8.0+
- Redis 7.0+

### 2. 克隆项目

```bash
git clone https://github.com/your-username/toutiao_backend.git
cd toutiao_backend
```

### 3. 创建虚拟环境

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
```

### 5. 配置环境变量

复制环境变量模板并填写实际配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置以下内容：

```env
# 数据库配置
DATABASE_URL=mysql+aiomysql://用户名:密码@主机:端口/数据库名?charset=utf8mb4

# Redis 配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# JWT 配置（务必修改为强密钥）
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# 应用配置
DEBUG_MODE=false
APP_HOST=0.0.0.0
APP_PORT=8000

# CORS 配置（逗号分隔多个来源）
ALLOWED_ORIGINS=http://localhost:5173
```

### 6. 初始化数据库

在 MySQL 中创建数据库：

```sql
CREATE DATABASE news_app DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

启动应用后，SQLAlchemy 会自动创建表结构。

### 7. 启动应用

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 8. 访问 API 文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 接口

### 用户模块 `/api/user`

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | `/api/user/register` | 用户注册 | 否 |
| POST | `/api/user/login` | 用户登录 | 否 |
| POST | `/api/user/refresh` | 刷新 Token | 否 |
| GET | `/api/user/info` | 获取用户信息 | 是 |
| PUT | `/api/user/update` | 更新用户信息 | 是 |
| PUT | `/api/user/password` | 修改密码 | 是 |

### 新闻模块 `/api/news`

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/api/news/categories` | 获取新闻分类 | 否 |
| GET | `/api/news/list` | 获取新闻列表 | 否 |
| GET | `/api/news/detail` | 获取新闻详情 | 否 |

### 收藏模块 `/api/favorite`

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | `/api/favorite/add` | 添加收藏 | 是 |
| DELETE | `/api/favorite/remove` | 取消收藏 | 是 |
| GET | `/api/favorite/list` | 收藏列表 | 是 |
| GET | `/api/favorite/check` | 检查是否已收藏 | 是 |

### 历史模块 `/api/history`

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | `/api/history/add` | 添加历史记录 | 是 |
| GET | `/api/history/list` | 历史记录列表 | 是 |
| DELETE | `/api/history/delete/{id}` | 删除历史记录 | 是 |
| DELETE | `/api/history/clear` | 清空历史记录 | 是 |

## 项目结构

```
toutiao_backend/
├── main.py                 # 应用入口
├── config/                 # 配置模块
│   ├── db_conf.py          #   数据库连接
│   └── cache_conf.py       #   Redis 缓存连接
├── models/                 # SQLAlchemy ORM 模型
│   ├── __init__.py         #   共享 Base 类
│   ├── news.py             #   分类 + 新闻表
│   ├── users.py            #   用户表
│   ├── favorite.py         #   收藏表
│   └── history.py          #   浏览历史表
├── schemas/                # Pydantic 请求/响应模型
├── crud/                   # 数据库操作层
├── routers/                # 路由处理器
├── cache/                  # Redis 缓存辅助
├── utils/                  # 工具模块
│   ├── auth.py             #   JWT 认证依赖
│   ├── jwt_handler.py      #   JWT 创建/验证
│   ├── logger.py           #   日志配置
│   ├── rate_limiter.py     #   限流配置
│   ├── response.py         #   统一响应格式
│   └── exception.py        #   全局异常处理
└── requirements.txt        # 依赖列表
```

## 许可证

[MIT License](LICENSE)
