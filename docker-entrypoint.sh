#!/usr/bin/env bash
set -xe


upshost="${UPS_HOST:-127.0.0.1}"
upsport="${UPS_PORT:-3493}"
upsuser="${UPS_USER:-monuser}"
upspassword="${UPS_PASSWORD:-secret}"

telegram_bot_token="${TELEGRAM_BOT_TOKEN:-}"
telegram_chat_id="${TELEGRAM_CHAT_ID:-}"

polling_interval="${POLLING_INTERVAL:-10}"
battery_difference="${BATTERY_DIFFERENCE:-20}"

smtp_server="${SMTP_SERVER:-smtp.example.com}"
smtp_port="${SMTP_PORT:-587}"
smtp_email="${SMTP_EMAIL:-}"
smtp_password="${SMTP_PASSWORD:-}"
smtp_receiver="${SMTP_TO:-}"
smtp_protocol="${SMTP_PROTOCOL:-tls}"

# NUT
echo "server = '$upshost'" > /app/webNUT/webnut/config.py
echo "port = '$upsport'" >> /app/webNUT/webnut/config.py
echo "username = '$upsuser'" >> /app/webNUT/webnut/config.py
echo "password = '$upspassword'" >> /app/webNUT/webnut/config.py

# Notifier
echo "polling_interval = '$polling_interval'" >> /app/webNUT/webnut/config.py
echo "battery_difference = '$battery_difference'" >> /app/webNUT/webnut/config.py

# Telegram
echo "telegram_bot_token = '$telegram'" >> /app/webNUT/webnut/config.py
echo "telegram_chat_id = '$telegram_chat_id'" >> /app/webNUT/webnut/config.py

# Email - SMTP
echo "smtp_server = '$smtp_server'" >> /app/webNUT/webnut/config.py
echo "smtp_port = '$smtp_port'" >> /app/webNUT/webnut/config.py
echo "smtp_email = '$smtp_email'" >> /app/webNUT/webnut/config.py
echo "smtp_password = '$smtp_password'" >> /app/webNUT/webnut/config.py
echo "smtp_receiver = '$smtp_receiver'" >> /app/webNUT/webnut/config.py
echo "smtp_protocol = '$smtp_protocol'" >> /app/webNUT/webnut/config.py

cat /app/webNUT/webnut/config.py

cd /app/webNUT && python setup.py install

cd webnut
exec pserve ../production.ini
