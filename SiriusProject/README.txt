Бот сейчас работает на сервере timeweb.
Задание на второй этап в директории video_summary_api
Как временное решение, функции генерации текста заменяет openai API gpt-4o, используемый через сервис ProxyAPI. В будущем будет заменён на обученные нами модели.
Для запуска api из директории video_summary_api:
uvicorn video_summary:app --reload
Для запуска бота из директории SmartNoteTG:
python run.py
