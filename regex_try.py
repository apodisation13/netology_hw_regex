import csv
import re


def make_phone_patter(phone_str: str):
    if re.search('доб', phone_str):
        pattern_phone = r"(\+7|8)?\s*\(?(\d{3})\)?[-\s]*(\d{3})[-\s]*(\d{2})[-\s]*(\d{2})[-\s\W\D]*(\d+)?[-\s\W\D]*"
        result = re.sub(pattern_phone, r"+7(\2)\3-\4-\5 доб.\6", phone_str)
    else:
        pattern_phone = r"(\+7|8)?\s*\(?(\d{3})\)?[-\s]*(\d{3})[-\s]*(\d{2})[-\s]*(\d{2})"
        result = re.sub(pattern_phone, r"+7(\2)\3-\4-\5", phone_str)
    # print(result)
    return result


with open('default_phonebook.csv', 'r', encoding='utf-8') as file:
    data = csv.reader(file, delimiter=',')
    raw_data = list(data)

clean_data = []
surname_list = []  # в этот список буду добавлять фамилии, чтобы искать повторы

clean_data.append(raw_data[0])  # добавляю заголовки полей из исходного файла

for line in raw_data[1:]:

    correct_name = []  # для каждой строки исходного файла отдельный массив с правильными ФИО

    surname = line[0].split()
    # print(surname)
    if surname[0] not in surname_list:
        surname_list.append(surname[0])

        # ниже пойдём только если не повторное имя
        # if len(surname) == 1:
        #     correct_name.append(surname[0])
        # elif len(surname) == 2:
        #     correct_name.append(surname[0])
        #     correct_name.append(surname[1])
        # elif len(surname) == 3:
        #     correct_name.append(surname[0])
        #     correct_name.append(surname[1])
        #     correct_name.append(surname[2])
        #
        # first_name = line[1].split()
        #
        # if len(first_name) == 1:
        #     correct_name.append(first_name[0])
        # elif len(first_name) == 2:
        #     correct_name.append(first_name[0])
        #     correct_name.append(first_name[1])
        #
        # last_name = line[2]
        # if last_name:
        #     correct_name.append(last_name)
        #
        correct_name = re.findall(r'(\w+)', ' '.join(line[:3]))
        if len(correct_name) < 3:
            correct_name.append('')
        # print(correct_name)

    # print(surname[0])
    for person in surname_list:
        if surname[0] == person:
            number = surname_list.index(person)  # ищу по фамилии номер строки повторяющегося человека
            # print(number)
            break

    info_list = []  # список для позиций 3-6
    total = []

    organization = line[3]
    position = line[4]
    phone = line[5]
    mail = line[6]

    if correct_name:  # если имя не повторяется
        info_list.append(organization)
        info_list.append(position)
        correct_phone = make_phone_patter(phone)
        info_list.append(correct_phone)
        info_list.append(mail)
        # print(info_list)

        total = correct_name + info_list
        # print(total)
        clean_data.append(total)
        # print(clean_data)
    else:
        if organization:
            clean_data[number + 1][3] = organization
        if position:
            clean_data[number + 1][4] = position
        if phone:
            correct_phone = make_phone_patter(phone)
            clean_data[number + 1][5] = correct_phone
        if mail:
            clean_data[number + 1][6] = mail


for line in clean_data:
    print(line)
