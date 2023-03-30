
# ===== Imported Libraries =====

import datetime

# ===== Defined Functions =====

def menu_options():
    
    menu = f"""\033[1mPlease select one of the following options below\033[0m:
r\t - \tRegistering a user
a\t - \tAdding a task
va\t - \tView all tasks
vm\t - \tView my task
e\t - \tExit 
Menu option selected: """

    menu_admin = f"""\033[1mPlease select one of the following options below\033[0m:
r\t - \tRegistering a user
a\t - \tAdding a task
va\t - \tView all tasks
vm\t - \tView my task
gr\t - \tGenerate reports
ds\t - \tDisplay statistics
e\t - \tExit
Menu option selected: """

    if inp_user == "admin":
        menu_choice = input(f"\n{menu_admin}").lower()
    else:
        menu_choice = input(f"\n{menu}").lower()
    return menu_choice

def user_login():
    # Parsing usernames & passwords into dictionary
    login_contents = {}
    with open("user2.txt", "r", encoding = "utf-8") as login_details:
        for line in login_details:
            username, password = line.strip().split(", ")
            login_contents[username] = password

    # Request username & error handle non-existing user  
    inp_user = str(input(f"\033[1mPlease enter your username\033[0m: "))
    while inp_user not in login_contents.keys():
        print(f"\033[0;31mUnfortunately {inp_user} does not have an account, please check the spelling or enter another username\033[0m")
        inp_user = str(input(f"\n\033[1mPlease enter another username\033[0m: "))

    # Request password & error handle mismatching password
    inp_password = str(input(f"\n\033[1mPlease enter your password\033[0m: "))
    while inp_password != login_contents.get(inp_user):
        print(f"\033[0;31mThe password you have entered does not match our records, please check the spelling and try again\033[0m")
        inp_password = str(input(f"\n\033[1mPlease try again, enter the password for this account:\033[0m "))
    
    return inp_user

def reg_user():
    # Parsing usernames & passwords from users2.txt into dictionary
    login_contents = {}
    with open("user2.txt", "r", encoding = "utf-8") as login_details:
        for line in login_details:
            username, password = line.strip().split(", ")
            login_contents[username] = password

    # if user is admin, request username
    if inp_user != "admin":
        print(f"\n\033[0;31mHello {inp_user}, unfortunately you are not authorised to register new users, please contact the administrator\033[0m")
    else:
        new_username = input("\n\033[1mPlease enter a new username\033[0m: ")

        # Error handle pre-existing user and mismatching passwords scenarios, else add to users2.txt
        if new_username in login_contents.keys():
            print(f"\n\033[0;31mThe username {new_username} already exists, please enter another username\033[0m")
        else:
            new_password = input("\n\033[1mPlease enter a new password\033[0m: ")
            confirm_password = input("\n\033[1mPlease re-enter password to confirm\033[0m: ")
            if new_password != confirm_password:
                    print(f"\n\033[0;31mThe passwords you have entered do not match, an account for this user cannot be created\033[0m")
            else:
                with open("user2.txt", "a", encoding = "utf-8") as login_details:
                    login_details.write(f"\n{new_username}, {new_password}")
                    print(f"\n\033[0;32mThank you for registering {new_username}, an account for them has now been created!\033[0m")

def add_task():
    # request user inputs for task details
    task_assignee = input(f"\033[1mPlease enter the username of the person to whom the task is assigned\033[0m: ")
    task_title = input(f"\033[1mPlease enter the task title\033[0m: ")
    task_description = input(f"\033[1mPlease enter the task description\033[0m: ")
    task_due_date = datetime.datetime.strptime(input(f"\033[1mPlease enter the due date of the task as DD/MM/YYYY\033[0m: "), "%d/%m/%Y").strftime("%d %b %Y")
    task_assigned_date = datetime.date.today().strftime("%d %b %Y")
    task_completed = "No"

    # write inputs into tasks.txt in set order
    with open("tasks.txt", "a", encoding = "utf-8") as task_list:
        task_list.write(f"\n{task_assignee}, {task_title}, {task_description}, {task_assigned_date}, {task_due_date}, {task_completed}")

def view_all_tasks():
    # Extract tasks.txt content & print in set format
    with open("tasks2.txt", "r", encoding = "utf-8") as task_list:
        contents = task_list.readlines()
        for line in contents:
            split_line = line.strip().split(", ")
            print(f"\nTask:\t\t\t{split_line[1]}\nAssigned to:\t\t{split_line[0]}\nDate assigned:\t\t{split_line[3]}\nDue date:\t\t{split_line[4]}\nTask Complete?:\t\t{split_line[5]}\nTask description:\n{split_line[2]}")

