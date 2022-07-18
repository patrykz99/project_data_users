#imported from other file
import functions_to_main as ftm


if __name__ == "__main__":


        req1 = ftm.request_and_json_from_site('https://jsonplaceholder.typicode.com/todos', 'jsonDatesTasks.json')
        corrected_dict = ftm.creating_dic_id_correct_tasks(req1) # słownik poprawnych odpowiedzi dla odpowiednich id
        list_usersId_best_worst = ftm.creating_list_of_best_usersId(corrected_dict) # krotka z listami
        req2 = ftm.request_and_json_from_site('https://jsonplaceholder.typicode.com/users?', 'jsonDatesUsers.json')
        list_of_users = req2 # lista słowników z informacjami użytkowników

        fileName = str(input('Type a name of file to save users dates:\n')) + '.xlsx' #
        print("\033c") # czyszczenie terminala po wpisaniu nazwy pliku
        ftm.create_xlsx_and_add_dates(list_of_users,corrected_dict, fileName) # plik xlsx z danymi i wykresem
        ftm.display_best_and_worst_usersId(list_usersId_best_worst)






