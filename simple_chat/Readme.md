SIMPLE CHAT USER GUIDE STEPS
1. create and activate python virtual environment in `simple_chat` folder with such a commands:
     * `python3 -m venv venv`
     * `source venv/bin/activate `
     * `pip install -r requirements.txt`
2. use file db.sqlite3 that already exists or load sqlite3 db with 
such a commands `sqlite3 db.sqlite3` -> `sqlite>.read chat_db_dump.txt` -> `sqlite>.dump `
3. `python manage.py runserver 8000`
4. admin http://127.0.0.1:8014/admin/ (admin tmp12345)
5. generate jwt token for resource access http://127.0.0.1:8000/api/token/
6. manage and execute API calls http://127.0.0.1:8000/swagger/



