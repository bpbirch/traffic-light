# Project Title

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Running the CLI](#running-the-cli)
- [CI/CD](#cicd)
- [Development and Testing](#development-and-testing)
    - [Development](#development)
    - [Testing](#testing)

## Introduction
Before getting into any 
This application provides a simple command-line interface CLI to set traffic light times, and provide a graphical display in ASCII characters of a traffic light, with light colors displayed for their respective times. Although this project's main entry point is currently a CLI tool, the project was also designed to be extensible as a web application, using FastAPI. So if we wanted the light interface to be consumed via http requests, we could easily implement a lightweight UI, and deploy this application to a cloud environment.

The goal of this project was primarily to write a CLI tool, but also to write code with an eye to readability and extensibility, while also writing code that is representative of my engineering habits and capabilities. For extensibility, I wrote the project as a FastAPI project, using a combination of repository/unit of work, dependency injection, and inversion of control patterns. Regarding those patterns, the code base comports with the following structure:

    - enterypoints/http layer
    - domain layer (contains our models for http input and business logic)
    - service layer (contains the CLI logic)
    - adapters/repositories layer

Writing code in this way allows us to decouple our application logic and database logic. Also, using dependency injection (particularly our injected unit of work) allows us to significantly reduce the size of our E2E tests in our test pyramid, because we can convert quite a few E2E tests to unit tests, by simply testing that the service layer is behaving well, while using an in-memory database.

I understand that a lot of this code was out of scope for the project, but I believe that it provides a very good example of design patterns I use, and allows for extensibility, which was a requirement of the assignment. In terms of extensibility, I wanted to make sure that this code could be used as a web-based microservice in the future, but I also wanted to ensure that the code and CLI could be used for more than traffic lights. For instance, the CLI, and the TrafficLightHandler that is instantiated within the CLI's main function, could both be extended very easily to handle non-standard traffic lights.

## Installation
This application was written as a poetry project, but users can also use pip for isntallation. For either approach, you should have virtualenv installed on your machine. Follow steps below to install dependencies.

### create your virtual environment
From the root of the project, first create a virtual environment:

```bash
    virtualenv -p python3 .venv
```

Now enter your virtual environment:

```bash
    source .venv/bin/activate
```

Once you are inside your virtual environment, you can now install your dependencies.

### poetry installation
If you have poetry installed (which makes project managemenet in python much easier in Python), then you can just install the project and create your lock file with simple poetry commands. You can view poetry dependencies inside of pyproject.toml. Here is the poetry command for installing dependencies and writing your lock file:

```bash
    poetry install && poetry lock
```

### pip installation
If you prefer to use pip, then simply run pip install. The requirements for pip can be found in requirements.txt:

```bash
    pip install -r requirements.txt
```

Now your dependencies are installed in your virtual environment

## Usage
The usage for this application is currently supported via the CLI tool. The project was designed to be extensible as a FastAPI web application / microservice as well. Please see the section on [running the cli](#running-the-cli) for usage instructions for the CLI tool.

## Running the CLI
A quick note for developers who are curious: the source code that is immediately used by the CLI is located at traffic_light/service/traffic_light_cli.yp

For help instructions regarding CLI usage, you can run:

```bash
    python -m scripts.cli run-traffic-light --help
```

After installation is successful, to run the traffic light simulation CLI, use the following command:


```bash
    python -m scripts.cli run-traffic-light
```

You can exit the program at any time by entering 'q' (you must hit enter during color time input prompts). Light times must be non-negative integers, but q can be entered as an escape key. Total color times must be greater than 0. You will also be prompted as to whether you want the light pattern to repeat indefinitely. 

Once you have entered valid inputs, such as 1, 1, 1, for green_time, yellow_time, and red_time, you will see a display of a traffic light, which will either cycle indefinitely if you chose Y in the original prompt for indefinite cycle repeats:

example output:

```
       ***
   ** ****** **
 * ************ *
* ************** *
* ************** *
 * ************ *
   ** ****** **
       ***


       ***
   ** ****** **
 * ************ *
* ************** *
* ************** *
 * ************ *
   ** ****** **
       ***


       ***
   ** ****** **
 * ************ *
* ************** *
* ************** *
 * ************ *
   ** ****** **
       ***
```

Regardless of whether you chose for the lights to cycle indefinitely or not, you can exit the light display loop at any time by pressing 'q'

## CI/CD
Tests run in a github action when merging to main or dev. Please see .github/workflows/ci.yml for details. Tests hit no external http API endpoints, so no credentials are needed in the action / github sercret.

## Development and Testing
This project was built as a poetry project, using commitizen for pre-commit hooks for code quality and type hinting. As part of our pre-commit hooks, we also ensure that our pyproject.toml dependencies are written to requirements.txt, so that developers not using poetry can still run the program and tests. Poetry tasks for mypy, flake8, etc. can be found in pyproject.toml under tool.taskipy.task

### Development
This project uses pre-commit and commitizen for commit hooks (code quality, formatting, etc.). We use mypy for type checking, flake8 for linting, and black for formatting. We run pre-commit hooks with those tools when we commit, by using commitizen. Commitizen is also used for semantic versioning. The following steps should be followed for commits.

First, make sure you have pre-commit hooks installed:

```bash
    pre-commit install
```

Then, when commiting, instead of running git commit, you should run:

```bash
    cz commit
```

You will then be prompted to specify breaking changes and provide a commit message. Then, before being checked in to remote, pre commit hooks will run that check mypy, flake8, black, and also copy our pyproject.toml file dependencies to requirements.txt, so that dependencies stay in sync for poetry and non poetry developers.

### Testing
To run all tests from a poetry environment, tests can be run with printed output, or without printed output. 

To run tests without printed output:

```bash
    poetry run task tests
```

To run with printed output:

```bash
    poetry run task tests_verbose
```

If you are not using a poetry environment, then you can run tests directly using pytest:

```bash
    pytest tests
```

The tests that are specific to the CLI can be found under tests/integration/test_traffic_light_cli.py. Other tests can be found under tests/unit and tests/e2e. Those tests mainly pertain to the underlying models that are used at the http layer and service layer of this project, if we wanted to extend the project to be a full microservice.
