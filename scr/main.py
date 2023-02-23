from hh import get_vacancies_survey_from_hh
from sj import get_vacancies_survey_from_sj
from terminaltables import DoubleTable
from dotenv import load_dotenv
import json
import os


def get_table_formatting(vacancies_survey):
    header = [
        "Programming Language",
        "Vacancies Found",
        "Vacancies Processed",
        "Average Salary"
    ]
    table = []
    table.append(header)
    for language, statistic in vacancies_survey.items():
        table.append(
            [
                language,
                str(statistic["vacancies_found"]),
                str(statistic["vacancies_processed"]),
                str(statistic["average_salary"])
            ]
        )
    return table


if __name__ == "__main__":
    load_dotenv()
    programming_languages = json.loads(os.getenv("PROGRAMMING_LANGUAGES"))
    token = os.getenv("SUPERJOB_TOKEN")
    hh_survey = get_vacancies_survey_from_hh(programming_languages)
    sj_survey = get_vacancies_survey_from_sj(programming_languages, token)
    table_instance_hh = DoubleTable(get_table_formatting(hh_survey),
                                    " HeadHunter Result Moscow ")
    table_instance_sj = DoubleTable(get_table_formatting(sj_survey),
                                    " SuperJob Result Moscow ")
    print(table_instance_hh.table)
    print()
    print(table_instance_sj.table)
