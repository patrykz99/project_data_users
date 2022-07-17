#imported from other
import functions_to_users as ftu

#imported libraries
import requests
import json
from collections import defaultdict
import xlsxwriter


if __name__ == "__main__":

        req1 = ftu.request_and_json_from_site('https://jsonplaceholder.typicode.com/todos', 'jsonDatesTasks.json',0)
        corrected_dic = ftu.creating_dic_id_correct_tasks(req1)
        list_usersId = ftu.creating_list_of_best_usersId(corrected_dic)
        best_users = ftu.convert_users_from_list_to_string(list_usersId)
        req2 = ftu.request_and_json_from_site('https://jsonplaceholder.typicode.com/users?', 'jsonDatesUsers.json',best_users,1)
        list_of_best_users = req2

        print(f'''Employees with id: {",".join(str(e) for e in list_usersId)} have obtained the most correct answers!!!

So: ''')
        ftu.choose_info_about_best_person(list_of_best_users,list_usersId)
        ftu.create_xlsx(list_of_best_users, 'tableDates.xlsx')





