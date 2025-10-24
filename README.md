### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # On Windows
venv/bin/activate #on macOS/Linux
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Notes

Configure environment variables in .env (database, API keys, etc.)

