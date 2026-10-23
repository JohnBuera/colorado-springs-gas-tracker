# Colorado Springs Gas Tracker

A gas-price dashboard made with FastAPI, SQLite / SQLAlchemy, and React + TypeScript.

## What works so far

- Compare demo station prices for Regular, MidGrade, Premium, and Diesel.
- View the lowest and average price for each fuel type.
- Search, sort, and save example stations.
- Use a calculator to compare the price difference on a fill-up.
- Run the Python maze simulation and fuel-cost optimizer.
- Run automatic backend tests.

**Important:** The current station names, addresses, and prices are examples. They are NOT live gas prices. The maze optimizer is a simulation, not real-road navigation.

## Start the backend

From the main project folder, use Python 3.11 or newer:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn backend.main:app --reload
```

Backend: http://127.0.0.1:8000
API documentation: http://127.0.0.1:8000/docs

## Start the frontend

Open a second terminal in the main project folder:

```bash
cd frontend
npm install
npm run dev
```

Then open http://localhost:5173.

To use a different API address, copy `frontend/.env.example` to `frontend/.env` and change `VITE_API_BASE_URL`.

## Test the project

```bash
python -m pytest -q
cd frontend
npm run build
```

## What still needs to be done before a public release

- Add a real, authorized gas-price data source with update timestamps.
- Replace the placeholder stations with real gas stations and locations.
- Use actual travel routes and distances before claiming net fuel savings.
- Host the backend and frontend, and configure production database/CORS.
