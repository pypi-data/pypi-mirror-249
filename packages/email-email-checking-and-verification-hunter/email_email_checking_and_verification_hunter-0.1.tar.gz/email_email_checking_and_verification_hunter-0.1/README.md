**Задание:**
Выберете любой сервис и сделайте для него клиент, 2-3 ендпоинта будет достаточно + добавить сервис, который принимает 
какие-то значения и сохраняет результаты, сохранять можно просто в локальную переменную.

Как пример:
https://hunter.io/api-documentation/v2
Реализовать в клиенте отправку запроса на проверку и верификацию е-мейла.
И добавить сервис проверки е-мейла + CRUD для результатов, для хранилища можно использовать переменную. Выложить на 
github, оформить пакетом.

Типизация обязательна.
Пользоваться вот этим линтером: https://github.com/wemake-services/wemake-python-styleguide
setup.cfg https://gist.github.com/dfirst/0957711a40d640d335e128eec4c17f21

**Решение:**

1. Структура проекта:
```bash
email_email_checking_and_verification_hunter/   # Основна папка проекту.
│
├── config.py                         
├── hunter_client.py
├── local_storage_service.py
├── logger.py
├── main.py
├── menu.py
├── README.md
├── request_manager.py
├── requirements.txt
├── setup.py
├── utils.py
```