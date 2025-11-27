import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from python_console import PythonConsole
from security import SecurityManager

class WebhookPythonBot:
    def __init__(self):
        self.token = os.getenv('BOT_TOKEN')
        self.webhook_url = os.getenv('WEBHOOK_URL')
        self.port = int(os.getenv('PORT', 10000))
        
        if not self.token:
            raise ValueError("BOT_TOKEN не установлен!")
            
        self.application = Application.builder().token(self.token).build()
        self.consoles = {}
        self.security = SecurityManager()
        
        self.setup_handlers()
        
    def setup_handlers(self):
        """Настройка обработчиков"""
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("console", self.open_console))
        self.application.add_handler(CommandHandler("lessons", self.show_lessons))
        self.application.add_handler(CommandHandler("security", self.security_info))
        self.application.add_handler(CallbackQueryHandler(self.button_handler))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user = update.effective_user
        welcome_text = f"""
🤖 Привет, {user.first_name}!

Добро пожаловать в бот для изучения Python!

Возможности:
💻 /console - Интерактивная Python консоль
📚 /lessons - Уроки по Python
🛡️ /security - Информация о безопасности

Бот работает на Render + UptimeRobot 🚀
        """
        await update.message.reply_text(welcome_text)

    # ... остальные методы такие же как в оригинальном bot.py ...

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка ввода кода"""
        user_id = update.effective_user.id
        code = update.message.text

        # Проверка безопасности
        quick_check = self.security.sanitize_input(code)
        if not quick_check["is_safe"]:
            error_msg = "❌ **Обнаружены проблемы с безопасностью:**\n" + "\n".join(quick_check["issues"][:3])
            await update.message.reply_text(error_msg, parse_mode='Markdown')
            return

        if user_id not in self.consoles:
            self.consoles[user_id] = PythonConsole()

        try:
            result = self.consoles[user_id].execute(code)
            
            if result.startswith(('❌', '⏰', '💥')):
                response = result
            else:
                response = f"```python\n>>> {code}\n{result}\n```"
            
            await update.message.reply_text(response, parse_mode='MarkdownV2')
            
        except Exception as e:
            error_msg = f"❌ Системная ошибка:\n```\n{str(e)}\n```"
            await update.message.reply_text(error_msg, parse_mode='MarkdownV2')

    def run_webhook(self):
        """Запуск в режиме webhook"""
        self.application.run_webhook(
            listen="0.0.0.0",
            port=self.port,
            url_path=self.token,
            webhook_url=f"{self.webhook_url}/{self.token}"
        )

    def run_polling(self):
        """Запуск в режиме polling (для разработки)"""
        self.application.run_polling()
