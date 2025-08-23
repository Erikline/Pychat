# Pychat - 开源实时聊天应用

Pychat 是一个基于 Django + Tornado + Vue3 构建的现代化实时聊天应用，支持私聊、群聊、文件传输、表情符号等功能。

## 功能特性

- ✅ 实时消息传输（WebSocket）
- ✅ 私聊与群聊支持
- ✅ 文件/图片传输
- ✅ 表情符号系统
- ✅ 用户在线状态
- ✅ 消息已读/未读状态
- ✅ 响应式设计
- ✅ 推送通知

## 技术栈

### 后端
- **Django 2.2.4** - Web框架
- **Tornado 4.5.3** - 异步Web服务器
- **Redis** - 消息队列与缓存
- **MySQL** - 主数据库（生产环境）
- **SQLite** - 开发环境数据库

### 前端
- **Vue 3** - 渐进式JavaScript框架
- **Vite** - 构建工具
- **TypeScript** - 类型安全
- **WebSocket** - 实时通信

## 系统要求

### 必需组件
- **Python 3.8** (强烈推荐，避免使用 Python 3.12+ 因为 Django 2.2.4 不兼容)
- **Node.js 16+**
- **Redis 5.0+**
- **OpenSSL**（用于HTTPS证书）
- **系统依赖**：
  - macOS: `brew install jpeg` (用于 Pillow 图像处理)
  - Ubuntu: `sudo apt-get install libjpeg-dev`

### 推荐环境
- macOS 10.15+ / Ubuntu 20.04+ / Windows 10+
- 8GB+ RAM
- 2GB+ 可用磁盘空间

## 环境配置说明

### Python 版本兼容性问题

⚠️ **重要提示**: 本项目使用 Django 2.2.4，该版本与 Python 3.12+ 不兼容（缺少 `distutils` 模块）。

**解决方案**:
1. 使用 Python 3.8 (推荐)
2. 创建独立的虚拟环境
3. 安装兼容版本的依赖包

### 依赖包版本

后端关键依赖版本:
- Django==2.2.4
- tornado==4.5.3
- tornado-redis==2.4.18
- django-cors-headers==3.2.1 (兼容 Django 2.2.4)
- Pillow>=8.1.0
- redis==2.10.6

## 快速开始

### 1. 克隆项目

```bash
# 项目已从本地获取
cd pychat
```

### 2. 后端配置与启动

#### 2.1 创建配置文件
```bash
# 创建 settings.py 指向本地配置
echo "from .settings_local import *" > backend/chat/settings.py
```

#### 2.2 安装Python依赖

⚠️ **重要**: 必须使用 Python 3.8 创建虚拟环境以避免兼容性问题

```bash
cd backend

# 安装系统依赖（必须先执行）
# macOS:
brew install jpeg

# Ubuntu/Debian:
# sudo apt-get install libjpeg-dev zlib1g-dev

# 使用 Python 3.8 创建虚拟环境
# macOS (如果有多个Python版本):
/usr/local/bin/python3.8 -m venv venv38
source venv38/bin/activate

# 或者使用系统默认Python 3.8:
# python3.8 -m venv venv38
# source venv38/bin/activate

# Windows:
# python3.8 -m venv venv38
# venv38\Scripts\activate

# 验证Python版本
python --version  # 应该显示 Python 3.8.x

# 安装依赖
pip install -r requirements.txt

# 安装兼容的django-cors-headers版本
pip install django-cors-headers==3.2.1
```

#### 2.3 数据库配置
开发环境使用SQLite，配置已包含在 `settings_local.py` 中，无需额外配置。

#### 2.4 启动Redis
```bash
# macOS (使用Homebrew)
brew install redis
brew services start redis

# Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis

# Docker
docker run -d -p 6379:6379 redis:alpine

# 验证Redis运行
redis-cli ping
# 应该返回 PONG
```

#### 2.5 数据库迁移
```bash
cd backend
python manage.py migrate
```

#### 2.6 启动后端服务

⚠️ **重要**: Pychat 需要同时启动三个独立的服务

**终端1 - 启动 Tornado API 服务器 (端口 8888)**:
```bash
cd backend
source venv38/bin/activate  # 激活Python 3.8虚拟环境
python manage.py start_tornado --port 8888 --host 0.0.0.0
```

