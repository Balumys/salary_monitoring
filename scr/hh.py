import sys
import requests


def get_vacancies_from_hh(language, page_number):
    url = "https://api.hh.ru/vacancies"
    numeric_params = {
        "Moscow": 1,
        "Last month": 30,
        "Developer_id": 96
    }
    header = {
        "User-Agent": "API test"
    }
    params = {
        "text": language,
        "area": numeric_params["Moscow"],
        "per_page": 90,
        "page": page_number,
        "period": numeric_params["Last month"],
        "professional_roles": numeric_params["Developer_id"]
    }
    response = requests.get(url, headers=header, params=params)
    response.raise_for_status()
    vacancies = response.json()
    return vacancies


def predict_rub_salary(vacancy):
    salary_range = vacancy['salary']
    if not salary_range:
        return None
    if vacancy['salary']['currency'] != 'RUR':
        return None
    if not salary_range["from"] and not salary_range["to"]:
        return None
    if not salary_range["from"]:
        salary = salary_range["to"] * 0.8
        return salary
    if not salary_range["to"]:
        salary = salary_range["from"] * 1.2
        return salary
    salary = (salary_range["from"] + salary_range["to"]) / 2
    return salary


def calc_statistic_hh(language, vacancies):
    statistic = {}
    salary_per_language = []
    vacancies_amount = vacancies[-1]
    vacancies.pop()
    for vacancy in vacancies:
        if not vacancy:
            continue
        salary_per_language.append(predict_rub_salary(vacancy))
    while None in salary_per_language:
        salary_per_language.remove(None)
        try:
            average_salary = round(sum(salary_per_language) / len(salary_per_language))
        except ZeroDivisionError as err:
            sys.exit(err)
    statistic[language] = {
        "vacancies_found": vacancies_amount,
        "vacancies_processed": len(salary_per_language),
        "average_salary": average_salary
    }
    return statistic


def get_vacancies_from_all_pages_hh(language):
    page = 0
    pages_number = 19
    vacancies = []
    while page < pages_number:
        page_response = get_vacancies_from_hh(language, page)
        vacancies.extend(page_response['items'])
        pages_number = page_response["pages"]
        page += 1
    vacancies_amount = page_response["found"]
    vacancies.append(vacancies_amount)
    return vacancies


def get_vacancies_survey_from_hh(programming_languages):
    hh_vacancies_survey = {}
    try:
        for language in programming_languages:
            vacancies = get_vacancies_from_all_pages_hh(language)
            hh_vacancies_survey.update(calc_statistic_hh(language, vacancies))
    except requests.exceptions.HTTPError as err:
        sys.exit(err)
    return hh_vacancies_survey


if __name__ == "__main__":
    get_vacancies_survey_from_hh()
