# AIweb Frontend (React + Vite)

Pages included:
- Login
- Register
- Credits Dashboard

## Run locally
```powershell
cd frontend
npm install
npm run dev
```

## API configuration
By default the frontend uses the real backend base URL `http://127.0.0.1:8000`.

- Enable mock API: set `VITE_MOCK_API=1`
- Use real backend: set `VITE_API_BASE_URL=http://127.0.0.1:8000`

Example:
```powershell
$env:VITE_API_BASE_URL = "http://127.0.0.1:8000"
$env:VITE_MOCK_API = "0"
npm run dev
```
