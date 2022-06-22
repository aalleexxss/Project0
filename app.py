
import mysql.connector
from collections import namedtuple
import csv

# shows all available tunings
# GOOD
def show_available_tunings(cursor):
    query = "SELECT tunings.tuning_name, tunings.strings, tunings.tuning, users.user_name, COUNT(tuning_likes.like_id) FROM tunings LEFT JOIN users ON tunings.user_id = users.user_id LEFT JOIN tuning_likes ON tuning_likes.tuning_id = tunings.tuning_id GROUP BY tunings.tuning_id;"
    cursor.execute(query)
    tunings = cursor.fetchall()
    print("   Tuning Name          Strings    Tuning                    Uploader             Likes")
    print(" ------------------------------------------------------------------------------------")
    for i in tunings:
        tuning_as_notes_list = [numsToNotes[int(x)] for x in i[2].split(",")]
        tuning  = "".join(x+"," for x in tuning_as_notes_list)
        print("| ", buffer_with_space(i[0], 20), buffer_with_space(str(i[1]), 10), buffer_with_space(tuning, 25),
        buffer_with_space(i[3], 20), str(i[4]), " |")
    print(" ------------------------------------------------------------------------------------")

# shows all available scales
# GOOD
def show_available_scales(cursor):
    query = "SELECT scales.scale_name, scales.steps, users.user_name, COUNT(scale_likes.like_id) FROM scales LEFT JOIN users ON scales.user_id = users.user_id LEFT JOIN scale_likes ON scale_likes.scale_id = scales.scale_id GROUP BY scales.scale_id;"
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
    query = "SELECT users.user_name AS name, COUNT(uploader_id) AS likes FROM users JOIN (SELECT uploader_id FROM tuning_likes UNION ALL SELECT uploader_id FROM scale_likes) AS like_table ON like_table.uploader_id=users.user_id GROUP BY uploader_id;"
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
# GOOD after quick test
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
# GOOD after quick test
def add_user(cursor, conn, user_name, pswd):
    if not get_user_id(cursor, user_name, pswd):
        sql = "INSERT INTO users (user_name, password) VALUES (%s, %s);"
        vals = (user_name, pswd)
        cursor.execute(sql, vals)
        conn.commit()
        return get_user_id(cursor, user_name, pswd)
    else:
        return False

# gets user input for each string note of a tuning. can use numbers or notes.
# inserts into tunings with tuning as csv string.
# GOOD
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
   
    sql = "INSERT INTO tunings (tuning_name, user_id, tuning, strings) VALUES (%s, %s, %s, %s);"
    vals = [tuning_name, user_id, tuning_as_csv_string, string_number]
    cursor.execute(sql, vals)
    conn.commit()

# gets input from user for steps of a scale. only accepts numbers
# inserts into scales with steps as csv string
# GOOD
def add_scale(cursor, conn, user_id):
    scale_name = input("please enter scale name -> ")
    if set_scale(cursor, scale_name):
        print("I'm sorry, that scale has already been entered")
        return
    print("Please enter the sequence of half steps in your scale, starting from the root.")
    print("enter \"Q\" when you're done.")
    steps_as_list = []
    while True: 
        step = input("->")
        if step.upper() == "Q":
            break
        if step.isdigit():
            steps_as_list.append(step)
        else:
            print("sorry, steps must be entered as a number")
            return

    steps_as_string = ""
    for i in steps_as_list:
        steps_as_string = steps_as_string + str(i) + ","

    steps_as_string = steps_as_string[0:len(steps_as_string)-1]

    sql = "INSERT INTO scales (scale_name, user_id, steps) VALUES (%s, %s, %s)"
    vals = [scale_name, user_id, steps_as_string]
    cursor.execute(sql, vals)
    conn.commit()

