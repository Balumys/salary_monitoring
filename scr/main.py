from hh import get_result_from_hh
from sj import get_result_from_sj
from terminaltables import DoubleTable
from dotenv import load_dotenv


def get_table_formatting(result):
    header = ["Programming Language", "Vacancies Found", "Vacancies Processed", "Average Salary"]
    table = []
    table.append(header)
    languages = result.keys()
    for language in languages:
        table.append(
            [language, str(result[language]["vacancies_found"]), str(result[language]["vacancies_processed"]),
             str(result[language]["average_salary"])])
    return table


if __name__ == "__main__":
    load_dotenv()
    hh_result = get_result_from_hh()
    sj_result = get_result_from_sj()
    table_instance_hh = DoubleTable(get_table_formatting(hh_result), " HeadHunter Result Moscow ")
    print(table_instance_hh.table)
    print()
    table_instance_sj = DoubleTable(get_table_formatting(sj_result), " SuperJob Result Moscow ")
    print(table_instance_sj.table)
