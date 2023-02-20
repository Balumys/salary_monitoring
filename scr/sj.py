import sys
import requests


def get_vacancies_from_sj(token, page_number, language):
    url = "https://api.superjob.ru/2.0/vacancies/"
    numeric_params = {
        "Developer id": 48,
    }
    header = {
        "X-Api-App-Id": token
    }
    params = {
        "town": "Москва",
        "keyword": language,
        "catalogues": numeric_params["Developer id"],
        "order_field": "date",
        "count": 100,
        "page": page_number

    }
    response = requests.get(url, params=params, headers=header)
    response.raise_for_status()
    vacancies = response.json()
    return vacancies


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


def get_vacancies_from_all_pages_sj(token, language):
    page = 0
    pages_number = 1
    vacancies = []
    while page < pages_number:
        page_response = get_vacancies_from_sj(token, page, language)
        vacancies.extend(page_response['objects'])
        if page_response["more"]:
            pages_number += 1
        page += 1
    return vacancies


def calc_statistic_sj(token, language, vacancies):
    result = {}
    salary_per_language = []
    response = get_vacancies_from_sj(token, 0, language)
    vacancies_amount = response["total"]
    for vacancy in vacancies:
        if vacancy:
            salary_per_language.append(predict_rub_salary_for_sj(vacancy))
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


def get_vacancies_survey_from_sj(programming_languages, token):
    sj_vacancies_survey = {}
    try:
        for language in programming_languages:
            vacancies = get_vacancies_from_all_pages_sj(token, language)
            sj_vacancies_survey.update(calc_statistic_sj(token, language, vacancies))
    except requests.exceptions.HTTPError as err:
        sys.exit(err)
    return sj_vacancies_survey


if __name__ == "__main__":
    get_vacancies_survey_from_sj()
