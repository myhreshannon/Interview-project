# Interview project
## Overview
This Python program runs a basic health check on any URLs provided in a yaml config file. It will check that the request was successful and was completed in less than 500ms. After checking all provided URLs, it will report the current uptime percentage in the console. The checks will repeat every 15 seconds until the program is exited by the user.

## Requirements
Python ([download](https://www.python.org/downloads/))

Packages used: pyyaml, requests

## Steps for use
```
git clone https://github.com/myhreshannon/Interview-project
cd Interview-project
python -m venv venv
python .\healthcheck.py sample_input.yml
