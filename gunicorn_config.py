# Конфигурация Gunicorn
bind = "127.0.0.1:8000"  # Интерфейс и порт
workers = 2             # Количество воркеров
# worker_class = "sync"   # Класс воркеров (по умолчанию)
timeout = 30            # Максимальное время выполнения запроса (сек)
accesslog = "./logs/access.log"  # Лог доступа
errorlog = "./logs/error.log"    # Лог ошибок
loglevel = "info"       # Уровень логирования (info, debug, warning)