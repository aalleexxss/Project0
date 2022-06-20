
import mysql.connector
from collections import namedtuple

# shows all available tunings
# GOOD
def show_available_tunings(cursor):
    query = "SELECT tunings.tuning_name, tunings.strings, tunings.tuning, users.user_name, tunings.likes FROM users INNER JOIN tunings ON users.user_id = tunings.user_id;"
    cursor.execute(query)
    tunings = cursor.fetchall()
    print("   Tuning Name          Strings    Tuning                    Uploader             Likes")
    print(" ------------------------------------------------------------------------------------")
    for i in tunings:
        print("| ", buffer_with_space(i[0], 20), buffer_with_space(str(i[1]), 10), buffer_with_space(i[2], 25),
        buffer_with_space(i[3], 20), str(i[4]), " |")
    print(" ------------------------------------------------------------------------------------")

# shows all available scales
# GOOD
def show_available_scales(cursor):
    query = "SELECT scales.scale_name, scales.steps, users.user_name, scales.likes FROM users INNER JOIN scales ON users.user_id = scales.user_id;"
    cursor.execute(query)
    scales = cursor.fetchall()
    print("   Scale Name           Steps        Uploader            Likes")
    print(" ------------------------------------------------------------")
    for i in scales:
        print("| ", buffer_with_space(i[0], 20), buffer_with_space(i[1], 12), buffer_with_space(i[2], 20), str(i[3]), " |")
    print(" ------------------------------------------------------------")

# shows all user data
# GOOD
def show_user_data(cursor):
    query = "SELECT users.user_name AS name, SUM(like_table.likes) AS likes FROM (SELECT scales.user_id AS user, scales.likes AS likes FROM scales UNION ALL SELECT tunings.user_id, tunings.likes FROM tunings) AS like_table RIGHT JOIN users ON users.user_id = like_table.user GROUP BY like_table.user;"
    cursor.execute(query)
    user_data = cursor.fetchall()
    print("   User Name         Total Likes ")
    print(" ------------------------------ ")
    for i in user_data:
        print("| ", buffer_with_space(i[0], 20), buffer_with_space(str(i[1]), 5), " |")
    print(" ------------------------------ ")

# adds spaces until str is total_length
def buffer_with_space(string, total_length):
    return string + " "*(total_length - len(string))

# takes a user name and password
# returns false if no user found, or returns user_id
def get_user_id(cursor, user_name, pswd):
    query = "SELECT users.user_id FROM users WHERE users.user_name=%s AND users.password=%s;"
    val = [user_name, pswd]
    cursor.execute(query, val)
    user_id = cursor.fetchall()
    if len(user_id) == 0:
        return False
    else:
        return user_id[0][0]
    

# adds a new user
def add_user(cursor, conn, user_name, pswd):
    if not get_user_id(cursor, user_name, pswd):
        sql = "INSERT INTO users (user_name, password) VALUES (%s, %s);"
        vals = (user_name, pswd)
        cursor.execute(sql, vals)
        conn.commit()
        return get_user_id(cursor, user_name, pswd)
    else:
        return False

def add_tuning(cursor, conn, user_id):
    tuning_name = input("please enter tuning name -> ")
    if set_tuning(cursor, tuning_name):
        print("I'm sorry, that tuning has already been entered")
        return
    string_number = int(input("please enter the number of strings -> "))

    tuning_notes = []

    for i in range(string_number):
        print("please enter note of ", str(i+1), " string -> ", end="")
        string_note = input()
        tuning_notes.append(string_note)

    tuning_num_list = tuning_to_nums(tuning_notes)
    if not tuning_num_list:
        print("I'm sorry, one or more notes entered are invalid.")
        return

    tuning_as_csv_string = ""
    for i in tuning_num_list:
        tuning_as_csv_string = tuning_as_csv_string + str(i) + ","
    
    tuning_as_csv_string = tuning_as_csv_string[0:len(tuning_as_csv_string)-1]
   
    sql = "INSERT INTO tunings (tuning_name, user_id, tuning, likes, strings) VALUES (%s, %s, %s, %s, %s);"
    vals = [tuning_name, user_id, tuning_as_csv_string, 0, string_number]
    cursor.execute(sql, vals)
    conn.commit()

