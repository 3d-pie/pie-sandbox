# Sandbox Scaffold



## 1 · Quick Start (Local)

```bash
# 1. Clone the repo
git clone https://github.com/3d-pie/pie-sandbox.git
cd your-sandbox/sandbox

# 2. Create & activate a fresh virtual environment (Python 3.12)
python3 -m venv .venv
source .venv/bin/activate # Linux    
# .venv\Scripts\activate # Windows 

# 3. Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Run the app
python -m app                     # http://localhost:5000
```

Tip: The first boot auto-creates `instance/sandbox.db` and the uploads/
directory (if missing). No additional setup required.


Follow the instructions in the challenge description to extend this scaffold.


## 2 · Running with Docker (optional)

Docker keeps your local environment clean and guarantees “it-works-on-my-machine” parity. 
[Get Started with Docker](https://www.docker.com/get-started/)

### 2.1 Build & Run


```bash
docker compose up --build        # first time or after deps change
# OR
docker compose up                # subsequent boots
```

Container exposes `http://localhost:5000`

Source code and `uploads/` are volume-mounted, so live-reloading works.


### 2.2 Why Docker?

- Isolation – no global Python packages or conflicting versions

- Parity – the deploy VM runs the exact same image

- One-liner spin-up – avoids local Python or venv hassles for the deploy VM

## 3. Project Structure

```
sandbox/
├─ app/                   # Flask application package
│  ├─ __init__.py         # Application factory and configuration
│  ├─ __main__.py         # Entry point for `python -m app`
│  ├─ models.py           # SQLAlchemy models (User, Item)
│  ├─ routes.py           # HTTP routes and view functions
│  ├─ services.py         # Stubs for parsing and rendering
│  └─ templates/          # Jinja2 HTML templates
│      ├─ base.html
│      ├─ login.html
│      ├─ rbac_demo.html
│      ├─ gcode_upload.html
│      └─ items_list.html
├─ uploads/               # File uploads are stored here (empty by default)
├─ migrations/            # Alembic environment and baseline migration
│  ├─ env.py
│  └─ versions/
│      └─ 0001_initial.py
├─ Dockerfile             # Build instructions for containerising the app
├─ docker-compose.yml     # Compose file to run the container with mounted volumes
├─ requirements.txt       # Python dependencies
└─ README.md              # This file
```

## 4 · Next Steps

- RBAC migration – replace legacy boolean flags with **Role/Permission** tables.

- G-Code parser – implement `services.gcode_parser()`.

- Thumbnail renderer – implement `services.thumbnail_render()`.

Check the separate Challenges document for full details. Happy hacking!