# shows all tunings of a user
# GOOD
def show_users_tunings(cursor, user_id):
    sql = "SELECT tunings.tuning_name, COUNT(tuning_likes.like_id) FROM tunings LEFT JOIN tuning_likes ON tuning_likes.tuning_id = tunings.tuning_id WHERE tunings.user_id=%s GROUP BY tunings.tuning_id;"
    val = [user_id]
    cursor.execute(sql, val)
    my_tunings = cursor.fetchall()
    print("  Tuning name         Likes ")
    print(" -------------------------- ")
    for i in my_tunings:
        print("| ", buffer_with_space(i[0], 20), str(i[1]), " |")
    print(" -------------------------- ")

# shows all the scales of a user
# GOOD
def show_users_scales(cursor, user_id):
    sql = "SELECT scales.scale_name, COUNT(scale_likes.like_id) FROM scales LEFT JOIN scale_likes ON scale_likes.scale_id = scales.scale_id WHERE scales.user_id=%s GROUP BY scales.scale_id;"
    val = [user_id]
    cursor.execute(sql, val)
    my_scales = cursor.fetchall()
    print("   Scales             Likes")
    print(" -------------------------- ")
    for i in my_scales:
        print("| ", buffer_with_space(i[0], 20), str(i[1]), " |")
    print(" ------------------------- ")

# GOOD
def delete_tuning(cursor, conn, user_id):
    tuning_name = input("enter the name of the tuning to delete -> ")
    tuning_check = set_tuning(cursor, tuning_name)
    if not tuning_check:
        print("no tuning with that name was found")
        return
    sql = "DELETE FROM tunings WHERE tunings.tuning_name=%s AND tunings.user_id=%s"
    vals = [tuning_name, user_id]
    cursor.execute(sql, vals)
    conn.commit()

# GOOD
def delete_scale(cursor, conn, user_id):
    scale_name = input("enter the name of the scale to delete -> ")
    scale_check = set_scale(cursor, scale_name)
    if not scale_check:
        print("no scale with that name was found")
        return
    sql = "DELETE FROM scales WHERE scales.scale_name=%s AND scales.user_id=%s"
    vals = [scale_name, user_id]
    cursor.execute(sql, vals)
    conn.commit()

# GOOD
def rename_tuning(cursor, conn, user_id):
    old_name = input("enter the tuning you would like to rename -> ")
    tuning_check = set_tuning(cursor, old_name)
    if not tuning_check:
        print("no tuning with that name was found")
        return
    new_name = input("enter the new name of the tuning -> ")
    sql = "UPDATE tunings SET tuning_name=%s WHERE tuning_name=%s AND tunings.user_id=%s"
    vals = [new_name, old_name, user_id]
    cursor.execute(sql, vals)
    conn.commit()

# GOOD
def rename_scale(cursor, conn, user_id):
    old_name = input("enter the scale you would like to rename -> ")
    scale_check = set_scale(cursor, old_name)
    if not scale_check:
        print("no tuning with that name was found.")
        return
    new_name = input("enter the new name of the scale -> ")
    sql = "UPDATE scales SET scale_name=%s WHERE scale_name=%s AND scales.user_id=%s"
    vals = [new_name, old_name, user_id]
    cursor.execute(sql, vals)
    conn.commit()

# takes a tuning name and returns named tuple of tuning
# GOOD
def set_tuning(cursor, tuning_name):
    sql = "SELECT tunings.tuning_name, users.user_name, tunings.tuning, tunings.strings FROM tunings JOIN users ON tunings.user_id = users.user_id WHERE tunings.tuning_name = %s;"
    val = [tuning_name]
    cursor.execute(sql, val)
    tuning = cursor.fetchall()
    if len(tuning) == 0:
        return False
    else:
        num_list = [int(x) for x in tuning[0][2].split(",")]
        note_list = tuning_to_notes(tuning[0][2].split(","))
        tuning_data = TuningTuple(tuning[0][0], tuning[0][1], note_list, num_list, tuning[0][3])
        return tuning_data

