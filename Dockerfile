# 基础镜像阶段
FROM python:3.10.4-slim-buster AS base
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y nginx supervisor htop wget curl iputils-ping procps telnet vim git sudo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# 安装 Node.js 和 pnpm
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g npm@latest --registry=https://registry.npmmirror.com && \
    npm install -g n --registry=https://registry.npmmirror.com && \
    n 20.14.0 && \
    hash -r && \
    npm install -g pnpm --registry=https://registry.npmmirror.com

# 依赖安装和最终镜像阶段  
FROM base AS final

ENV APP_ENV=prod
WORKDIR /app

# 设置git凭证参数,在构建时通过--build-arg传入

# 安装前端依赖
COPY frontend/ /app/frontend/
WORKDIR /app/frontend
RUN pnpm install --registry=https://registry.npmmirror.com && \
    pnpm run build

# 安装后端依赖
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --index-url https://pypi.tuna.tsinghua.edu.cn/simple 

# 复制后端代码和配置文件
COPY backend/ /app/
COPY .env /app/
COPY depoly/config/nginx_conf/ /etc/nginx/conf.d/
COPY depoly/config/supervisor/ /etc/supervisor/conf.d/

EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]