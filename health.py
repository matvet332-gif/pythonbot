from flask import Flask
import threading
import time
import requests

app = Flask(__name__)

class HealthMonitor:
    def __init__(self):
        self.healthy = True
        self.start_monitoring()
    
    def start_monitoring(self):
        """Запуск мониторинга в отдельном потоке"""
        def monitor():
            while True:
                try:
                    # Проверяем доступность основных функций
                    self.healthy = self.check_health()
                except Exception as e:
                    self.healthy = False
                    print(f"Health check failed: {e}")
                
                time.sleep(300)  # Проверка каждые 5 минут
        
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
    
    def check_health(self):
        """Проверка здоровья приложения"""
        try:
            # Можно добавить дополнительные проверки
            return True
        except:
            return False

health_monitor = HealthMonitor()

@app.route('/health')
def health():
    """Endpoint для проверки здоровья"""
    if health_monitor.healthy:
        return 'OK', 200
    else:
        return 'Service Unavailable', 503

@app.route('/')
def index():
    return """
    <html>
        <head>
            <title>Python Learning Bot</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .status { padding: 10px; border-radius: 5px; }
                .healthy { background: #d4edda; color: #155724; }
            </style>
        </head>
        <body>
            <h1>🤖 Python Learning Bot</h1>
            <div class="status healthy">🚀 Status: Running</div>
            <p>Bot is deployed on Render and monitored by UptimeRobot</p>
            <p><a href="/health">Health Check</a></p>
        </body>
    </html>
    """
