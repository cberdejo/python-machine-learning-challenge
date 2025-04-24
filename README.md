[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pytest](https://img.shields.io/badge/pytest-%23ffffff.svg?style=for-the-badge&logo=pytest&logoColor=2f9fe3)
![Streamlit](https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

🐍 python-challenge-mlpython-challenge-ml

Solution to the [Python Challenge by jfaldanam](https://github.com/jfaldanam/py_challenge).  
This project includes a backend and frontend architecture with support for local development and Docker containers.

---

## Table of Contents

- [Project Structure](#project-structure)
- [Running the Project](#running-the-project)
  - [Before You Start](#before-you-start)
  - [Local Setup](#local-setup)
  - [Docker Setup](#docker-setup)
- [Testing](#testing)
- [Author](#author)
- [License](#license)

---
## 📂 Project Structure

```
📁 python-challenge-ml-uv
├─ 📁 backend-python-challenge
│  ├─ 📁 src
│  │  ├─ 📁 api
│  │  │  ├─ 📁 controllers
│  │  │  ├─ 📁 models
│  │  │  ├─ 📁 routes
│  │  │  ├─ 📄 app.py
│  │  │  ├─ 📄 main.py
│  │  │  ├─ 📄 utils.py
│  │  ├─ 📁 clustering
│  │  ├─ 📁 config
│  │  └─ 📁 machine_learning
│  ├─ 📄 .env-template
│  ├─ 📄 pyproject.toml
│  ├─ 📄 requirements.txt
│  └─ 📄 uv.lock
├─ 📁 visualization
│  ├─ 📁 src
│  │  ├─ 📁 visualization
│  ├─ 📄 .env-template
│  ├─ 📄 pyproject.toml
│  ├─ 📄 requirements.txt
│  └─ 📄 uv.lock
├─ 📄 .gitignore
├─ 📄 LICENSE
└─ 📄 README.md
```

---

## 🚀 Running the Project

### 🛠️ Before You Start

Copy the `.env-template` file to `.env` and complete the necessary environment variables.

#### backend-python-challenge

```bash
cp backend-python-challenge/.env-template backend-python-challenge/.env
```

Example of environment variables:

```bash
MINIO_ROOT_USER=minioadmin 
MINIO_ROOT_PASSWORD=minioadmin
MINIO_ENDPOINT=minio:9000
# For local development:
# MINIO_ENDPOINT=localhost:9000

HOST=0.0.0.0
PORT=8000

DATA_SERVICE_URL=http://data_service:8777/api/v1/animals/data
# For local development:
# DATA_SERVICE_URL=http://localhost:8777/api/v1/animals/data
```

#### visualization

```bash
cp visualization/.env-template visualization/.env
```

Example of environment variables:

```bash
# For Docker:
API_BASE=http://backend:8000

# For local development:
# API_BASE=http://localhost:8000
```
---
Clone the [data-service repository](https://github.com/jfaldanam/py_challenge) which provides the simulated data API:

```bash
git clone https://github.com/jfaldanam/py_challenge.git
```

---

### Local Setup

If you prefer not to use Docker, follow these steps to run the project locally:

1. Initialize `data-service` following its [README instructions](https://github.com/jfaldanam/py_challenge/blob/master/data-service/README.md).

2. If you dont have currently a MinIO instance, you can start a local MinIO instance with Docker:

```bash
docker run -p 9000:9000 -p 9001:9001 -e MINIO_ROOT_USER=minioadmin -e MINIO_ROOT_PASSWORD=minioadmin -v minio_data:/data minio/minio server /data --console-address ":9001"
```

MinIO will be available at:
- http://localhost:9000 (API)
- http://localhost:9001 (Web Console)

3. Run the backend:

```bash
cd backend-python-challenge
```

With `uv`:

```bash
uv run src/api/main.py
```

Without `uv`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/api/main.py
```

4. Run the frontend (Streamlit):

```bash
cd visualization
```

With `uv`:

```bash
uv run streamlit run src/visualization/app.py
```

Without `uv`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run src/visualization/app.py
```

---

### Docker Setup

To build and run the project with Docker:

```bash
docker-compose up --build
```

This will start the following services:
- backend: Main API (port 8000)
- frontend: Streamlit app (port 8501)
- minio: Local S3 storage (ports 9000, 9001)
- data_service: Microservice to generate synthetic data (port 8777)

You can modify the ports in `docker-compose.yml`.

---

## 🧪 Testing


Tests are located in `backend/tests/` and use `pytest`.

```bash
pytest
```

---

## 👨‍💻 Author

Developed by [Christian Berdejo](https://www.linkedin.com/in/christian-berdejo-63073728b/?locale=en_US)  
Based on the original challenge by [jfaldanam](https://github.com/jfaldanam/py_challenge)

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
