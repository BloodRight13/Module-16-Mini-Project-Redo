# E-commerce API

This is a basic e-commerce API built using Flask and PostgreSQL. It allows you to manage items in a database.

## Setup

1.  **Create a PostgreSQL database on Render.**
2.  **Set up environment variables:**
    *   `RENDER_DB_HOST`: The host of your PostgreSQL database on Render
    *   `RENDER_DB_NAME`: The database name
    *   `RENDER_DB_USER`: The database username
    *   `RENDER_DB_PASSWORD`: The database password
    *    `RENDER_DB_PORT`: The database Port
3.  **Clone the repository:**

    ```bash
    git clone <YOUR_GITHUB_REPO_URL>
    ```
4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Run the application locally:**
    ```bash
      python run.py
    ```
6.  **Run Tests**

    ```bash
      python -m unittest discover -s app/tests -p "test_*.py"
    ```

## API Endpoints

*   `GET /items`: Get all items.
*   `POST /items`: Create a new item.
*   `GET /items/<item_id>`: Get an item by ID.
*   `PUT /items/<item_id>`: Update an item by ID.
*   `DELETE /items/<item_id>`: Delete an item by ID.

## Swagger Documentation

You can access the Swagger UI at the `/swagger` endpoint of the deployed application.
Swagger Documentation Link [Swagger UI](your_deployed_url/swagger)

## GitHub Repository

[Link to the GitHub repository](YOUR_GITHUB_REPO_URL)