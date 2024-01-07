from category_crawler import kategoriju_crawler
from category_crawler import irasyti_i_csv
from data_ex import run_data_ex
from data_ex import clear_file
from data_ex import print_csv_file
from data_ex import run_data_extracion
from data_ex import clear_json_file


def time_limit_setup(msg):
    while True:
        try:
            time_limit = int(input(msg))
            return time_limit
        except ValueError:
            print("Prašome įvesti skaičių.")

def logika(msg):
    while True:
        atsakymas = input(msg).upper()
        if atsakymas in ["Y", "N"]:
            return atsakymas
        print("Prašome įvesti 'Y' arba 'N'.")

atsakymas = logika("Ar norite pradėti kategorijų gavimą iš tinklapio? (Y/N): ")
if atsakymas == "Y":
    kategorijos = kategoriju_crawler()
    print("Gautos kategorijos:")
    for kategorija in kategorijos:
        print(kategorija)

    atsakymas = logika("Ar norite įrašyti gautas kategorijas į CSV failą? (Y/N): ")
    if atsakymas == "Y":
        irasyti_i_csv(kategorijos)


atsakymas = logika("Ar norite pradėti duomenų išgavimą iš pasirinktų kategorijų ? (Y/N): ")
if atsakymas == "Y":
    time_limit = time_limit_setup("Nustatykite laiko limitą duomenų išgavimui (sekundėmis): ")
    run_data_ex(time_limit)

atsakymas = logika("Ar norite įrašyti duomenis į csv ir Json failą ? (Y/N): ")
if atsakymas == "Y":
        clear_file()
        print_csv_file()
        clear_json_file()
        run_data_extracion()
        print("Duomenys sėkmingai gauti ir įrašyti į data.csv failą !")

