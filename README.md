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

## Deployment on 
https://eurekastockmarket-production.up.railway.app/

## Contact

For more information, contact: <m.fragueiro.lazcano@gmail.com>