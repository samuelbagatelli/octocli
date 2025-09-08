<a id="readme-top"></a>



<!-- PROJECT LOGO -->
<br />
<div align="center">
    <a href="https://pypi.org/project/octocli/">
        <img src="img/logo.png" alt="Logo" width="80" height="80" />
    </a>
    <h3 align="center">OCTO CLI</h3>
    <p align="center">
        Command Line Interface to manage FastAPI projects.
        <br />
        <a href="https://github.com/samuelbagatelli/octocli/tree/main"><strong>Explore the docs »</strong></a>
        <br />
        <br />
        <a href="https://pypi.org/project/octocli/">View Demo</a>
        &middot;
        <a href="https://github.com/samuelbagatelli/octocli/issues">Report Bug</a>
    </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
    <summary>Table of Contents</summary>
    <ol>
        <li>
            <a href="#about-the-project">About The Project</a>
            <ul>
                <li><a href="#build-with">Built With</a></li>
                <li><a href="#description">Description</a></li>
            </ul>
        </li>
        <li>
            <a href="#getting-started">Getting Started</a>
            <ul>
                <li><a href="#prerequisites">Prerequisites</a></li>
                <li><a href="#installation">Installation</a></li>
            </ul>
        </li>
        <li>
            <a href="#usage">Usage</a>
        </li>
        <li>
            <a href="#roadmap">Roadmap</a>
        </li>
        <li>
            <a href="#contributing">Contributing</a>
        </li>
        <li>
            <a href="#license">License</a>
        </li>
    </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![octocli example][product-screenshot]

The OCTO CLI is made to manage a FastAPI advanced projetc, following the patterns used on CPID.

Default folder structure:
```
project/
├── app/
│   ├── main.py
│   ├── models/
│   │   └── model.py
│   ├── prefix/
│   │   └── prefix_base.py
│   ├── routers/
│   │   └── route.py
│   ├── schemas/
│   │   └── schema.py
│   └── settings/
│       ├── .env
│       ├── config.py
│       └── database.py
├── requirements.txt
└── README.md
```

The models use the SQLAlchemy ORM declarative mapping version of representation. Where the `prefix/prefix_base.py` contains a version of the

```python
class Base(DeclarativeBase):
    pass
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Description

<!-- TODO: Insert a description of the project -->
The Beija-Flor project is a...

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![FastAPI][fastapi]][fastapi-url]
* [![Pydantic][pydantic]][pydantic-url]
* [![SQLAlchemy][sqlalchemy]][sqlalchemy-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Some instructions to get the API up and running.
This will get the API running on your local environment.

### Prerequisites

The only prerequisite is Python 3.8+ installed. Most of linux distros come with python pre-installed (WSL included).

For Windows users: **No support on documentation yet.**

### Installation

1. Clone the repository
    ```sh
    git clone git@gitlab.arandu.org.br:softwarecpid/beija-flor/beijaflor-backend.git
    cd beijaflor-backend
    ```

2. Start a python virtual environment
    ```sh
    python3 -m venv .venv
    ```

3. Source your shell to the virtual environment
    ```sh
    source .venv/bin/activate
    ```

4. Install project dependencies
    ```sh
    pip install -r requirements.txt
    ```

5. Create the `.env` file
    ```sh
    cat app/settings/.env.example > app/settings/.env
    ```

6. Now fill the `.env` with the correct variables

7. Run the application (development mode)
    ```sh
    fastapi dev app/main.py
    ```

8. Change git remote url to avoid accidental pushes to base project (optional)
    ```sh
    git remote set-url origin ""
    git remote -v
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

The usage cases of the API are listed on the `/docs` endpoint. Feel free to take a look.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

All your current tasks are listed on the GPLab plataform. See [your tasks](https://gplab.info/index.php/projects/all_tasks) to know what you have to do.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

<!-- TODO: Add gitlab contributing routine -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the <project_license>. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
[product-screenshot]: imgs/screenshot.png
[fastapi]: https://img.shields.io/badge/fastapi-009688?style=for-the-badge&logo=fastapi&logoColor=white
[fastapi-url]: https://fastapi.tiangolo.com/
[pydantic]: https://img.shields.io/badge/pydantic-E92063?style=for-the-badge&logo=pydantic
[pydantic-url]: https://docs.pydantic.dev/2.0/
[sqlalchemy]: https://img.shields.io/badge/sqlalchemy-D71F00?style=for-the-badge&logo=sqlalchemy
[sqlalchemy-url]: https://www.sqlalchemy.org/

