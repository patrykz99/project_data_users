#imported libraries
import requests
from collections import defaultdict
import xlsxwriter


#functions
def creating_dic_id_correct_tasks(converted_from_json):
    corrected_dic = defaultdict(int)
    for line in converted_from_json:
        if line['completed'] == True:
            corrected_dic[line['userId']] += 1

    return corrected_dic


def creating_list_of_best_usersId(corrected_dic):
    best_correct_value = max(corrected_dic.values())
    list_of_best_usersId = []
    for userId, numberOfCorrectness in corrected_dic.items():
        if numberOfCorrectness == best_correct_value:
            list_of_best_usersId.append(userId)

    return list_of_best_usersId

def convert_users_from_list_to_string(list_usersId):
    conj_string = 'id='
    it = 1
    for id in list_usersId:
        if it == len(list_usersId):
            conj_string += str(id)
        else:
            it+= 1
            conj_string += str(id) + '&id='

    return conj_string

def choose_info_about_best_person(bestUsers, key: str='name') -> str:
    for user in bestUsers:
        print(f'{user[key]} will get a raise!!!')


def create_xlsx(users_to_create_headings, file_name: str) -> str:
    workbook = xlsxwriter.Workbook(file_name)
    excel_sheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True,'align':'center'})

    for i, (k, v) in enumerate(users_to_create_headings[0].items()):
        if k != 'address':
            excel_sheet.set_column(0,i, 15)
            excel_sheet.write(0, i, k,bold )
        else:
            excel_sheet.set_column(i, i, 20)
            excel_sheet.write(0,i,'Correct tasks',bold)
            excel_sheet.set_column(i+1, i+1, 30)
            excel_sheet.write(0,i+1,'Percentage of correct tasks',bold)
            break

    workbook.close()
def add_dates_to_xlsx():
    pass

if __name__ == "__main__":

    request = requests.get('https://jsonplaceholder.typicode.com/todos')

    try:
        toJson = request.json()

    except requests.exceptions.JSONDecodeError:
        print('Not possible to format from Json\'a to Python')
    else:
        corrected_dic = creating_dic_id_correct_tasks(toJson)
        list_usersId = creating_list_of_best_usersId(corrected_dic)
        best_users = convert_users_from_list_to_string(list_usersId)
        request2 = requests.get('https://jsonplaceholder.typicode.com/users?' + str(best_users))
        list_of_best_users = request2.json()

        print(f'''Employees with id: {",".join(str(e) for e in list_usersId)} have obtained the most correct answers!!! 
        
So: ''')
        choose_info_about_best_person(list_of_best_users)
        create_xlsx(list_of_best_users, 'tableDates.xlsx')





