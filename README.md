1)  Для запуска кода создать виртуальную среду:
    python -m venv .venv (python3 for linux)

2)  Скачать все зависимости:
    pip install -r requirements.txt

3)  Запустить веб сервер:
    uvicorn main:app --reload
    или
    Если есть функция main в main то можно просто:
    python main.py
    
4)  Периодически обновлять список зависимостей:
    pip freeze > requirements.txt