# takes scale name and returns named tuple of scale 
# GOOD
def set_scale(cursor, scale_name):
    sql = "SELECT scales.scale_name, users.user_name, scales.steps FROM scales JOIN users ON scales.user_id=users.user_id WHERE scale_name=%s"
    val = [scale_name]
    cursor.execute(sql, val)
    scale = cursor.fetchall()
    if len(scale) == 0:
        return False
    else:
        steps_as_nums = [int(x) for x in scale[0][2].split(",")]
        scale_data = ScaleTuple(scale[0][0], scale[0][1], steps_as_nums)
        return scale_data

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
        if int(i) in numsToNotes.keys():
            notes.append(numsToNotes[int(i)])
        else:
            return False
    return notes

def generate_fretboard(tuning_array):
    fretboard_array = [[]]
    for i in tuning_array:
        fretboard_array[0].append(i)
    for i in range(14):
        temp = [(j % 12)+1 for j in fretboard_array[i]]
        fretboard_array.append(temp)
    return fretboard_array

def print_board(board):
    fret_num = 0
    for i in board:
        print(buffer_with_space(str(fret_num), 2), "- |", end="")
        for j in i:
            if j != 0:
                print(buffer_with_space(numsToNotes[j], 2), "|", end="")
            else:
                print("   |", end="")
        print()
        print("     -------------------------")
        fret_num += 1

