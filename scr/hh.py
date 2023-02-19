import os
import sys
import requests
import json
from dotenv import load_dotenv


def get_vacancies_from_hh(key: str, page: int):
    url = "https://api.hh.ru/vacancies"
    header = {
        "User-Agent": "API test"
    }
    params = {
        "text": key,
        "area": 1,
        "per_page": 90,
        "page": page,
        "period": 30,
        "professional_roles": 96,
        "only_with_salary": True
    }
    response = requests.get(url, headers=header, params=params)
    response.raise_for_status()
    return response


def predict_rub_salary(vacancy):
    salary_range = vacancy['salary']
    if vacancy['salary']['currency'] == 'RUR':
        if salary_range["from"] and salary_range["to"] is not None:
            salary = (salary_range["from"] + salary_range["to"]) / 2
        else:
            salary = salary_range["from"] * 1.2 if salary_range["to"] is None else salary_range["to"] * 0.8
    else:
        salary = None
    return salary


def calc_statistic_hh(language, all_pages_response):
    result = {}
    salary_per_language = []
    response = get_vacancies_from_hh(language, 0)
    vacancies_amount = response.json()["found"]
    vacancies = all_pages_response
    for vacancy in vacancies:
        if vacancy:
            salary_per_language.append(predict_rub_salary(vacancy))
        else:
            continue
    while None in salary_per_language:
        salary_per_language.remove(None)
    result[language] = {
        "vacancies_found": vacancies_amount,
        "vacancies_processed": len(salary_per_language),
        "average_salary": round(sum(salary_per_language) / len(salary_per_language))
    }
    return result


def get_all_pages_hh(key):
    page = 0
    pages_number = 19
    all_pages = []
    while page < pages_number:
        page_response = get_vacancies_from_hh(key, page)
        vacancies_found = page_response.json()["found"]
        page_payload = page_response.json()
        all_pages.extend(page_payload['items'])
        pages_number = (vacancies_found // 100) + 1 if (vacancies_found // 100) + 1 < 20 else 20
        page += 1
    return all_pages


def get_result_from_hh():
    load_dotenv()
    programming_languages = json.loads(os.getenv("PROGRAMMING_LANGUAGES"))
    head_hunter_result = {}
    try:
        for language in programming_languages:
            all_pages = get_all_pages_hh(language)
            head_hunter_result.update(calc_statistic_hh(language, all_pages))
    except requests.exceptions.HTTPError as err:
        sys.exit(err)
    return head_hunter_result


if __name__ == "__main__":
    get_result_from_hh()
