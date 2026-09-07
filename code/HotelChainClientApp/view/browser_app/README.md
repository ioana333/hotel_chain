# Browser app

Interfata web este separata de aplicatia desktop si nu modifica restul proiectului.

Porneste mai intai microserviciile:

```powershell
cd D:\FACULTATE\AN 3\SEM II\PS\PROIECT\WORK\app\HotelChainFinalPython\HotelChainMicroservices
..\.venv\Scripts\python.exe -m database.seed_sqlite
..\.venv\Scripts\python.exe .\run_all_services.py
```

Intr-un al doilea terminal porneste interfata browser:

```powershell
cd D:\FACULTATE\AN 3\SEM II\PS\PROIECT\WORK\app\HotelChainFinalPython\HotelChainClientApp\view\browser_app
..\..\..\.venv\Scripts\python.exe .\run_browser_app.py
```

Deschide:

```text
http://127.0.0.1:5500
```

Serverul local serveste fisierele statice si trimite cererile `/api/...` catre API Gateway-ul existent de pe `http://127.0.0.1:8000`.
