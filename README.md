# Salary Monitoring
Salary Monitoring is a console script that allows you to monitor vacancies amounts and average salaries on user defined
programming languages from two most popular job services, [HeadHunter](https://hh.ru) and [SuperJob](https://www.superjob.ru).

## How to install
### Pre-requests
1. Get a free API Key at [SuperJob API](https://api.superjob.ru/register)


### Installation
Python3 should be already installed

You need **3** additional libraries: python-dotenv, terminaltables, requests.

To install them use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:

```
pip install -r requirements.txt
```
Place API token in **.env** file and specify the programming languages you want to get information from.

```
PROGRAMMING_LANGUAGES=["Python","Java","JavaScript","C++","C#","1c","Scala"]
SUPERJOB_TOKEN=YourToken
```

## Usage
Salary monitoring contains one script **main.py** for printing results in the terminal and **2** additional ones for 
fetching data from HeadHunter and SuperJob accordingly. 

### main.py
Getting result from HeadHunter and SuperJob and print table in terminal.

Example: ``python3 main.py ``
```
╔ HeadHunter Result Moscow ══════════════╦═════════════════════╦════════════════╗
║ Programming Language ║ Vacancies Found ║ Vacancies Processed ║ Average Salary ║
╠══════════════════════╬═════════════════╬═════════════════════╬════════════════╣
║ Python               ║ 889             ║ 721                 ║ 190147         ║
║ Java                 ║ 480             ║ 407                 ║ 226524         ║
║ JavaScript           ║ 1075            ║ 915                 ║ 169168         ║
║ C++                  ║ 452             ║ 414                 ║ 176345         ║
║ C#                   ║ 323             ║ 301                 ║ 178198         ║
║ 1c                   ║ 19082           ║ 1798                ║ 124912         ║
║ Scala                ║ 35              ║ 32                  ║ 230516         ║
╚══════════════════════╩═════════════════╩═════════════════════╩════════════════╝

╔ SuperJob Result Moscow ════════════════╦═════════════════════╦════════════════╗
║ Programming Language ║ Vacancies Found ║ Vacancies Processed ║ Average Salary ║
╠══════════════════════╬═════════════════╬═════════════════════╬════════════════╣
║ Python               ║ 6               ║ 6                   ║ 115680         ║
║ Java                 ║ 3               ║ 3                   ║ 155000         ║
║ JavaScript           ║ 15              ║ 15                  ║ 120272         ║
║ C++                  ║ 12              ║ 12                  ║ 163500         ║
║ C#                   ║ 2               ║ 2                   ║ 122500         ║
║ 1c                   ║ 35              ║ 35                  ║ 157602         ║
║ Scala                ║ 1               ║ 1                   ║ 240000         ║
╚══════════════════════╩═════════════════╩═════════════════════╩════════════════╝

```

### Additional files
#### hh.py
Contain functions to get data from [HeadHunter API](https://dev.hh.ru) and calculating average salary per programming
language.
#### sj.py
Contain functions to get data from [SuperJob API](https://api.superjob.ru/register) and calculating average salary per programming
language.

## Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
