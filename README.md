# 🐍 Python Challenge ML

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pytest](https://img.shields.io/badge/pytest-%23ffffff.svg?style=for-the-badge&logo=pytest&logoColor=2f9fe3)
![Streamlit](https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

> A comprehensive machine learning solution built with Python, featuring a modern backend API and interactive frontend visualization interface.

This project is a complete solution to the [Python Challenge by jfaldanam](https://github.com/jfaldanam/py_challenge), implementing a robust architecture with backend services, frontend visualization, and containerized deployment options.

## ✨ Features

- 🔥 **Modern Python Stack**: Built with FastAPI, Streamlit, and modern Python tooling
- 🐳 **Docker Support**: Full containerization with docker-compose
- 📊 **Interactive Visualizations**: Streamlit-powered frontend for data exploration
- 🔧 **Machine Learning Pipeline**: Complete ML workflow implementation
- 📦 **Package Management**: Modern dependency management with `uv`
- 🧪 **Testing Suite**: Comprehensive test coverage with pytest
- 🛡️ **Code Quality**: Linting and formatting with Ruff

## 📋 Table of Contents

- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
  - [Prerequisites](#prerequisites)
  - [Local Development](#local-development)
  - [Docker Deployment](#docker-deployment)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

## 📂 Project Structure

```
📁 python-challenge-ml-uv/
├── 📁 backend-python-challenge/
│   ├── 📁 src/
│   │   ├── 📁 api/
│   │   │   ├── 📁 controllers/
│   │   │   ├── 📁 models/
│   │   │   ├── 📁 routes/
│   │   │   ├── 📄 app.py
│   │   │   ├── 📄 main.py
│   │   │   └── 📄 utils.py
│   │   ├── 📁 clustering/
│   │   ├── 📁 config/
│   │   └── 📁 machine_learning/
│   ├── 📄 .env-template
│   ├── 📄 pyproject.toml
│   ├── 📄 requirements.txt
│   └── 📄 uv.lock
├── 📁 visualization/
│   ├── 📁 src/
│   │   └── 📁 visualization/
│   ├── 📄 .env-template
│   ├── 📄 pyproject.toml
│   ├── 📄 requirements.txt
│   └── 📄 uv.lock
├── 📄 .gitignore
├── 📄 LICENSE
└── 📄 README.md
```

## 🚀 Quick Start

Get up and running in minutes with Docker:

```bash
# Clone the repository with submodules
git clone --recurse-submodules <your-repo-url>
cd python-challenge-ml-uv

# Start all services
docker-compose up --build
```

Access the application:
- 🌐 **Frontend**: http://localhost:8501
- 🔧 **API**: http://localhost:8000
- 📦 **MinIO Console**: http://localhost:9001

## 📦 Installation

### Prerequisites

- Python 3.8+
- Docker & Docker Compose (for containerized deployment)
- Git

### Local Development

> [!IMPORTANT]
> This repository uses git submodules. Clone with `--recurse-submodules` or run `git submodule update --init --recursive` after cloning.

#### 1. Set up the Data Service

Initialize the `data-service` following its [README instructions](https://github.com/jfaldanam/py_challenge/blob/master/data-service/README.md).

#### 2. Start MinIO (if not using Docker)

```bash
docker run -d \
  -p 9000:9000 -p 9001:9001 \
  -e MINIO_ROOT_USER=minioadmin \
  -e MINIO_ROOT_PASSWORD=minioadmin \
  -v minio_data:/data \
  minio/minio server /data --console-address ":9001"
```

#### 3. Backend Setup

```bash
cd backend-python-challenge

# Copy and configure environment
cp .env-template .env
# Edit .env with your settings

# With uv (recommended)
uv run src/api/main.py

# Or with traditional venv
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/api/main.py
```

#### 4. Frontend Setup

```bash
cd visualization

# Copy and configure environment
cp .env-template .env
# Edit .env with your settings

# With uv (recommended)
uv run streamlit run src/visualization/app.py

# Or with traditional venv
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run src/visualization/app.py
```

### Docker Deployment

The easiest way to run the entire stack:

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop services
docker-compose down
```

**Services Overview:**
- `backend`: FastAPI application (port 8000)
- `frontend`: Streamlit visualization app (port 8501)
- `minio`: S3-compatible object storage (ports 9000, 9001)
- `data_service`: Synthetic data generation service (port 8777)

## ⚙️ Configuration

### Backend Configuration

Edit `backend-python-challenge/.env`:

```bash
# MinIO Configuration
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
MINIO_ENDPOINT=minio:9000  # Use localhost:9000 for local development

# API Configuration
HOST=0.0.0.0
PORT=8000

# Data Service
DATA_SERVICE_URL=http://data_service:8777/  # Use http://localhost:8777/ for local
```

### Frontend Configuration

Edit `visualization/.env`:

```bash
# API Endpoint
API_BASE=http://backend:8000  # Use http://localhost:8000 for local development
```

## 🎯 Usage

1. **Access the Web Interface**: Navigate to http://localhost:8501
2. **Explore the API**: Visit http://localhost:8000/docs for interactive API documentation
3. **Monitor Storage**: Access MinIO console at http://localhost:9001


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Christian Berdejo**
- LinkedIn: [Christian Berdejo](https://www.linkedin.com/in/christian-berdejo-63073728b/?locale=en_US)
- Based on the original challenge by [jfaldanam](https://github.com/jfaldanam/py_challenge)
