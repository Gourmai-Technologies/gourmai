# Gourmai

 ![version](https://img.shields.io/badge/version-0.9.0-blue.svg)

<br />

> Features:

- ✅ `Up-to-date dependencies`
- ✅ Database: `SQLite`
- ✅ `DB Tools`: SQLAlchemy ORM, Flask-Migrate (schema migrations)
- ✅ Session-Based authentication (via **flask_login**), Forms validation
- ✅ `Docker`
- ✅ CI/CD via `Render`

<br />

## Table of Contents

* [Docker Support](#docker-support)
* [Quick Start](#quick-start)
* [Documentation](#documentation)
* [File Structure](#file-structure)
* [Browser Support](#browser-support)
* [Resources](#resources)
* [Reporting Issues](#reporting-issues)
* [Technical Support or Questions](#technical-support-or-questions)
* [Licensing](#licensing)
* [Useful Links](#useful-links)

<br />

## Docker Support

> 👉 **Step 1** - Get the code

```bash
$ git clone https://github.com/gourmai/gourmai.git
$ cd gourmai
```

> 👉 **Step 2** - Start the APP in `Docker`

```bash
$ docker-compose up --build 
```

Visit `http://localhost:5085` in your browser. The app should be up & running.

<br />

## Manual Build 

> 👉 **Step 1** - Get the code

```bash
$ # Get the code
$ git clone https://github.com/gourmai/gourmai.git
$ cd gourmai
$
$ # Virtualenv modules installation (Unix based systems)
$ python -m venv .venv
$ source .venv/bin/activate
$
$ # Virtualenv modules installation (Windows based systems)
$ # virtualenv env
$ # .\env\Scripts\activate
$
$ # Install modules
$ pip3 install -r requirements.txt
$
$ # Set the FLASK_APP environment variable
$ (Unix/Mac) export FLASK_APP=run.py
$ (Windows) set FLASK_APP=run.py
$ (Powershell) $env:FLASK_APP = ".\run.py"
$
$ # Set up the DEBUG environment
$ # (Unix/Mac) export FLASK_ENV=development
$ # (Windows) set FLASK_ENV=development
$ # (Powershell) $env:FLASK_ENV = "development"
$
$ # Start the application (development mode)
$ # --host=0.0.0.0 - expose the app on all network interfaces (default 127.0.0.1)
$ # --port=5000    - specify the app port (default 5000)  
$ flask run --host=0.0.0.0 --port=5000
$
$ # Access the dashboard in browser: http://127.0.0.1:5000/
```

> Note: To use the app, please access the registration page and create a new user. After authentication, the app will unlock the private pages.

<br />

## Documentation

The documentation for the **Material Dashboard Flask** is hosted at our [website](https://demos.creative-tim.com/material-dashboard-flask/docs/1.0/getting-started/getting-started-flask.html).

<br />

## Licensing

- Copyright 2024 - present [Gourmai](https://www.gourmai.co.uk/)

<br />

## Useful Links

- [More products](https://www.creative-tim.com/bootstrap-themes) from Creative Tim
- [Tutorials](https://www.youtube.com/channel/UCVyTG4sCw-rOvB9oHkzZD1w)
- [Freebies](https://www.creative-tim.com/bootstrap-themes/free) from Creative Tim
- [Affiliate Program](https://www.creative-tim.com/affiliates/new) (earn money)

<br />

---
[Material Dashboard Flask](https://www.creative-tim.com/product/material-dashboard-flask) - Provided by [Creative Tim](https://www.creative-tim.com/) and [AppSeed](https://appseed.us)
