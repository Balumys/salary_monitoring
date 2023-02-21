def calc_average_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return int((salary_from + salary_to) / 2)
    if not salary_from:
        return int(salary_to * 0.8)
    if not salary_to:
        return int(salary_from * 1.2)
