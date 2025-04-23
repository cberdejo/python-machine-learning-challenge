![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pytest](https://img.shields.io/badge/pytest-%23ffffff.svg?style=for-the-badge&logo=pytest&logoColor=2f9fe3)
![Streamlit](https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

# 🐍 python-challenge-ml

Repositorio con la resolución del [Python Challenge de jfaldanam](https://github.com/jfaldanam/py_challenge).  
Este proyecto incluye una arquitectura dividida en backend y frontend, con soporte para desarrollo local y contenedores Docker.

---

## 📁 Estructura del proyecto 
```
python-challenge-ml-uv
├─ 📁backend-python-challenge
│  ├─ 📁tests
│  ├─ 📁src
│  │  ├─ 📁api
│  │  │  ├─ 📁controllers
│  │  │  │  ├─ 📄animals_controller.py
│  │  │  │  ├─ 📄get_all_models_controller.py
│  │  │  │  ├─ 📄predict_controller.py
│  │  │  │  ├─ 📄train_controller.py
│  │  │  │  ├─ 📄validate_controller.py
│  │  │  ├─ 📁models
│  │  │  │  ├─ 📄animal_data.py
│  │  │  │  ├─ 📄generic_response.py
│  │  │  │  ├─ 📄synthetic_data.py
│  │  │  ├─ 📁routes
│  │  │  │  ├─ 📄animals_routes.py
│  │  │  │  ├─ 📄machine_learning_routes.py
│  │  │  ├─ 📄app.py
│  │  │  ├─ 📄main.py
│  │  │  ├─ 📄utils.py
│  │  ├─ 📁clustering
│  │  │  └─ 📄cluster_data.py
│  │  ├─ 📁config
│  │  │  ├─ 📄logger_config.py
│  │  │  ├─ 📄minio_config.py
│  │  └─ 📁machine_learning
│  │     ├─ 📁models
│  │     │  ├─ 📄analysis_result.py
│  │     ├─ 📄classify.py
│  │     ├─ 📄machine_learning_functions.py
│  │     ├─ 📄predict.py
│  │     ├─ 📄validate.py
│  ├─ 📄.env-template
│  ├─ 📄.python-version
│  ├─ 📄pyproject.toml
│  ├─ 📄requirements-dev.txt
│  ├─ 📄requirements.txt
│  └─ 📄uv.lock
├─ 📁visualizattion
├─ 📄.gitignore
├─ 📄LICENSE
└─ 📄README.md
```

---




## 🐳 Uso con Docker

### Levantar el proyecto

```bash
docker-compose up --build
```

Esto iniciará los servicios del backend y frontend.  
Podés configurar los puertos y volúmenes en `docker-compose.yml`.

---


## 🧪 Testing

Los tests están en `backend/tests/` y usan `pytest`.

```bash
pytest
```

Podés agregar tests unitarios y de integración según sea necesario.

---

## 🧠 Autor

Desarrollado por [Christian Berdejo](https://www.linkedin.com/in/christian-berdejo-63073728b/?locale=en_US)

Basado en el challenge original de [jfaldanam](https://github.com/jfaldanam/py_challenge)

---

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.

