# Project Title

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Running the CLI](#running-the-cli)
- [CI/CD](#cicd)
- [Development and Testing](#development-and-testing)

## Introduction
This application provides a simple command-line interface CLI to set traffic light times, and provide a graphical display in ASCII characters of a traffic light, with light colors displayed for their respective times. Although this project's main entry point is currently through a CLI tool, the project was also designed to be extensible as a web application, using FastAPI. So if we wanted the light interface to be consumed via http requests, we could easily implement a lightweight UI, and deploy this application to a cloud environment. For more information on project structure and design patterns used in this project, please see the section on development and [Development and Testing](#development-and-testing)

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
If you have poetry installed (which makes project managemenet in python much easier in Python), then you can just install the project and create your lock file:

```bash
    poetry install && poetry lock
```

### pip installation
If you prefer to use pip, then simply run pip install:

```bash
    pip install -r requirements.txt
```

Now your dependencies are installed in your virtual environment

## Usage
The usage for this application is currently supported via the CLI tool. The project was designed to be extensible as a FastAPI web application / microservice as well. Please see the next section for usage instructions for the CLI tool.

## Running the CLI
To run the traffic light simulation CLI, use the following command:

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


















