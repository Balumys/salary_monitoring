import sys
import requests


def get_response_from_hh(language, page_number):
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
    return response


def predict_rub_salary(vacancy):
    salary_range = vacancy['salary']
    if salary_range is not None:
        if vacancy['salary']['currency'] == 'RUR':
            if salary_range["from"] and salary_range["to"] is not None:
                salary = (salary_range["from"] + salary_range["to"]) / 2
            else:
                salary = salary_range["from"] * 1.2 if salary_range["to"] is None else salary_range["to"] * 0.8
        else:
            salary = None
    else:
        salary = None
    return salary


def calc_statistic_hh(language, vacancies):
    statistic = {}
    salary_per_language = []
    response = get_response_from_hh(language, 0)
    vacancies_amount = response.json()["found"]
    for vacancy in vacancies:
        if vacancy:
            salary_per_language.append(predict_rub_salary(vacancy))
        else:
            continue
    while None in salary_per_language:
        salary_per_language.remove(None)
    statistic[language] = {
        "vacancies_found": vacancies_amount,
        "vacancies_processed": len(salary_per_language),
        "average_salary": round(sum(salary_per_language) / len(salary_per_language))
    }
    return statistic


def get_vacancies_from_all_pages_hh(language):
    page = 0
    pages_number = 19
    vacancies = []
    while page < pages_number:
        page_response = get_response_from_hh(language, page)
        vacancies_found = page_response.json()["found"]
        page_payload = page_response.json()
        vacancies.extend(page_payload['items'])
        pages_number = (vacancies_found // 100) + 1 if (vacancies_found // 100) + 1 < 20 else 20
        page += 1
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
