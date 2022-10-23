Image Super Resolution
---
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#prerequisites">Prerequisites</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#other-commands">Other commands</a></li>
    <li><a href="#connect-to-database">Connect to database</a></li>
    <li><a href="#credits">Credits</a></li>

  </ol>
</details>

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

- Clone this repo
- Install the prerequisites
- Run the service
- Check http://localhost:8080
- Done! :tada:
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Prerequisites

- Install [Docker](https://www.docker.com/)
- Install [Docker Compose](https://docs.docker.com/compose/install/)
- Following the Airflow release from [Python Package Index](https://pypi.python.org/pypi/apache-airflow)
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Usage

Run the web service with docker

```
docker-compose up -d

# Build the image
# docker-compose up -d --build
```

Check http://localhost:8080/

- `docker-compose logs` - Displays log output
- `docker-compose ps` - List containers
- `docker-compose down` - Stop containers
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Other commands

If you want to run airflow sub-commands, you can do so like this:

- `docker-compose run --rm webserver airflow list_dags` - List dags
- `docker-compose run --rm webserver airflow test [DAG_ID] [TASK_ID] [EXECUTION_DATE]` - Test specific task

If you want to run/test python script, you can do so like this:
- `docker-compose run --rm webserver python /usr/local/airflow/dags/[PYTHON-FILE].py` - Test python script
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Connect to database

If you want to use Ad hoc query, make sure you've configured connections:
go to Airflow UI Dashboard, click Admin -> Connections and Edit "postgres_default" set this values:
- Host : postgres
- Schema : airflow
- Login : airflow
- Password : airflow
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Credits

- [Apache Airflow](https://github.com/apache/incubator-airflow)
- [docker-airflow](https://github.com/puckel/docker-airflow/tree/1.10.0-5)
<p align="right">(<a href="#readme-top">back to top</a>)</p>