def view_my_tasks():
    # Parse task2.txt contents into dictionary (for numbering each task) & create empty list (for list of assignees) and updated dictionary (for edited tasks)
    task_dict = {}
    assignees = []
    updated_task_dict = {}

    with open("tasks2.txt", "r", encoding = "utf-8") as task_list:
        contents = task_list.readlines()
        for number, line in enumerate(contents,1):
            split_line = line.strip().split(", ")
            task_dict[number] = split_line
            assignees.append(split_line[0])

            # print tasks where user is assignee
            if inp_user != split_line[0]:
                continue
            else:
                print(f"""\n
---------- Task no. {number}\n 
Task:\t\t\t{split_line[1]}
Assigned to:\t\t{split_line[0]}
Date assigned:\t\t{split_line[3]}
Due date:\t\t{split_line[4]}
Task Complete?:\t\t{split_line[5]}
Task description:\t{split_line[2]}
\n----------""")

    # sub-menu to 'change completion state', 'edit task', or to 'return to main menu'
    if inp_user in assignees:
        task_chosen = int(input(f"\nPlease enter the number of the task you wish to edit (or enter '-1' to return to the Main Menu)\nTask selected: "))
        if task_chosen == -1:
            menu_options()
        else:
            edit_choice = int(input(f"""
\nWhat would you like to do with this task?
1\t-\tMark the task as 'Completed'
2\t-\tEdit the task
Action selected: """))
            if edit_choice == 1:
                task_dict[task_chosen][-1] = 'Yes' # list
                updated_task_dict = (", ".join(task) for task in task_dict.values()) # string, separated with commas

            # if 'edit task' selected, sub menu to 'modify assignee' or 'modify due date' with preliminary task completion state check
            elif edit_choice == 2 and task_dict[task_chosen][-1] != 'No':
                print(f"This task can no longer be edited as it has been completed")
                task_chosen = int(input(f"\nPlease enter the number of the task you wish to edit (or enter '-1' to return to the Main Menu)\nTask selected: "))
            elif edit_choice == 2 and task_dict[task_chosen][-1] != 'Yes':
                modify_choice = int(input(f"""
\nWhich edit would you like to make to the task?
1\t-\tModify the task's assignee
2\t-\tModify the task's due date
Edit selected: """)) 
                if modify_choice == 1:
                    task_dict[task_chosen][0] = input(f"To whom is this task to be assigned to instead of \'{task_dict[task_chosen][0]}\'? ")
                    updated_task_dict = (", ".join(task) for task in task_dict.values()) # string, separated with commas
                
                # Error handle incorrect date format & date before today
                elif modify_choice == 2:
                    try:
                        task_dict[task_chosen][4] = datetime.datetime.strptime(input(f"\nPlease enter the new due date, using the format DD/MM/YYYY, for this task: "), "%d/%m/%Y").strftime("%d %b %Y")
                        print(f"You have successfully changed the due date for this task!")
                        updated_task_dict = (", ".join(task) for task in task_dict.values()) # string, separated with commas
                        if task_dict[task_chosen][4] < datetime.date.today().strftime("%d %b %Y"):
                            print(f"You have entered a due date before today's date, please try again")
                            task_dict[task_chosen][4] = datetime.datetime.strptime(input(f"\nPlease enter the new due date, using the format DD/MM/YYYY, for this task: "), "%d/%m/%Y").strftime("%d %b %Y")
                    except ValueError:
                        print(f"You have entered a due date in an incorrect format, please try again")
                        task_dict[task_chosen][4] = datetime.datetime.strptime(input(f"\nPlease enter the new due date, using the format DD/MM/YYYY, for this task: "), "%d/%m/%Y").strftime("%d %b %Y")
                else:
                    print(f"You have selected an option that doesn't exist")
            else:
                print(f"You have selected an option that doesn't exist")
                task_chosen = int(input(f"\nPlease enter the number of the task you wish to edit (or enter '-1' to return to the Main Menu):\n"))
        with open("tasks2.txt", "w+", encoding = "utf-8") as task_list:
            task_list.write("\n".join(updated_task_dict))
    else:
        print(f"\nYou do not have any assigned tasks")

# Used the following resource to understand how to implement error handling:
# (URL:https://docs.python.org/3/tutorial/errors.html)

