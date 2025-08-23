# Pychat 问题排除指南

本文档记录了在 Pychat 项目启动和运行过程中可能遇到的常见问题及其解决方案。

## 目录

1. [环境配置问题](#环境配置问题)
2. [依赖安装问题](#依赖安装问题)
3. [服务启动问题](#服务启动问题)
4. [SSL/HTTPS 连接问题](#sslhttps-连接问题)
5. [端口占用问题](#端口占用问题)

---

## 环境配置问题

### 问题1: Python 版本兼容性问题

**现象:**
```
ERROR: Could not find a version that satisfies the requirement Django==2.2.4
```

**原因:** Django 2.2.4 不兼容 Python 3.12+ 版本

**解决方案:**
1. 使用 Python 3.8 版本
2. 创建虚拟环境:
   ```bash
   # macOS/Linux
   python3.8 -m venv venv38
   source venv38/bin/activate
   
   # Windows
   python3.8 -m venv venv38
   venv38\Scripts\activate
   ```
3. 验证 Python 版本:
   ```bash
   python --version  # 应显示 Python 3.8.x
   ```

### 问题2: 系统依赖缺失

**现象:**
```
error: Microsoft Visual C++ 14.0 is required
# 或
fatal error: 'Python.h' file not found
```

**解决方案:**

**macOS:**
```bash
brew install python@3.8
xcode-select --install
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.8 python3.8-dev python3.8-venv build-essential
```

**Windows:**
- 安装 Visual Studio Build Tools
- 或安装 Visual Studio Community

---

## 依赖安装问题

### 问题3: CORS 模块缺失

**现象:**
```
ModuleNotFoundError: No module named 'corsheaders'
```

**原因:** 缺少 django-cors-headers 依赖

**解决方案:**
```bash
pip install django-cors-headers==3.2.1
```

**注意:** 必须使用 3.2.1 版本以兼容 Django 2.2.4

### 问题4: django-cors-headers 版本冲突

**现象:**
```
django-cors-headers 3.13.0 requires Django>=3.2
```

**解决方案:**
1. 卸载不兼容版本:
   ```bash
   pip uninstall django-cors-headers
   ```
2. 安装兼容版本:
   ```bash
   pip install django-cors-headers==3.2.1
   ```
3. 确认 Django 版本保持在 2.2.4:
   ```bash
   pip install Django==2.2.4
   ```

### 问题5: Pillow 安装失败

**现象:**
```
ERROR: Failed building wheel for Pillow
```

**解决方案:**

**macOS:**
```bash
brew install libjpeg libpng libtiff
pip install Pillow==8.1.0
```

**Ubuntu/Debian:**
```bash
sudo apt install libjpeg-dev libpng-dev libtiff-dev
pip install Pillow==8.1.0
```

---

## 服务启动问题

### 问题6: 前端启动脚本错误

**现象:**
```
npm ERR! Missing script: "dev"
```

**原因:** package.json 中没有 "dev" 脚本

**解决方案:**
使用正确的启动命令:
```bash
npm start  # 而不是 npm run dev
```

### 问题7: Redis 连接失败

**现象:**
```
redis.exceptions.ConnectionError: Error 61 connecting to localhost:6379
```

**解决方案:**
1. 启动 Redis 服务:
   ```bash
   # macOS (使用 Homebrew)
   brew services start redis
   
   # Ubuntu/Debian
   sudo systemctl start redis-server
   
   # 手动启动
   redis-server
   ```
2. 验证 Redis 运行:
   ```bash
   redis-cli ping  # 应返回 PONG
   ```

---

## SSL/HTTPS 连接问题

### 问题8: SSL 连接重置错误

**现象:**
```
Xhr.ts:124 http GET out: /validate_user ::: , status: 0
Failed to load resource: net::ERR_CONNECTION_RESET
SSL Error: [SSL: WRONG_VERSION_NUMBER] wrong version number
```

**原因:** 前端使用 HTTP 协议连接配置了 SSL 的 Tornado 服务器

**解决方案:**
1. 修改前端 API 配置文件 `frontend/src/ts/utils/runtimeConsts.ts`:
   ```typescript
   // 将 HTTP 改为 HTTPS
   export const WS_API_URL = `wss://${BACKEND_CURRENT_ADDRESS}/ws`;
   export const XHR_API_URL = `https://${BACKEND_CURRENT_ADDRESS}/api`;
   export const MEDIA_API_URL = `https://${BACKEND_CURRENT_ADDRESS}`;
   ```
2. 重启前端开发服务器:
   ```bash
   npm start
   ```

### 问题9: SSL 证书警告

**现象:** 浏览器显示 "您的连接不是私密连接" 或 "证书无效"

**解决方案:**

**方法一：直接访问并信任证书（推荐）**
1. 点击 "高级" 或 "Advanced"
2. 点击 "继续访问" 或 "Proceed to localhost (unsafe)"
3. 这是开发环境的自签名证书，属于正常现象

**方法二：通过钥匙串访问管理证书（macOS Safari）**
1. 打开 "钥匙串访问" 应用（Applications > Utilities > Keychain Access）
2. 在左侧选择 "系统" 钥匙串
3. 在搜索框中输入 "localhost" 找到相关证书
4. 双击证书打开详细信息
5. 展开 "信任" 部分
6. 将 "使用此证书时" 设置为 "始终信任"
7. 关闭窗口并输入管理员密码确认更改
8. 重启Safari浏览器

**方法三：使用其他浏览器测试**
- Chrome：通常会显示警告但允许继续访问
- Firefox：可以添加安全例外
- 建议在开发阶段使用Chrome进行测试

### 问题10: 网络IP地址SSL连接失败

**现象:**
- `https://localhost:8080` 可以正常访问
- `https://192.168.1.x:8080` 出现连接错误或证书无效
- 需要在其他设备上测试功能时无法访问

**原因:** SSL证书只包含 `DNS:localhost`，不包含局域网IP地址

**解决方案:**
1. **修改证书配置文件:**
   ```bash
   cd frontend/build/certs
   # 编辑 v3.ext 文件，添加IP地址
   ```
   
   在 `v3.ext` 文件中添加:
   ```
   [v3_req]
   authorityKeyIdentifier=keyid,issuer
   basicConstraints=CA:FALSE
   keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
   subjectAltName = @alt_names
   
   [alt_names]
   DNS.1 = localhost
   IP.1 = 192.168.1.x  # 替换为实际IP地址
   ```

2. **重新生成SSL证书:**
   ```bash
   cd frontend/build/certs
   
   # 生成新的私钥
   openssl genrsa -out server.key 2048
   
   # 生成证书签名请求
   openssl req -new -key server.key -out server.csr -subj "/C=US/ST=CA/L=San Francisco/O=Pychat/OU=Dev/CN=localhost"
   
   # 生成自签名证书
   openssl x509 -req -in server.csr -signkey server.key -out server.crt.pem -days 365 -extensions v3_req -extfile v3.ext
   
   # 更新私钥文件名
   cp server.key private.key.pem
   ```

3. **验证证书配置:**
   ```bash
   openssl x509 -in server.crt.pem -text -noout | grep -A 10 "Subject Alternative Name"
   # 应显示: DNS:localhost, IP Address:192.168.1.x
   ```

4. **重启前端服务:**
   ```bash
   # 停止当前前端服务
   # 重新启动
   cd frontend
   npm start
   ```

**验证方法:**
- 使用 `https://localhost:8080` 在本机访问
- 使用 `https://192.168.1.x:8080` 在其他设备访问
- 两个地址都应该正常工作，无连接错误

**注意事项:**
- 首次在其他设备访问时，仍需接受自签名证书警告
- 确保防火墙允许8080端口访问
- 所有设备需在同一局域网内

---

## 端口占用问题

### 问题11: 端口被占用

**现象:**
```
Port 8080 is in use, trying another one...
Error: listen EADDRINUSE: address already in use :::8888
```

**解决方案:**

**查找占用端口的进程:**
```bash
# macOS/Linux
lsof -i :8888
lsof -i :8000
lsof -i :8081

# Windows
netstat -ano | findstr :8888
```

**终止占用进程:**
```bash
# macOS/Linux
kill -9 <PID>

# Windows
taskkill /PID <PID> /F
```

**或使用不同端口:**
```bash
# Tornado
python manage.py start_tornado --port 8889 --host 0.0.0.0

# Django
python manage.py runserver 0.0.0.0:8001
```

---

## 验证环境命令

运行以下命令验证环境配置是否正确:

```bash
# 1. 检查 Python 版本
python --version

# 2. 检查关键依赖
pip list | grep -E "Django|tornado|redis|Pillow|django-cors-headers"

# 3. 检查 Redis 连接
redis-cli ping

# 4. 检查端口占用
lsof -i :8888 -i :8000 -i :8081

# 5. 测试 Django 配置
python manage.py check
```

---

## 完整启动流程

按以下顺序启动所有服务:

1. **启动 Redis:**
   ```bash
   redis-server
   ```

2. **启动 Tornado API 服务器:**
   ```bash
   cd backend
   source venv38/bin/activate
   python manage.py start_tornado --port 8888 --host 0.0.0.0
   ```

3. **启动 Django 静态文件服务器:**
   ```bash
   cd backend
   source venv38/bin/activate
   python manage.py runserver 0.0.0.0:8000
   ```

4. **启动前端开发服务器:**
   ```bash
   cd frontend
   npm start
   ```

5. **访问应用:**
   - 前端应用: https://localhost:8081
   - API 服务: https://localhost:8888
   - 静态文件: http://localhost:8000

---

## 数据库相关问题

### 问题12：数据库表缺失错误

**现象：**
- 访问API接口时出现500内部服务器错误
- 错误信息显示：`sqlite3.OperationalError: no such table: chat_user`
- Tornado服务器日志中出现数据库表不存在的错误

**原因：**
- Django应用的数据库迁移文件缺失或未执行
- `chat`应用缺少初始迁移文件（0001_initial.py）
- 数据库中没有创建必要的表结构

**解决方案：**
```bash
# 1. 进入backend目录
cd backend

# 2. 激活虚拟环境
source venv38/bin/activate

# 3. 为chat应用创建初始迁移文件
python manage.py makemigrations chat

# 4. 应用所有迁移
python manage.py migrate
```

**验证方法：**
```bash
# 检查数据库表是否创建成功
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat.settings')
import django
django.setup()
from django.db import connection
cursor = connection.cursor()
cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'chat_%';\")
print('Chat tables:', [row[0] for row in cursor.fetchall()])
"

# 测试API接口
curl -k -X POST "https://localhost:8888/api/validate_user?username=testuser" -v
```

**预期结果：**
- 数据库中应包含：chat_user、chat_channel、chat_message等表
- API接口返回200状态码
- 不再出现表缺失错误

### 问题13：注册API外键约束失败

**现象：**
- 用户点击注册按钮后，POST `https://localhost:8888/api/register` 返回500内部服务器错误
- 错误信息：`sqlite3.IntegrityError: FOREIGN KEY constraint failed`
- 错误发生在 `RoomUsers(user_id=user_profile.id, room_id=settings.ALL_ROOM_ID, notifications=False).save()` 这一行

**原因分析：**
1. 注册过程中尝试将新用户添加到主房间（`ALL_ROOM_ID=1`）
2. 数据库中不存在id为1的Room记录
3. `RoomUsers`表的`room`字段是外键，引用`Room`表，因此插入失败

**解决方案：**
1. **检查ALL_ROOM_ID设置：**
   ```bash
   # 在backend/chat/settings_base.py中找到ALL_ROOM_ID = 1
   ```

2. **验证Room记录是否存在：**
   ```bash
   DJANGO_SETTINGS_MODULE=chat.settings python -c "from django.db import connection; cursor = connection.cursor(); cursor.execute('SELECT id, name, channel_id FROM chat_room WHERE id = 1'); result = cursor.fetchone(); print('Room with id=1:', result if result else 'Not found')"
   ```

3. **创建主频道和主房间：**
   ```bash
   python manage.py shell -c "
   from chat.models import Channel, Room
   from django.db import transaction
   
   with transaction.atomic():
       # 创建主频道
       channel, created = Channel.objects.get_or_create(
           id=1,
           defaults={'name': 'Main', 'disabled': False, 'creator': None}
       )
       print(f'Channel created: {created}, Channel: {channel}')
       
       # 创建主房间
       room, created = Room.objects.get_or_create(
           id=1,
           defaults={
               'name': 'Main',
               'channel': channel,
               'is_main_in_channel': True,
               'p2p': False,
               'disabled': False,
               'creator': None
           }
       )
       print(f'Room created: {created}, Room: {room}')
   "
   ```

**验证方法：**
1. **测试注册API：**
   ```bash
   curl -X POST "https://localhost:8888/api/register?username=testuser&password=testpass123&email=test@example.com" -k -v
   ```

2. **检查响应状态：**
   - 应该返回HTTP 200 OK状态码
   - 不再出现外键约束失败错误

**预期结果：**
- 注册API正常工作，返回200状态码
- 新用户成功创建并自动加入主房间
- 外键约束问题完全解决

### 问题14：前端WebSQL初始化失败

**现象：**
```
Unable to init websql, because Error: DatabaseWrapper not supported
     at new DatabaseWrapper (DatabaseWrapper.ts:62:13) 
     at init (main.ts:126:15) 
     at main.ts:195:3 . Falling back to localstorage
```

**原因分析：**
1. **WebSQL已被废弃**: WebSQL数据库API于2009年推出，2010年废弃，现代浏览器已不再支持
2. **浏览器兼容性问题**: 
   - Chrome从版本119开始完全移除WebSQL支持
   - Firefox从未实现WebSQL
   - Safari在2019年移除了WebSQL支持
3. **检测逻辑**: `DatabaseWrapper.ts`中的`if (!window.openDatabase)`检测到浏览器不支持WebSQL时抛出错误

**解决方案：**
这是一个预期的行为，不是错误：

1. **系统设计**: 应用已经实现了回退机制，当WebSQL不可用时自动使用LocalStorage
2. **LocalStorage回退**: `main.ts`中的try-catch块捕获WebSQL错误并回退到LocalStorage存储
3. **现代替代方案**: 建议迁移到IndexedDB，这是现代浏览器支持的标准客户端数据库API

**验证方法：**
1. 检查浏览器控制台确认回退到LocalStorage成功
2. 验证应用功能正常工作（消息存储、用户数据等）
3. 确认没有数据丢失或功能异常

**预期结果：**
- 应用正常运行，使用LocalStorage作为存储后端
- 所有聊天功能正常工作
- 用户数据正确保存和加载

---

## 获取帮助

如果遇到本文档未涵盖的问题:

1. 检查终端输出的完整错误信息
2. 联系项目维护者获取帮助
3. 确认所有依赖版本与 requirements.txt 一致
4. 验证 Python 版本为 3.8.x
5. 确保所有服务按正确顺序启动

记住：大多数问题都与环境配置和版本兼容性相关。严格按照文档要求配置环境通常可以避免大部分问题。