def get_notes_in_key(key, scale_steps):
    if key not in notesToNum.keys():
        print("I'm sorry, that key is invalid")
        return
    scale_nums = [notesToNum[key]]
    for i in range(len(scale_steps)):
        previous_num_in_scale = scale_nums[i]
        next_number = previous_num_in_scale + scale_steps[i]
        corrected_num = (next_number%13) + (next_number//13)
        scale_nums.append(corrected_num)
    return scale_nums

def generate_scale_board(scale_nums, board):
    scale_board = [[]]
    for i in range(len(board)):
        if i > 0:
            scale_board.append([])
        for j in range(len(board[i])):
            if board[i][j] in scale_nums:
                scale_board[i].append(board[i][j])
            else:
                scale_board[i].append(0)
    return scale_board

def add_tunings_from_csv(cursor, conn, user_id, file_name):
    with open(file_name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            sql = "INSERT INTO tunings (tuning_name, user_id, tuning, strings) VALUES (%s, %s, %s, %s);"
            vals = [row[0], user_id, row[1], row[2]]
            cursor.execute(sql, vals)
        conn.commit()
    csv_file.close()

def like_tuning(cursor, conn, user_id):
    tuning_name = input("please enter the name of tuning to like -> ")
    sql = "SELECT tuning_id, user_id FROM tunings WHERE tuning_name = %s"
    val = [tuning_name]
    cursor.execute(sql, val)
    tuning_id = cursor.fetchall()
    if len(tuning_id) == 0:
        print("I'm sorry, no tuning with that name was found.")
        return
    else:
        uploader_id = tuning_id[0][1]
        tuning_id = tuning_id[0][0]
    sql = "SELECT like_id FROM tuning_likes WHERE user_id=%s AND tuning_id=%s;"
    vals = [user_id, tuning_id]
    cursor.execute(sql, vals)
    like_id = cursor.fetchall()
    if len(like_id) != 0:
        print("I'm sorry, you've already liked that tuning")
        return
    sql = "INSERT INTO tuning_likes (user_id, uploader_id, tuning_id) VALUES (%s, %s, %s);"
    vals = [user_id, uploader_id, tuning_id]
    cursor.execute(sql, vals)
    conn.commit()

def like_scale(cursor, conn, user_id):
    scale_name = input("please enter the name of the scale to like -> ")
    sql = "SELECT scale_id, user_id FROM scales WHERE scale_name = %s"
    val = [scale_name]
    cursor.execute(sql, val)
    scale_id = cursor.fetchall()
    if len(scale_id) == 0:
        print("I'm sorry, no scale with that name was found.")
        return
    else:
        uploader_id = scale_id[0][1]
        scale_id = scale_id[0][0]
    sql = "SELECT like_id FROM scale_likes WHERE user_id=%s AND scale_id=%s"
    vals = [user_id, scale_id]
    cursor.execute(sql, vals)
    like_id = cursor.fetchall()
    if len(like_id) != 0:
        print("I'm sorry, you've already liked that scale")
        return
    sql = "INSERT INTO scale_likes (user_id, uploader_id, scale_id) VALUES (%s, %s, %s)"
    vals = [user_id, uploader_id, scale_id]
    cursor.execute(sql, vals)
    conn.commit()

def scale_to_txt(sess):  
    with open("shapes.txt", "w") as f:
        tuning_string = "Tuning: " + sess.current_tuning.name + "\n"
        scale_string = "Scale: " + sess.current_scale.name + "\n"
        key_string = "Key: " + sess.current_key + "\n\n"
        f.write(tuning_string)
        f.write(scale_string)
        f.write(key_string)

        fret_num = 0
        for i in sess.scale_board:
            write_string = buffer_with_space(str(fret_num), 2) + "- |" 
            for j in i:
                if j != 0:
                    write_string += buffer_with_space(numsToNotes[j], 3) + "|"
                else:
                    write_string += "   |"
            write_string += "\n"
            f.write(write_string)
            f.write("    -------------------------\n")
            fret_num += 1
    f.close()


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
        self.tuning_set = False
        self.scale_set = False
        self.key_set = False

    def set_id(self, id):
        self.id = id

    def set_current_scale(self, scale):
        self.current_scale = scale
        self.scale_set = True
    
    def set_current_tuning(self, tuning):
        self.current_tuning = tuning
        self.tuning_set = True

    def set_current_key(self, key):
        self.current_key = key
        self.key_set = True

    def set_notes_in_key(self, notes):
        self.key_notes = notes

    def set_fretboard(self, board):
        self.fretboard = board

    def set_scaleboard(self, scale_board):
        self.scale_board = scale_board

    


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
ScaleTuple = namedtuple("ScaleTuple", "name uploader steps")

session = SessionData()
session.set_id(4)

print("Welcome to Tunings and Scales!")
print("Please enter \"L\" to log in or \"S\" to sign up.")
choice = input("-> ").upper()
while choice != "L" and choice != "S":
    print("Sorry, your choice is not recognized.")
    print("please enter \"L\" to log in or \"S\" to sign up.")
    choice = input("-> ").upper()

if choice == "L":
    while True: 
        print("Please enter username")
        user = input("-> ")
        print("Please enter your password")
        password = input("-> ")
        user_id = get_user_id(session.cursor, user, password)
        if user_id:
            session.set_id(user_id)
            break
        else:
            print("Incorrect or user name or password. please try again")

elif choice == "S":
    while True:
        print("Select a user name")
        user = input("-> ")
        print("Select a password")
        password = input("-> ")
        user_id = add_user(session.cursor, session.connection, user, password)
        if user_id:
            session.set_id(user_id)
            break
        else:
            print("User name is already taken. Please try again.")

option = ""
while option != "Q":
    if session.tuning_set:
        tuning_string =buffer_with_space(session.current_tuning.name, 20)
    else:
        tuning_string = buffer_with_space("no tuning set yet", 20)

    if session.scale_set:
        scale_string = buffer_with_space(session.current_scale.name, 20)
    else:
        scale_string = buffer_with_space("no scale set yet", 20)

    if session.key_set:
        key_string = buffer_with_space(session.current_key, 20)
    else:
        key_string = buffer_with_space("no key set yet", 20)

    print("_____________________________________________________________________")
    print("_____________________________________________________________________")

    print("Info: ")
    print(" ---------------------------------------")
    print("| current tuning: ", tuning_string, "|")
    print("| current scale:  ", scale_string, "|")
    print("| current key:    ", key_string, "|")
    print(" ---------------------------------------")

    print("Options: ")
    print(" -------------------------------------------------------------- ")
    print("| \"VT\" to view all tunings                                     |")
    print("| \"VS\" to view all scales                                      |")
    print("| \"VU\" to view all users                                       |")
    print("| \"ET\" to enter a new tuning                                   |")
    print("| \"ES\" to enter a new scale                                    |")
    print("| \"MT\" to view your tunings                                    |")
    print("| \"MS\" to view your scales                                     |")
    print("| \"ST\" to set a tuning                                         |")
    print("| \"SS\" to set a scale                                          |")
    print("| \"SK\" to set a key                                            |")
    print("| \"RT\" to rename one of your tunings                           |")
    print("| \"RS\" to rename one of your scales                            |")
    print("| \"DT\" to delete one of your tunings                           |")
    print("| \"DS\" to delete one of your scales                            |")
    print("| \"PS\" to print out the selected scale in the selected tuning  |")
    print("| \"TC\" to add tunings from a csv file                          |")
    print("| \"LT\" to like a tuning                                        |")
    print("| \"LS\" to like a scale                                         |")
    print("| \"TXT\" to save the current scale shape as a txt file          |")
    print("| \"Q\" to quit                                                  |")
    print(" -------------------------------------------------------------- ")
    option = input("-> ").upper()

    scale_change = False
    tuning_change = False
    key_change = False

    if option == "VT":
        show_available_tunings(session.cursor)

    elif option == "VS":
        show_available_scales(session.cursor)

    elif option == "VU":
        show_user_data(session.cursor)

    elif option == "ET":
        add_tuning(session.cursor, session.connection, session.id)

    elif option == "ES":
        add_scale(session.cursor, session.connection, session.id)

    elif option == "MT":
        show_users_tunings(session.cursor, session.id)

    elif option == "MS":
        show_users_scales(session.cursor, session.id)

    elif option == "ST":
        tuning_name = input("Please enter tuning name -> ")
        tuning_data = set_tuning(session.cursor, tuning_name)
        session.set_current_tuning(tuning_data)
        tuning_change = True
        
    elif option == "SS":
        scale_name = input("Please enter scale name -> ")
        scale_data = set_scale(session.cursor, scale_name)
        session.set_current_scale(scale_data)
        scale_change = True

    elif option == "SK":
        key = input("Please enter key -> ")
        if key in notesToNum.keys():
            session.set_current_key(key)
            key_change = True
        else:
            print("I'm sorry, that's an invalid key")

    elif option == "RT":
        rename_tuning(session.cursor, session.connection, session.id)

    elif option == "RS":
        rename_scale(session.cursor, session.connection, session.id)

    elif option == "DT":
        delete_tuning(session.cursor, session.connection, session.id)

    elif option == "DS":
        delete_scale(session.cursor, session.connection, session.id)

    elif option == "PS":
        if not session.scale_set:
            print("No scale is currently selected")
            continue
        elif not session.tuning_set:
            print("No tuning is currently selected")
            continue
        elif not session.key_set:
            print("No key is currently selected")
        else:
            session.set_fretboard(generate_fretboard(session.current_tuning.numbers))
            session.set_notes_in_key(get_notes_in_key(session.current_key, session.current_scale.steps))
            session.set_scaleboard(generate_scale_board(session.key_notes, session.fretboard))
            print_board(session.scale_board)

    elif option == "TC":
        file_name = input("Enter name of CSV file -> ")
        add_tunings_from_csv(session.cursor, session.connection, session.id, file_name)

    elif option == "LT":
        like_tuning(session.cursor, session.connection, session.id)

    elif option == "LS":
        like_scale(session.cursor, session.connection, session.id)

    elif option == "TXT":
        if not session.scale_set:
            print("No scale is currently selected")
            continue
        elif not session.tuning_set:
            print("No tuning is currently selected")
            continue
        elif not session.key_set:
            print("No key is currently selected")
        else:
            session.set_fretboard(generate_fretboard(session.current_tuning.numbers))
            session.set_notes_in_key(get_notes_in_key(session.current_key, session.current_scale.steps))
            session.set_scaleboard(generate_scale_board(session.key_notes, session.fretboard))
            scale_to_txt(session)