def gen_reports():
        # Parse contents of users2.txt & populate list of all registered users 
        users = []

        with open("user2.txt", "r", encoding = "utf-8") as user_list:
            user_contents = user_list.readlines()
            for line in user_contents:
                user_split_line = line.strip().split(", ")
                users.append(user_split_line[0])
        
        # Create empty dictionaries to store count of each group of tasks by user
        completed_dict = {}
        incomplete_dict = {}
        incomplete_due_dict = {}

        user_breakdown = ""

        for user in users:
            completed_dict[user] = 0
            incomplete_dict[user] = 0
            incomplete_due_dict[user] = 0

        # Parse contents of tasks2.txt, split out each section & tally totals per user
        with open("tasks2.txt", "r", encoding = "utf-8") as task_list:
            task_contents = task_list.readlines()

            total_tasks = int(len(task_contents))
            task_completed = int(0)
            task_incomplete = int(0)
            task_incomplete_due = int(0)

            for line in task_contents:
                task_split_line = line.strip().split(", ")
                due_date = datetime.datetime.strptime(task_split_line[4], "%d %b %Y")
                current_date = datetime.datetime.today()
                completion_status = task_split_line[5]
                task_assignee = task_split_line[0]

                if completion_status == 'Yes':
                    completed_dict[task_assignee] = completed_dict.setdefault(task_assignee, 0) + 1
                    task_completed += 1
                elif completion_status == 'No':
                    incomplete_dict[task_assignee] = incomplete_dict.setdefault(task_assignee, 0) + 1
                    task_incomplete += 1
                    if current_date > due_date:
                        incomplete_due_dict[task_assignee] = incomplete_due_dict.setdefault(task_assignee, 0) + 1
                        task_incomplete_due += 1

        # calculate and format user & task data, Error handle users with no tasks & write in outputs into respective txt files
        for user in users:
            try:
                user_breakdown += (f"""---------- {user}'s Task Report\n
Of all tasks:
- Number assigned to user:              {completed_dict[user] + incomplete_dict[user]}
- Percentage assigned to user:          {"{:.2%}".format((completed_dict[user] + incomplete_dict[user]) / total_tasks)}\n
Of {user}'s tasks:
- Percentage complete:                  {"{:.2%}".format(completed_dict[user] / (completed_dict[user] + incomplete_dict[user]))}
- Percentage incomplete:                {"{:.2%}".format(incomplete_dict[user] / (completed_dict[user] + incomplete_dict[user]))}
- Percentage incomplete & overdue:      {"{:.2%}".format(incomplete_due_dict[user] / (completed_dict[user] + incomplete_dict[user]))}\n
---------------------------------------------------
\n""")
            except ZeroDivisionError:
                user_breakdown += (f"""---------- {user}'s Task Report\n
Of all tasks:
- Number assigned to user:              None
- Percentage assigned to user:          None\n
Of {user}'s tasks:
- Percentage complete:                  None
- Percentage incomplete:                None
- Percentage incomplete & overdue:      None\n
---------------------------------------------------
\n""")

        with open("task_overview.txt", "w+", encoding = "utf-8") as task_overview:
            task_overview.write(f"""\t---------- Overall Task Report ----------\n
Total number of tasks:              {total_tasks}
- of which complete                 {task_completed}
- of which incomplete               {task_incomplete}
- of which incomplete & overdue     {task_incomplete_due}\n
Percentage of incomplete tasks:     {"{:.2%}".format(task_incomplete / total_tasks)}
Percentage of overdue tasks:        {"{:.2%}".format(task_incomplete_due / total_tasks)}\n
---------------------------------------------------""")

        with open("user_overview.txt", "w+", encoding = "utf-8") as user_overview:
            user_overview.write(user_breakdown)

# Used this resource to understand how to format a float into a percentage:
# (URL: https://www.w3resource.com/python-exercises/string/python-data-type-string-exercise-36.php)

# Used this resource to understand how to group/sum values per dictionary key:
# (URL: https://stackoverflow.com/questions/3483520/use-cases-for-the-setdefault-dict-method)

def disp_stats():

    gen_reports()
    with open("task_overview.txt", "r", encoding = "utf-8") as task_overview:
        t_contents = task_overview.read()
    
    with open("user_overview.txt", "r", encoding = "utf-8") as user_overview:
        u_contents = user_overview.read()

    print(t_contents)
    print(u_contents)

# =========== Main Body ===========

login_contents = {}
task_dict = {}

inp_user = user_login()

while True:
    menu_choice = menu_options()
    if menu_choice == 'r':
        reg_user()
    elif menu_choice == 'a':
        add_task()
    elif menu_choice == 'va':
        view_all_tasks()
    elif menu_choice == 'vm':
        view_my_tasks()
    elif menu_choice == 'gr':
        gen_reports()
    elif menu_choice == 'ds':
        disp_stats()
    elif menu_choice == 'e':
        print('Goodbye!!!')
        exit()
    else:
        print("You have selected an option that does not exist, please try again")
        menu_choice = menu_options()
