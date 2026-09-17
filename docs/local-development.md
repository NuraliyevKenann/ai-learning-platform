# Local development

To start the project locally on Windows, run one command from the project root:

```powershell
.\scripts\start-dev.ps1
```

The script starts Docker Desktop if needed, starts PostgreSQL with Docker Compose,
and opens separate PowerShell windows for the backend and frontend.

Open the site at:

```text
http://127.0.0.1:5173/
```

Useful backend links:

```text
http://127.0.0.1:8000/api/v1/health
http://127.0.0.1:8000/docs
```

To stop only PostgreSQL:

```powershell
.\scripts\stop-dev.ps1
```

Close the backend and frontend PowerShell windows manually when you finish working.
