import os
import sys
import requests
import json
from dotenv import load_dotenv


def get_vacancies_from_sj(token, page, key):
    url = "https://api.superjob.ru/2.0/vacancies/"
    header = {
        "X-Api-App-Id": token
    }
    params = {
        "town": "Москва",
        "keyword": key,
        "catalogues": 48,
        "order_field": "date",
        "no_agreement": 1,
        "count": 100,
        "page": page

    }
    response = requests.get(url, params=params, headers=header)
    response.raise_for_status()
    return response


def predict_rub_salary_for_sj(vacancy):
    if vacancy["currency"] == "rub":
        if vacancy["payment_from"] and vacancy["payment_to"] != 0:
            salary = (vacancy["payment_from"] + vacancy["payment_to"]) / 2
        elif vacancy["payment_from"] != 0:
            salary = vacancy["payment_from"] * 1.2
        elif vacancy["payment_to"] != 0:
            salary = vacancy["payment_to"] * 0.8
        else:
            return None
    else:
        return None
    return int(salary)


def get_all_pages_sj(token, key):
    page = 0
    pages_number = 19
    all_pages = []
    while page < pages_number:
        page_response = get_vacancies_from_sj(token, page, key)
        vacancies_found = page_response.json()["total"]
        page_payload = page_response.json()
        all_pages.extend(page_payload['objects'])
        pages_number = (vacancies_found // 100) + 1 if (vacancies_found // 100) + 1 < 20 else 20
        page += 1
    return all_pages


def calc_statistic_sj(token, key, all_pages_response):
    result = {}
    salary_per_language = []
    response = get_vacancies_from_sj(token, 0, key)
    vacancies_amount = response.json()["total"]
    vacancies = all_pages_response
    for vacancy in vacancies:
        if vacancy:
            salary_per_language.append(predict_rub_salary_for_sj(vacancy))
        else:
            continue
    while None in salary_per_language:
        salary_per_language.remove(None)
    result[key] = {
        "vacancies_found": vacancies_amount,
        "vacancies_processed": len(salary_per_language),
        "average_salary": round(sum(salary_per_language) / len(salary_per_language))
    }
    return result


def get_result_from_sj():
    load_dotenv()
    token = os.getenv("SUPERJOB_TOKEN")
    programming_languages = json.loads(os.getenv("PROGRAMMING_LANGUAGES"))
    super_job_result = {}
    try:
        for language in programming_languages:
            all_pages = get_all_pages_sj(token, language)
            super_job_result.update(calc_statistic_sj(token, language, all_pages))
    except requests.exceptions.HTTPError as err:
        sys.exit(err)
    return super_job_result


if __name__ == "__main__":
    get_result_from_sj()