def add_scale(cursor, conn, user_id):
    scale_name = input("please enter scale name -> ")
    if set_scale(cursor, scale_name):
        print("I'm sorry, that scale has already been entered")
        return
    steps = input("please enter steps -> ")
    sql = "INSERT INTO scales (scale_name, user_id, steps, likes) VALUES (%s, %s, %s, %s)"
    vals = [scale_name, user_id, steps, 0]
    cursor.execute(sql, vals)
    conn.commit()

def show_users_tunings(cursor, user_id):
    sql = "SELECT * FROM tunings WHERE user_id=%s;"
    val = [user_id]
    cursor.execute(sql, val)
    my_tunings = cursor.fetchall()
    print("  Tuning name         Likes ")
    print(" -------------------------- ")
    for i in my_tunings:
        print("| ", buffer_with_space(i[1], 20), str(i[4]), " |")
    print(" -------------------------- ")

# shows all the scales of a user
def show_users_scales(cursor, user_id):
    sql = "SELECT * FROM scales WHERE user_id=%s;"
    val = [user_id]
    cursor.execute(sql, val)
    my_scales = cursor.fetchall()
    print("   Scales             Likes")
    print(" -------------------------- ")
    for i in my_scales:
        print("| ", buffer_with_space(i[1], 20), str(i[4]), " |")
    print(" ------------------------- ")

def delete_tuning(cursor, conn, user_id):
    tuning_name = input("enter the name of the tuning to delete -> ")
    tuning_check = set_tuning(cursor, tuning_name)
    if not tuning_check or tuning_check[1] != user_id:
        print("no tuning with that name was found")
        return
    sql = "DELETE FROM tunings WHERE tunings.tuning_name=%s AND tunings.user_id=%s"
    vals = [tuning_name, user_id]
    cursor.execute(sql, vals)
    conn.commit()

def delete_scale(cursor, conn, user_id):
    scale_name = input("enter the name of the scale to delete -> ")
    scale_check = set_scale(cursor, scale_name)
    if not scale_check or scale_check[1] != user_id:
        print("no scale with that name was found")
        return
    sql = "DELETE FROM scales WHERE scales.scale_name=%s AND scales.user_id=%s"
    vals = [scale_name, user_id]
    cursor.execute(sql, vals)
    conn.commit()

def rename_tuning(cursor, conn, user_id):
    old_name = input("enter the tuning you would like to rename -> ")
    tuning_check = set_tuning(cursor, old_name)
    if not tuning_check or tuning_check[1] != user_id:
        print("no tuning with that name was found")
        return
    new_name = input("enter the new name of the tuning -> ")
    sql = "UPDATE tunings SET tuning_name=%s WHERE tuning_name=%s AND tunings.user_id=%s"
    vals = [new_name, old_name, user_id]
    cursor.execute(sql, vals)
    conn.commit()

def rename_scale(cursor, conn, user_id):
    old_name = input("enter the scale you would like to rename -> ")
    scale_check = set_scale(cursor, old_name)
    if not scale_check or scale_check[1] != user_id:
        print("no tuning with that name was found.")
        return
    new_name = input("enter the new name of the scale -> ")
    sql = "UPDATE scales SET scale_name=%s WHERE scale_name=%s AND scales.user_id=%s"
    vals = [new_name, old_name, user_id]
    cursor.execute(sql, vals)
    conn.commit()

def set_tuning(cursor, tuning_name):
    sql = "SELECT tuning, user_id FROM tunings WHERE tuning_name=%s"
    val = [tuning_name]
    cursor.execute(sql, val)
    tuning = cursor.fetchall()
    if len(tuning) == 0:
        return False
    else:
        return tuning

def set_scale(cursor, scale_name):
    sql = "SELECT steps, user_id FROM scales WHERE scale_name=%s"
    val = [scale_name]
    cursor.execute(sql, val)
    scale = cursor.fetchall()
    if len(scale) == 0:
        return False
    else:
        return scale

def tuning_to_nums(notes):
    nums = []
    for i in notes:
        if i in notesToNum.keys():
            nums.append(notesToNum[i])
        elif isinstance(i, int):
            if i <= 12 and i >= 1:
                nums.append(i)
        else:
            return False
    return nums

def tuning_to_notes(nums):
    notes = []
    for i in nums:
        if i in numsToNotes.keys():
            notes.append(numsToNotes[i])
        elif isinstance(i, str):
            if i in notesToNum.keys():
                notes.append(numsToNotes[notesToNum[i]])
        else:
            return False
    return notes


