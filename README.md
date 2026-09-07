# HotelChain

A management application for a hotel chain, built as a university project (Software Engineering). The system is organized as a microservices architecture in Python (FastAPI), with two types of client interface: a desktop app and a web app.

Main features: searching and filtering hotels/rooms, reservations, reviews (only for rooms you've booked), CRUD for rooms/users/clients, statistics (with charts via matplotlib), data export (CSV/JSON/XML/DOC), and notifications when login credentials change.

## Requirements

- Python 3.11 or newer
- pip

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/ioana333/hotel_chain.git
cd hotel_chain
```

**2. Create and activate a virtual environment**

```bash
python -m venv .venv
```

Windows:
```powershell
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

**3. Install the dependencies**

```bash
pip install -r code/requirements.txt
```

## Running the project

**Step 1 — initialize the databases with demo data**

```bash
cd code/HotelChainMicroservices
python -m database.seed_sqlite
```

Warning: this command drops and recreates all the tables, so run it once at the start (or any time you want to reset the data back to the demo state).

**Step 2 — start all the microservices**

Still inside `code/HotelChainMicroservices`:

```bash
python run_all_services.py
```

This starts the API Gateway on port `8000` and the 6 microservices on ports `8001`–`8006`. Each one has interactive docs at `http://127.0.0.1:<port>/docs`. Stop everything with `CTRL+C`.

**Step 3 — start a client (in a new terminal, with the virtual environment activated)**

Option A — desktop app:

```bash
cd code/HotelChainClientApp
python app.py
```

Option B — web app:

```bash
cd code/HotelChainClientApp/view/browser_app
python run_browser_app.py
```

then open `http://127.0.0.1:5500` in your browser.

## Demo accounts

Created automatically by `seed_sqlite`:

| Role | Username | Password |
|---|---|---|
| Client | `client` | `client` |
| Employee | `angajat` | `angajat` |
| Manager | `manager` | `manager` |
| Administrator | `admin` | `admin` |
