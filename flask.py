from flask import Flask, request
from telegram import Update
from telegram.ext import Application, ContextTypes
import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Инициализация бота
BOT_TOKEN = os.getenv('BOT_TOKEN')
application = Application.builder().token(BOT_TOKEN).build()

# Импортируем обработчики
from bot import PythonLearningBot
bot_instance = PythonLearningBot()

@app.route('/')
def index():
    return "Python Learning Bot is running! 🚀"

@app.route('/webhook/' + BOT_TOKEN, methods=['POST'])
def webhook():
    """Webhook endpoint для Telegram"""
    update = Update.de_json(request.get_json(), application.bot)
    application.update_queue.put(update)
    return 'ok'

@app.route('/health')
def health_check():
    """Health check для UptimeRobot"""
    return 'OK', 200

def main():
    """Запуск приложения"""
    port = int(os.environ.get('PORT', 10000))
    
    # Устанавливаем webhook
    webhook_url = os.getenv('WEBHOOK_URL', '') + '/webhook/' + BOT_TOKEN
    application.bot.set_webhook(webhook_url)
    
    # Запускаем Flask
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    main()