**终端2 - 启动 Django 静态文件服务器 (端口 8000)**:
```bash
cd backend
source venv38/bin/activate  # 激活Python 3.8虚拟环境
python manage.py runserver 0.0.0.0:8000
```

### 3. 前端配置与启动

#### 3.1 安装依赖
```bash
cd frontend

# 安装依赖（处理Vue3兼容性问题）
npm install --legacy-peer-deps

# 安装Vue3兼容的 vue-class-component
npm install vue-class-component@8.0.0-rc.1 --save --legacy-peer-deps
```

#### 3.2 启动前端开发服务器

**终端3 - 启动 Vite 前端服务器**:
```bash
cd frontend
npm start  # 通常会在端口 8080 或 8081 启动
```

服务器会自动选择可用端口，通常是:
- 首选: https://localhost:8080
- 备选: https://localhost:8081 (如果8080被占用)

#### 3.3 构建生产版本
```bash
npm run build
```

### 4. 访问应用

开发环境访问地址：
- **前端应用**: https://localhost:8081 (或 8080)
- **API服务**: https://localhost:8888 (Tornado)
- **静态文件**: https://localhost:8000 (Django)

**服务架构说明**:
- **Tornado (8888)**: 处理 WebSocket 连接和 API 请求 (`/api/*`, `/ws`)
- **Django (8000)**: 提供静态文件和媒体文件服务
- **Vite (8081)**: 前端开发服务器，提供热重载

⚠️ **注意**: 首次访问时会提示证书风险，请点击"继续访问"。

### 5. 启动顺序

建议按以下顺序启动服务:
1. 启动 Redis 服务
2. 启动 Tornado API 服务器 (端口 8888)
3. 启动 Django 静态文件服务器 (端口 8000) 
4. 启动前端开发服务器 (端口 8081)

所有服务启动成功后，访问前端地址即可使用应用。

## 项目结构

```
pychat/
├── backend/                 # 后端代码
│   ├── chat/               # Django应用
│   │   ├── models.py       # 数据模型
│   │   ├── settings*.py    # 配置文件
│   │   └── tornado/        # Tornado相关
│   ├── migrations/         # 数据库迁移
│   ├── requirements-local.txt  # 本地依赖（无MySQL）
│   └── manage.py          # Django管理脚本
├── frontend/               # 前端代码
│   ├── src/               # 源代码
│   │   ├── ts/           # TypeScript文件
│   │   ├── vue/          # Vue组件
│   │   └── assets/       # 静态资源
│   └── build/            # 构建配置
├── screen_cast_extension/  # 屏幕共享扩展
└── README.md
```

## 故障排除

### 常见环境问题

#### 1. Python 版本兼容性问题

**问题**: `ModuleNotFoundError: No module named 'distutils'`

**原因**: Python 3.12+ 移除了 `distutils` 模块，Django 2.2.4 依赖该模块

**解决方案**:
```bash
# 使用 Python 3.8 创建新的虚拟环境
/usr/local/bin/python3.8 -m venv venv38
source venv38/bin/activate
pip install -r requirements.txt
```

#### 2. Pillow 安装失败

**问题**: `error: Microsoft Visual C++ 14.0 is required` 或 `jpeg` 相关错误

**解决方案**:
```bash
# macOS
brew install jpeg

# Ubuntu/Debian
sudo apt-get install libjpeg-dev zlib1g-dev

# 然后重新安装
pip install Pillow>=8.1.0
```

#### 3. CORS 错误

**问题**: 前端无法访问 API，出现 CORS 错误

**原因**: 只启动了 Django 服务器，API 端点在 Tornado 服务器中

**解决方案**: 确保同时启动三个服务:
- Tornado API 服务器 (8888)
- Django 静态文件服务器 (8000)
- 前端开发服务器 (8081)

#### 4. django-cors-headers 版本不兼容

**问题**: `django-cors-headers 3.13.0 requires Django>=3.2`

**解决方案**:
```bash
pip install django-cors-headers==3.2.1
```

#### 5. 端口被占用

**问题**: `Address already in use`

**解决方案**:
```bash
# 查找占用端口的进程
lsof -i :8888  # 或其他端口号

# 终止进程
kill -9 <PID>
```

### 验证环境

启动所有服务后，可以通过以下方式验证:

```bash
# 检查 Tornado API 服务
curl -k https://localhost:8888/api/validate_user

# 检查 Django 静态文件服务
curl -I http://localhost:8000/

# 检查前端服务
curl -k https://localhost:8081/
```

## 开发指南

### 环境变量

#### 后端环境变量
```bash
# 可选：自定义Redis配置
export REDIS_HOST=localhost
export REDIS_PORT=6379
export REDIS_DB=0

# 可选：自定义端口
export DJANGO_SETTINGS_MODULE=chat.settings_local
```

#### 前端环境变量
```bash
# 开发环境
export NODE_ENV=development

# 生产环境
export NODE_ENV=production
```

### 常用命令

#### 后端命令
```bash
# 创建超级用户
python manage.py createsuperuser

# 运行测试
python manage.py test

# 数据库操作
python manage.py makemigrations
python manage.py migrate

# 启动服务
python manage.py start_tornado --port 8888
```

#### 前端命令
```bash
# 开发服务器
npm run start

# 代码检查
npm run start:lint

# 生产构建
npm run build

# 本地预览
npm run serve
```

### 调试技巧

#### 后端调试
1. 在 `settings_local.py` 中设置 `DEBUG = True`
2. 查看控制台输出的SQL语句
3. 使用Django的 `shell_plus`：
   ```bash
   python manage.py shell_plus
   ```

#### 前端调试
1. 浏览器开发者工具 (F12)
2. Vue DevTools扩展
3. 查看Network标签页的WebSocket连接

## 常见问题

### 1. Python 3.12 兼容性问题
**问题**: `ModuleNotFoundError: No module named 'distutils'`
**解决**: 
```bash
# 安装 setuptools
pip install setuptools

# 或降级到 Python 3.8-3.11
```

### 2. Redis连接失败
**问题**: `ConnectionError: Error 61 connecting to localhost:6379`
**解决**: 
```bash
# 检查Redis是否运行
redis-cli ping
# 应该返回 PONG

# 如果未运行，启动Redis
brew services start redis  # macOS
sudo systemctl start redis  # Linux
```

### 2. 证书错误
**问题**: `NET::ERR_CERT_INVALID`
**解决**: 
- 开发环境：浏览器地址栏输入 `thisisunsafe` 绕过
- 生产环境：配置有效的SSL证书

### 3. 端口占用
**问题**: `Address already in use`
**解决**:
```bash
# 查找占用端口的进程
lsof -i :8080  # 前端端口
lsof -i :8888  # 后端端口

# 终止进程
kill -9 <PID>
```

### 5. 前端依赖安装失败
**问题**: `ERESOLVE unable to resolve dependency tree`
**解决**:
```bash
# 使用 legacy-peer-deps 选项
npm install --legacy-peer-deps

# 清理缓存后重试
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

### 6. 数据库迁移失败
**问题**: `django.db.utils.OperationalError`
**解决**:
```bash
# 删除旧的迁移文件和数据库
rm backend/db.sqlite3
find backend/migrations -name "*.py" -not -name "__init__.py" -delete

# 重新迁移
python manage.py makemigrations
python manage.py migrate
```

### 7. Pillow 安装失败
**问题**: `error: jpeg is required unless explicitly disabled`
**解决**:
```bash
# macOS
brew install jpeg zlib

# Ubuntu/Debian
sudo apt-get install libjpeg-dev zlib1g-dev

# 然后重新安装
pip install Pillow
```

### 8. Vue3 兼容性问题
**问题**: `No matching export in "node_modules/vue/dist/vue.runtime.esm-bundler.js"`
**解决**:
```bash
# 安装 Vue3 兼容的 vue-class-component
npm install vue-class-component@8.0.0-rc.1 --save --legacy-peer-deps
```

## 生产部署

### Docker部署（推荐）
```bash
# 使用Docker Compose
docker-compose up -d
```

### 手动部署
1. 配置生产环境变量
2. 使用MySQL作为数据库
3. 配置Nginx反向代理
4. 设置SSL证书
5. 使用PM2管理进程

## 贡献指南

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 支持

- 📧 邮箱支持: dev@pychat.org
- 🐛 问题反馈: [GitHub Issues](https://github.com/akoidan/pychat/issues)
- 💬 社区讨论: [GitHub Discussions](https://github.com/akoidan/pychat/discussions)

## 致谢

感谢所有为这个项目做出贡献的开发者们！