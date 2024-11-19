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
COPY /frontend/project /app/frontend/project
WORKDIR /app/frontend/project
COPY /frontend/project/src/api/upload.ts /app/frontend/project/src/api/upload.ts


# 安装前端依赖并添加调试信息

RUN pnpm install --registry=https://registry.npmmirror.com  && \
    pnpm add -D typescript@latest vue-tsc@latest  --registry=https://registry.npmmirror.com  && \
    pnpm run build

COPY backend/ /app/backend
# RUN pnpm run build
# pnpm add -D typescript@latest vue-tsc@latest  --registry=https://registry.npmmirror.com  
# 安装后端依赖
WORKDIR /app/backend

RUN pip install --no-cache-dir -r requirements.txt 


RUN mkdir -p /var/log/fastapi /var/log/nginx 

COPY deploy/config/nginx_conf/* /etc/nginx/conf.d/
COPY deploy/config/supervisor/*.conf /etc/supervisor/conf.d/
EXPOSE 9000
CMD ["sh", "-c", "/usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf"]