# class for session data
class SessionData:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host = "127.0.0.1",
            user = "Alex",
            password = "Revature-P0",
            database = "Project1"
        )
        self.cursor = self.connection.cursor()

    def set_id(self, id):
        self.id = id

    def set_scale(self, scale):
        self.current_scale = scale
    
    def set_tuning(self, tuning):
        self.current_tuning = tuning


notesToNum = {
    "a": 1,
    "a#": 2,
    "bb": 2,
    "b": 3,
    "c": 4,
    "c#": 5,
    "db": 5,
    "d": 6,
    "d#": 7,
    "eb": 7,
    "e": 8,
    "f": 9,
    "f#": 10,
    "gb": 10,
    "g": 11,
    "g#": 12,
    "ab": 12
}

numsToNotes = {
    1: "a",
    2: "a#",
    3: "b",
    4: "c",
    5: "c#",
    6: "d",
    7: "d#",
    8: "e",
    9: "f",
    10: "f#",
    11: "g",
    12: "g#"
}

TuningTuple = namedtuple("TuningTuple", "name uploader notes numbers strings")
standard = TuningTuple("standard", "Alex", ['a',5,'c','d',1,'f'],[1,2,3,4,5,6], 6)

print(tuning_to_notes(standard.notes))

session = SessionData()

session.set_id(4)
add_tuning(session.cursor, session.connection, session.id)

# print(add_user(session.cursor, session.connection, "joe", "123"))

# print("Welcome to Tunings and Scales!")
# print("Please enter \"L\" to log in or \"S\" to sign up.")
# choice = input("-> ").upper()
# while choice != "L" and choice != "S":
#     print("Sorry, your choice is not recognized.")
#     print("please enter \"L\" to log in or \"S\" to sign up.")
#     choice = input("-> ").upper()

# if choice == "L":
#     while True: 
#         print("Please enter username")
#         user = input("-> ")
#         print("Please enter your password")
#         password = input("-> ")
#         user_id = get_user_id(session.cursor, user, password)
#         if user_id:
#             session.set_id(user_id)
#             break
#         else:
#             print("Incorrect or user name or password. please try again")

# elif choice == "S":
#     while True:
#         print("Select a user name")
#         user = input("-> ")
#         print("Select a password")
#         password = input("-> ")
#         user_id = add_user(session.cursor, session.connection, user, password)
#         if user_id:
#             session.set_id(user_id)
#             break
#         else:
#             print("User name is already taken. Please try again.")

# option = ""
# while option != "Q":
#     print("Options: ")
#     print("\"VT\" to view all tunings")
#     print("\"VS\" to view all scales")
#     print("\"VU\" to view all users")
#     print("\"ET\" to enter a new tuning")
#     print("\"ES\" to enter a new scale")
#     print("\"MT\" to view your tunings")
#     print("\"MS\" to view your scales")
#     print("\"ST\" to set a tuning")
#     print("\"SS\" to set a scale")
#     print("\"RT\" to rename one of your tunings")
#     print("\"RS\" to rename one of your scales")
#     print("\"DT\" to delete one of your tunings")
#     print("\"DS\" to delete one of your scales")
#     print("\"Q\" to quit")
#     option = input("-> ").upper()

#     if option == "VT":
#         print("in VT")
#         show_available_tunings(session.cursor)

#     elif option == "VS":
#         show_available_scales(session.cursor)

#     elif option == "VU":
#         show_user_data(session.cursor)

#     elif option == "ET":
#         add_tuning(session.cursor, session.connection, session.id)

#     elif option == "ES":
#         add_scale(session.cursor, session.connection, session.id)

#     elif option == "MT":
#         show_users_tunings(session.cursor, session.id)

#     elif option == "MS":
#         show_users_scales(session.cursor, session.id)

#     elif option == "ST":
#         tuning_name = input("Please enter tuning name -> ")
#         set_tuning(session.cursor, tuning_name)

#     elif option == "SS":
#         scale_name = input("Please enter scale name -> ")
#         set_scale(session.cursor, scale_name)

#     elif option == "RT":
#         rename_tuning(session.cursor, session.connection, session.id)

#     elif option == "RS":
#         rename_scale(session.cursor, session.connection, session.id)

#     elif option == "DT":
#         delete_tuning(session.cursor, session.connection, session.id)

#     elif option == "DS":
#         delete_scale(session.cursor, session.connection, session.id)


