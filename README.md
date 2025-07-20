# E-commerce API

This is a simple e-commerce backend application built with FastAPI and MongoDB.

## Features

- Create and list products.
- Create and list orders.
- Filtering and pagination for product and order listings.

## Project Structure

- `app/`: Contains the main application logic.
  - `main.py`: The entry point of the FastAPI application.
  - `database.py`: Handles the MongoDB connection.
  - `models.py`: Defines the Pydantic data models.
  - `routers/`: Contains the API route definitions.
    - `products.py`: Routes for product-related operations.
    - `orders.py`: Routes for order-related operations.
- `.env`: Stores environment variables (e.g., MongoDB connection string).
- `requirements.txt`: Lists the Python dependencies.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/pswitchy/E-commerce-API.git
    cd e-commerce-api
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    Create a `.env` file in the root directory and add your MongoDB connection string:
    ```
    MONGO_DETAILS="your-mongodb-connection-string"
    ```

5.  **Run the application:**
    ```bash
    uvicorn app.main:app --reload
    ```
    The application will be running at `http://127.0.0.1:8000`.

## API Documentation

Once the application is running, you can access the interactive API documentation at `http://127.0.0.1:8000/docs`.
