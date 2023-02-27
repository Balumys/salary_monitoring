import requests
from average_salary import calc_average_salary
from Numeric_params import ParametersHH


def get_vacancies_from_hh(language, page_number):
    url = "https://api.hh.ru/vacancies"
    header = {
        "User-Agent": "API test"
    }
    params = {
        "text": language,
        "area": ParametersHH.Moscow.value,
        "per_page": 90,
        "page": page_number,
        "period": ParametersHH.LastMont.value,
        "professional_roles": ParametersHH.DeveloperID.value
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
    salary_from = salary_range["from"]
    salary_to = salary_range["to"]
    return calc_average_salary(salary_from, salary_to)


def calc_statistic_hh(vacancies_info):
    statistic = {}
    salaries_per_language = []
    vacancies_amount = vacancies_info["vacancies_amount"]
    vacancies = vacancies_info["vacancies"]
    for vacancy in vacancies:
        if not vacancy:
            continue
        salary = predict_rub_salary(vacancy)
        if not salary:
            continue
        salaries_per_language.append(salary)
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


def get_vacancies_from_all_pages_hh(language) -> dict:
    page = 0
    pages_number = 19
    vacancies_hh = dict()
    vacancies = []
    while page < pages_number:
        page_response = get_vacancies_from_hh(language, page)
        vacancies.extend(page_response['items'])
        pages_number = page_response["pages"]
        page += 1
    vacancies_amount = page_response["found"]
    vacancies_hh["vacancies"] = vacancies
    vacancies_hh["vacancies_amount"] = vacancies_amount
    return vacancies_hh


def get_vacancies_survey_from_hh(programming_languages):
    hh_vacancies_survey = {}
    for language in programming_languages:
        vacancies_info = get_vacancies_from_all_pages_hh(language)
        hh_vacancies_survey[language] = calc_statistic_hh(vacancies_info)
    return hh_vacancies_survey


if __name__ == "__main__":
    get_vacancies_survey_from_hh()
