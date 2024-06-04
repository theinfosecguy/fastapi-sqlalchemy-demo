## FastAPI SQLAlchemy Demo

This repository contains a basic example of integrating FastAPI with SQLAlchemy to create a robust and scalable web application. The project demonstrates essential features such as CRUD operations, dependency injection, database migrations with Alembic, and testing.

## Installation

1. **Clone the repository**:

   ```sh
   git clone https://github.com/theinfosecguy/fastapi-sqlalchemy-demo.git
   cd fastapi-sqlalchemy-demo
   ```

2. **Create and activate a virtual environment**:

```
python -m venv fastapi-env
source fastapi-env/bin/activate`
```

3. **Install dependencies:**
```
pip install -r requirements.txt
```

## Running the Application

1. **Start the FastAPI application:**
```
uvicorn main:app --reload
```
The application will be available at `http://127.0.0.1:8000`.

2. **Explore the API documentation:**
Open your browser and go to `http://127.0.0.1:8000/docs` to access the automatically generated Swagger UI documentation.
