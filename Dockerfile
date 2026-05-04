FROM python:3.11-slim

RUN apt-get update && apt-get install -y openssh-server && rm -rf /var/lib/apt/lists/*

# SSH config for Azure App Service
RUN echo "root:Docker!" | chpasswd
COPY sshd_config /etc/ssh/sshd_config

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .
COPY init.sh /init.sh
RUN chmod +x /init.sh

EXPOSE 8000 2222

CMD ["/init.sh"]
