# Inventory Management API

A Python Flask-based Inventory Management API designed to help manage inventory records, perform inventory operations, and integrate with external APIs. The project uses SQLite for data storage and includes a command-line interface (CLI) and automated tests.

## Features

* **Inventory Management:** Manage inventory records through API endpoints.
* **SQLite Database:** Store inventory data in a local database.
* **REST API:** Handle client requests using Flask routes and HTTP methods.
* **Command-Line Interface:** Interact with supported application features through the terminal.
* **External API Integration:** Connect with an external API for additional functionality.
* **Automated Testing:** Test inventory operations and external API functionality using pytest.

## Technologies Used

* Python 3
* Flask
* SQLite
* pytest
* Requests (if used by the external API integration)
* Git and GitHub

## Project Structure

```text
inventory-management-api/
├── app.py
├── cli.py
├── inventory.db
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_inventory.py
│   └── test_external_api.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

Ensure that you have the following installed:

* Python 3
* pip
* Git

### 1. Clone the repository

```bash
git clone https://github.com/mils2001/inventory-management-api.git
```

Navigate into the project directory:

```bash
cd inventory-management-api
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it on Linux or macOS:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

Start the Flask application using:

```bash
python3 app.py
```

Check the terminal output for the local address where the server is running.

## Running Tests

Run the automated test suite with:

```bash
pytest -q
```

Alternatively:

```bash
python3 -m pytest -q
```

The tests cover inventory functionality and external API integration.

## Command-Line Interface

The project includes a CLI in `cli.py`.

Run:

```bash
python3 cli.py
```

Follow the available terminal prompts to use the supported CLI features.

## Database

The application uses SQLite for local data persistence. The database file is named `inventory.db`.

SQLite is lightweight and does not require a separate database server, making it suitable for development and testing.

## Development Workflow

The project uses Git for version control and GitHub for collaboration.

The development branch is:

```text
feature/flask-api
```

To retrieve the latest changes:

```bash
git pull origin feature/flask-api
```

To run tests before committing:

```bash
pytest -q
```

## Future Improvements

Potential enhancements include:

* Add inventory search, filtering, and sorting.
* Implement stock quantity updates and low-stock alerts.
* Add input validation and consistent error handling.
* Introduce user authentication and role-based permissions.
* Add pagination for large inventory collections.
* Improve API documentation with Swagger or OpenAPI.
* Add Docker support and continuous integration.
* Expand automated tests for edge cases and invalid requests.

## Contributing

1. Fork the repository or create a feature branch.
2. Make your changes.
3. Add or update tests.
4. Run the test suite.
5. Commit your changes with a descriptive message.
6. Open a pull request for review.

## License

A license has not yet been specified. Add a license file if you intend to distribute or allow others to reuse this project.

## Author

**Christian David Wafula**

GitHub: [@mils2001](https://github.com/mils2001)
