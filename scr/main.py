from hh import get_result_from_hh
from sj import get_result_from_sj
from terminaltables import DoubleTable


def get_table_formatting(result):
    header = ["Programming Language", "Vacancies Found", "Vacancies Processed", "Average Salary"]
    table = []
    table.append(header)
    for key in result.keys():
        table.append(
            [key, str(result[key]["vacancies_found"]), str(result[key]["vacancies_processed"]),
                 str(result[key]["average_salary"])])
    return table


if __name__ == "__main__":
    hh_result = get_result_from_hh()
    sj_result = get_result_from_sj()
    table_instance_hh = DoubleTable(get_table_formatting(hh_result), " HeadHunter Result Moscow ")
    print(table_instance_hh.table)
    print()
    table_instance_sj = DoubleTable(get_table_formatting(sj_result), " SuperJob Result Moscow ")
    print(table_instance_sj.table)
