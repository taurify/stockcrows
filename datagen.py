"""Generate sample data."""
from datetime import date, timedelta
from random import randint
from numpy.random import normal


class CompanyData:
    """Company name, stock data."""

    def __init__(self, name="", data=None):
        """Initialize."""
        if data is None:
            data = []
        self.name = name
        self.data = data


def read_names(name_file: str) -> list:
    """Read company names."""
    with open(name_file, "r") as f:
        names = f.read().splitlines()  # f.readlines() does not strip newline char

    for i in names:
        print(i)
    return names


def write_data_file(output_file: str, companies: list):
    """Write company data to file."""
    with open(output_file, "w") as f:
        # s = "\n".join(companies)
        for i in range(len(companies)):
            for k in range(10):
                for j in range(len(companies[i].data[k])):
                    s = f"{i},{companies[i].data[k][j][0].__str__()},{companies[i].data[k][j][1]}\n"
                    f.write(s)


def generate_start_date():
    """."""
    i = randint(0, 1460)

    d1 = date(2016, 1, 1)
    d1 += timedelta(i)
    return d1


def generate_end_date():
    """."""
    i = randint(0, 50)

    if i == 17:  # Small chance for bankruptcy
        i = randint(0, 1460)
        d1 = date.today()
        d1 -= timedelta(i)
        return d1

    return date.today()


def generate_company_data(names: list):
    """."""
    companies = []

    for name in names:
        d1 = generate_start_date()
        d2 = generate_end_date()

        if d1.year > d2.year or d1.year == d2.year and d1.month > d2.month or \
                d1.year == d2.year and d1.month == d2.month and d1.day >= d2.day:
            d2 = date.today()

        data = generate_stocks(d1, d2)
        comp = CompanyData(name, data)
        companies.append(comp)

    return companies


def generate_stocks(d1: date, d2: date):
    """."""
    data = []

    for a in range(10):
        multiplier = randint(10, 200)
        k = multiplier * 0.5
        m = 0.8 * multiplier
        luck = randint(-2, 6) / 5
        data.append([])
        for i in range(1465):
            d3 = d1 + timedelta(i)

            if d3.year > d2.year or d3.year == d2.year and d3.month > d2.month or \
                    d3.year == d2.year and d3.month == d2.month and d3.day >= d2.day:
                break
            k = (m * normal(0.6, 0.15) + 0.2 * k) * (1 + i * luck / 1465)
            # k += multiplier * normal(0.00005, 0.01)  # Quite like Brown motion, slightly tilted to the growth
            if k < 0:  # Bankruptcy
                # Could be e. g. return data, True, which is: data, flag = generate_stocks(d1, d2, multiplier)
                break  # and comp = CompanyData(name, data, flag), GUI app could show warning with the flag
            data[a].append((d3, float(k)))

    return data


if __name__ == "__main__":
    names1 = read_names("company_names.txt")
    companies1 = generate_company_data(names1)
    write_data_file("company_data.txt", companies1)
