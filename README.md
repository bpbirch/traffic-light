# Project Title

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Running the CLI](#running-the-cli)
- [CI/CD](#cicd)

## Introduction
Provide a brief introduction to your project here.

## Installation
Instructions on how to install your project.

## Usage
The usage for this application is currently entered using the CLI tool. The project was designed to be extensible as a FastAPI web application / microservice as well.

## Running the CLI
To run the traffic light simulation CLI, use the following command:

```bash
    python -m scripts.cli run-traffic-light
```

You can exit the program at any time by entering 'q' (you must hit enter during color time input prompts). Total color times must be greater than 0. You will also be prompted as to whether you want the light pattern to cycle indefinitely. An ASCII representation of a stop light will then be displayed in your terminal.

## CI/CD
Tests run in a github action when merging to main or dev. Please see .github/workflows/ci.yml for details. Tests hit no external http API endpoints, so no credentials are needed in the action.






















