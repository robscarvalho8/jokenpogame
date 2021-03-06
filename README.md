# JokenpoGame

A simple API that returns the result of a Jokenpo game

## Introduction

Description of technologies used and expectations

Python 3.9 language was used as standard backend technology

The framework was used [Flask](https://flask.palletsprojects.com/en/2.0.x/)

We use the [Pandas](https://pandas.pydata.org/) library to work with the data

To run the tests we use [pytest](https://docs.pytest.org/en/7.0.x/)


## Overview

The application receives 3 query parameters, in its URL, coin_from, coint_to and amout:
    
- player: Player number
- play: Play chosen by the player
- entrance: Player entry number


Documentation and details can be found at the following endpoints:


    localhost:5000/docs

## Requirements

To run the project locally you need the following tools:

- [Git](https://git-scm.com/), to clone the project
- [Docker](https://docs.docker.com/engine/install/)

## Install and Run Project

To run locally, just clone the repository and start dockerfile:
- Clone the project (repository: [https://github.com/robscarvalho8/jokenpogame.git](https://github.com/robscarvalho8/jokenpogame.git))
- Select project folder

### RUN Dockerfile

1 - Build docker

    $ docker build -t jokenpogame .

2 - Run Docker

    $ docker run -d -p 5000:5000 --name jokenpogame jokenpogame

3 - Run Tests: First entry in a docker bash:

    $ docker exec -it jokenpogame bash

4 - Run Tests: Second inside a docker execute:

    $ pytest




## Directory Structure



    ├── api                          <-  The code of interest
    │   ├── models                   <- Package where the request schemas are found 
    │   ├── server                   <- Package that provider server to ../main.py
    │   ├── tests                    <- Package where the application tests are located 
    │   └── views                    <- Package where the application endpoints are made available
    ├── Dockerfile                   <- Dockerfile to up application
    ├── main.py                      <- Code that launches the application
    ├── Pipfile                      <- Package and distribution management up
    └── Pipfile.lock                 <- Package and distribution management up