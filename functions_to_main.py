#imported libraries
import requests
import json
import xlsxwriter
from collections import defaultdict
from math import floor
import pprint



#functions

def request_and_json_from_site(site_link, file_name):
    request = requests.get(str(site_link))
    try:
        toJson = request.json()
        with open(str(file_name), 'w', encoding='UTF-8') as json_file:
            json.dump(toJson, json_file, ensure_ascii=False, indent=4)

    except requests.exceptions.JSONDecodeError:
        print('Not possible to format from Json\'a to Python')

    else:
        return toJson


def creating_dic_id_correct_tasks(converted_from_json):
    corrected_dic = defaultdict(int)
    for line in converted_from_json:
        if line['completed'] == True:
            corrected_dic[line['userId']] += 1

    return corrected_dic


def creating_list_of_best_usersId(corrected_dic):
    best_correct_value = max(corrected_dic.values())
    worst_correct_value = min(corrected_dic.values())

    list_of_best_usersId = [userId for userId, numberOfCorrectness in corrected_dic.items() \
                            if numberOfCorrectness == best_correct_value]
    list_of_worst_usersId = [userId for userId, numberOfCorrectness in corrected_dic.items() \
                             if numberOfCorrectness == worst_correct_value]

    return (list_of_best_usersId, list_of_worst_usersId)

def display_best_and_worst_usersId(list_usersId_best_worst):
    for n in range(len(list_usersId_best_worst)):
        if n == 0:
            joined = ", ".join(str(e) for e in list_usersId_best_worst[n])
            good = f'The most correct answer has/have user/s with id: {joined}'
        else:
            joined = ", ".join(str(e) for e in list_usersId_best_worst[n])
            bad = f'The least correct answer has/have user/s with id: {joined}'

    return print('{}\n{}\n'.format(good,bad))


def create_list_of_dicts_users_informations(list_of_users,dict_users_correct_tasks):
    list_of_dicts_users_info = []
    for it in range(len(list_of_users)):
        dict_users_info = {}
        for k, v in list_of_users[it].items():
            if k == 'address':
                dict_users_info['city'] = list_of_users[it][k]['city']
                continue
            if k == 'website':
                dict_users_info['correct tasks'] = dict_users_correct_tasks[it+1]
                dict_users_info['Percentage of correct tasks'] = floor((dict_users_correct_tasks[it+1]/ 20 * 100))
                break

            dict_users_info[k] = v
        list_of_dicts_users_info.append(dict_users_info)
        del dict_users_info
    return list_of_dicts_users_info


def create_xlsx_and_add_dates(list_of_users,dict_users_correct_tasks, file_name: str) -> str:
    workbook = xlsxwriter.Workbook(file_name)
    excel_sheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True,'align':'center'})

    for i, (k, v) in enumerate(list_of_users[0].items()):
        if k != 'address':
            excel_sheet.set_column(0, i, 30)
            excel_sheet.write(0, i, k, bold)
        else:
            excel_sheet.set_column(i, i, 30)
            excel_sheet.write(0,i,'City',bold)
            excel_sheet.set_column(i+1, i+1, 30)
            excel_sheet.write(0,i+1,'Phone number',bold)
            excel_sheet.set_column(i + 2, i + 2, 20)
            excel_sheet.write(0, i + 2, 'Correct tasks', bold)
            excel_sheet.set_column(i + 3, i + 3, 30)
            excel_sheet.write(0, i + 3, 'Percent of correct tasks [%]', bold)
            break

    #wywolanie funkcji, ktra tworzy liste słowników z danymi uzytkownikow
    list_dict_users_dates = create_list_of_dicts_users_informations(list_of_users, dict_users_correct_tasks)

    #wpisanie danych do arkusza kalkulacyjnego
    for iter in range (len(list_dict_users_dates)):
        for i, v in enumerate(list_dict_users_dates[iter].values()):
            excel_sheet.write(iter+1,i,v)

    workbook.close()

