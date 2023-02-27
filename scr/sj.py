import sys
import requests
from average_salary import calc_average_salary
from Numeric_params import ParametersSJ


def get_vacancies_from_sj(token, page_number, language):
    url = "https://api.superjob.ru/2.0/vacancies/"
    header = {
        "X-Api-App-Id": token
    }
    params = {
        "town": "Москва",
        "keyword": language,
        "catalogues": ParametersSJ.DeveloperID.value,
        "order_field": "date",
        "count": 100,
        "page": page_number

    }
    response = requests.get(url, params=params, headers=header)
    response.raise_for_status()
    vacancies = response.json()
    return vacancies


def predict_rub_salary_for_sj(vacancy):
    salary_from = vacancy["payment_from"]
    salary_to = vacancy["payment_to"]
    if not salary_from and not salary_to:
        return None
    if vacancy["currency"] != "rub":
        return None
    return calc_average_salary(salary_from, salary_to)


def get_vacancies_from_all_pages_sj(token, language) -> dict:
    page = 0
    pages_number = 1
    vacancies_sj = dict()
    vacancies = []
    while page < pages_number:
        page_response = get_vacancies_from_sj(token, page, language)
        vacancies.extend(page_response['objects'])
        if page_response["more"]:
            pages_number += 1
        page += 1
    vacancies_amount = page_response["total"]
    vacancies_sj["vacancies"] = vacancies
    vacancies_sj["vacancies_amount"] = vacancies_amount
    return vacancies_sj


def calc_statistic_sj(vacancies_info):
    statistic = {}
    salaries_per_language = []
    vacancies=vacancies_info["vacancies"]
    vacancies_amount = vacancies_info["vacancies_amount"]
    for vacancy in vacancies:
        if not vacancy:
            continue
        predict_salary = predict_rub_salary_for_sj(vacancy)
        if not predict_salary:
            continue
        salaries_per_language.append(predict_salary)
    try:
        average_salary = round(sum(salaries_per_language) / len(salaries_per_language))
    except ZeroDivisionError:
        average_salary = 0
    statistic = {
        "vacancies_found": vacancies_amount,
        "vacancies_processed": len(salaries_per_language),
        "average_salary": average_salary
    }
    return statistic


def get_vacancies_survey_from_sj(programming_languages, token):
    sj_vacancies_survey = {}
    try:
        for language in programming_languages:
            vacancies_info = get_vacancies_from_all_pages_sj(token, language)
            sj_vacancies_survey[language] = calc_statistic_sj(vacancies_info)
    except requests.exceptions.HTTPError as err:
        sys.exit(err)
    return sj_vacancies_survey


if __name__ == "__main__":
    get_vacancies_survey_from_sj()
