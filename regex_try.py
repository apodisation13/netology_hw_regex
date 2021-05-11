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


def csv_reader(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = csv.reader(file, delimiter=',')
        list_data = list(data)
        return list_data


def csv_writer(file_path, contacts_list):
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        datawriter = csv.writer(file, delimiter=',')
        datawriter.writerows(contacts_list)
    print(f'Проверьте файл {file_path}')


def make_full_name(line, surname_list):
    correct_name = []  # для каждой строки исходного файла отдельный массив с правильными ФИО

    surname = line[0].split()
    # print(surname)
    if surname[0] not in surname_list:
        surname_list.append(surname[0])

        correct_name = re.findall(r'(\w+)', ' '.join(line[:3]))
        if len(correct_name) < 3:
            correct_name.append('')

    return correct_name


def find_name_index_line(surname_list, surname):
    for person in surname_list:
        if surname == person:
            number = surname_list.index(person)  # ищу по фамилии номер строки повторяющегося человека
            # print(number)
            return number


def make_info(line, correct_name, clean_data, number):
    info_list = []  # список для позиций 3-6

    organization = line[3]
    position = line[4]
    phone = line[5]
    mail = line[6]
    # print(organization, position, phone, mail)

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


def make_clean_data():
    raw_data = csv_reader('default_phonebook.csv')

    clean_data = []  # ИТОГОВЫЙ СПИСОК
    surname_list = []  # в этот список буду добавлять фамилии, чтобы искать повторы

    clean_data.append(raw_data[0])  # добавляю заголовки полей из исходного файла

    for line in raw_data[1:]:

        correct_name = make_full_name(line, surname_list)
        number = find_name_index_line(surname_list, line[0].split()[0])

        make_info(line, correct_name, clean_data, number)

    for line in clean_data:
        print(line)

    return clean_data


if __name__ == "__main__":
    clean_list = make_clean_data()
    csv_writer('clean_phonebook.csv', clean_list)
