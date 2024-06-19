# Stock Market API Service

## Description

This service exposes endpoints for user registration, login, and obtaining stock market information.

## Deployment on 
https://eurekastockmarket-production.up.railway.app/


## EXCECUTION in local
install python 

**Run the following commands:**
- pip install -r requirements.txt
- python manage.py runserver


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
  - `limit`: Indicates the amount of the las measures you want to see (optional, default 1)

**TIME_SERIES_INTRADAY**
    **Mandatory:**
    - `symbol`: Stock market symbol
    - `function`: Alpha Vantage API function
    - `interval`:   ['1min', '5min', '15min', '30min', '60min']

**TIME_SERIES_DAILY, TIME_SERIES_DAILY, TIME_SERIES_DAILY_ADJUSTED, TIME_SERIES_WEEKLY, TIME_SERIES_WEEKLY_ADJUSTED, TIME_SERIES_MONTHLY, TIME_SERIES_MONTHLY_ADJUSTED**
    **Mandatory:**
    - `symbol`: Stock market symbol
    - `function`: Alpha Vantage API function


*Optional to implement datatype as csv*



**Deployment**
    -The deployment was done on Railway because it is free, unlike Heroku, AWS, etc., which are paid services. The database used is Postgres from Elephant as it is also free. The downside is the connection time, which adds latency to the response.

## Things to Improve:
    -The API key for Alpha Vantage is stored in the .env file, which can be hashed and stored in the database.
    -The project has the capability for extension, with each TIME type having its own instance. There is also a FunctionValidator to validate parameters and execute dynamically.
    -The datatype as CSV is not implemented but is planned.
    -The factory method and SOLID principles for Open/Closed were used.

## Contact

For more information, contact: <m.fragueiro.lazcano@gmail.com>