

## 项目目录

Shiguang/
├── docker-compose.yml # Docker 编排文件
├── nginx.conf # Nginx 配置文件
├── backend/ # Django 后端代码目录
│ ├── manage.py
│ ├── Shiguang/ # Django 项目目录
│ └── Dockerfile # Django 容器构建文件
├── frontend/shiguang #Vue前端代码目录
└── README文档

---

## 🛠️ 技术栈

- **前端框架：Vue+Vite**

- **后端框架**：[Django](https://www.djangoproject.com/) 
- **数据库**：MySQL 8.0
- **缓存服务**：Redis 7.0
- **Web 服务器**：Nginx
- **容器化部署**：Docker + Docker Compose

---

## 🚀 后端部署

### 1. 克隆项目

```bash
git clone https://github.com/yourname/yourrepo.git 
cd yourrepo
```

### 2.构建并启动服务

```bash
docker-compose up -d --build
```

### 3. 数据库迁移

```bash
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
```

### 4. 创建管理员账户（可选）

```bash
docker-compose exec backend python manage.py createsuperuser
```

### 5. 收集静态文件（生产环境必须）

```bash
docker-compose exec backend python manage.py collectstatic --noinp
```



## 后端管理后台

```bash
http://localhost/admin
http://localhost/api
http://localhost/api/docs
```

默认超级用户：username:shiguang     password:shiguang

## 🚀 前端部署

首次运行或从 Git 拉取项目后，需要先安装依赖：

```bash
npm install
```

```bash
npm run build
```

> 默认会生成一个 `dist/` 目录，里面包含所有静态资源（HTML、CSS、JS、图片等），可以用于部署。 

