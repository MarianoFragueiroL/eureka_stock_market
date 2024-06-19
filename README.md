# Stock Market API Service

## Description

This service exposes endpoints for user registration, login, and obtaining stock market information.

## Endpoints

### User Sign Up

- **URL:** `/api/signup/`
- **Método:** `POST`
- **Data :**
    **Must:**
        - `username`: Nombre de usuario
        - `password`: password
    **Optional:**
        - `first_name`: Name
        - `last_name`: Last Name
        - `email`: email

### User Login
- **URL:** `/api/login/`
- **Método:** `POST`
- **Data :**
    - `username`: Nombre de usuario
    - `password`: password

### Get Stock Market Information

- **URL:** `/api/stock/`
- **Method:** `POST`
- **Headers:**
  - `API_KEY`: User's API key
- **Request Body:**
  - `symbol`: Stock market symbol
  - `function`: Alpha Vantage API function (optional, default `TIME_SERIES_DAILY_ADJUSTED`)
  - `interval`: Time interval (optional, default `daily`)
  - `time_period`: Time period (optional)
  - `series_type`: Series type (optional, default `close`)

## Deployment on Heroku

1. Clone the repository.
2. Create a `Procfile` with the following content:
    ```plaintext
    web: gunicorn stock_market_api.wsgi --log-file -
    ```
3. Create a `requirements.txt` with the project dependencies:
    ```bash
    pip freeze > requirements.txt
    ```
4. Add the Heroku configuration in `settings.py` as explained above.
5. Log in to Heroku:
    ```bash
    heroku login
    ```
6. Create a new application on Heroku:
    ```bash
    heroku create your-app-name
    ```
7. Set up PostgreSQL on Heroku:
    ```bash
    heroku addons:create heroku-postgresql:hobby-dev
    ```
8. Configure environment variables on Heroku:
    ```bash
    heroku config:set DJANGO_SETTINGS_MODULE=stock_market_api.settings
    heroku config:set ALPHA_APIKEY=your_alpha_vantage_api_key
    ```
9. Push the code to Heroku:
    ```bash
    git add .
    git commit -m "Deploy to Heroku"
    git push heroku master
    ```
10. Run migrations on Heroku:
    ```bash
    heroku run python manage.py migrate
    ```
11. Open the application on Heroku:
    ```bash
    heroku open
    ```

## Contact

For more information, contact: <m.fragueiro.lazcano@gmail.com>