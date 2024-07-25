"""This module is a Capstone Project for Python for Data Science.

It handles user authentication, task management, and viewing tasks.
"""

# 2024/07/17 Reviewed 2024/07/19
# 1 - Python for Data Science (L1T15)
# Capstone Project - Files by Kriste Alberts

# ====importing libraries====
from datetime import datetime
import sys

# ====Login Section====


def validate_username(username, user_dictionary):
    """Validate the username by checking if it exists in the stored data."""
    return username in user_dictionary


def validate_password(username, password, user_dictionary):
    """Valide the password by checking if it matches the username."""
    return user_dictionary.get(username) == password


def read_user_data():
    """Read usernames and passwords from user.txt file."""
    user_dictionary = {}
    with open('user.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split(', ')
            user_dictionary[username] = password
    # Returns a dictionary with usernames as keys and passwords as values
    return user_dictionary


def login(user_data):
    """Handle the login process."""
    while True:
        # Prompt the user to enter their username
        username = input("Please enter your username: ").strip().lower()
        # Use a nested loop to validate username and password seperately
        if validate_username(username, user_data):
            while True:
                # Prompt the user to enter their password
                password = input("Please enter your password: ").strip()
                # Validate the entered password
                if validate_password(username, password, user_data):
                    print("Login successful!")
                    return username  # Exit the function if login is successful
                else:
                    print("Invalid password. Please try again.")
        else:
            print("Invalid username. Please try again.")

def count_users_and_tasks():
    """Count and display the total number of users and tasks."""
    with open('user.txt', 'r') as user_file:
        total_users = sum(1 for _ in user_file)
    with open('tasks.txt', 'r') as task_file:
        total_tasks = sum(1 for _ in task_file)
    print(f"\nTotal number of users: {total_users}")
    print(f"Total number of tasks: {total_tasks}")
    print(f"---------------------------")

# Read user data from user.txt
user_data = read_user_data()


# Start the login process
logged_in_user = login(user_data)


while True:
    # Present the menu to the user
    if logged_in_user == 'admin':
        menu = input(
            "Please select one of the following options: \n"
            "r - register a user \n"
            "a - add task \n"
            "va - view all tasks \n"
            "vm - view my tasks \n"
            "ds - display statistics \n"
            "e - exit: "
        ).lower()  # Make sure that the user input is converted to lower case
    else:
        menu = input(
            "Please select one of the following options: \n"
            "a - add task \n"
            "va - view all tasks \n"
            "vm - view my tasks \n"
            "e - exit: "
        ).lower()  # Make sure that the user input is converted to lower case

    if menu == 'r'and logged_in_user == 'admin':
        new_user = input(
                "Please enter username for new user: ").strip().lower()
        while True:
            new_password = input(
                        "Please enter password for new user: ").strip()
            new_password_confirmation = input(
                                    "Please enter password again for \
confirmation: ")
            # Nested if for checking password
            if new_password == new_password_confirmation:
                with open("user.txt", 'a+') as file:
                    file.seek(0)  # Move pointer to the beginning of the file
                    lines = file.read()  # Read the entire file contents
                    # Check if the file ends with a newline
                    if not lines.endswith('\n'):
                        file.write('\n')  # If not, write a newline
                    # Append the new user data
                    file.write(f"{new_user}, {new_password}\n")
                    print("New user has been added successfully.")
                # Reload user data to include the new user for following tasks
                user_data = read_user_data()
                break  # Exit the loop after successful registration
            else:
                print("Passwords do not match. Please try again.")

    elif menu == 'a':
        while True:
            username_for_task_completion = input(
                                        "Please enter the username of \
the person to whom the task is assigned to: ").strip().lower()
            # Check if the username exists in the user data
            if username_for_task_completion in user_data:
                break  # Exit the loop if the username is valid
            else:
                print("The username does not exist. Please try again.")
        title_of_task = input("Please enter the title of the task: ").strip()
        description_of_task = input(
                            "Please enter the description of the task: "
                            ).strip()
        while True:
            task_due_date_input = input(
                                "Please enter the date on which the \
task is due (DD MMM YYYY): ").strip()
            try:
                task_due_date = datetime.strptime(
                    task_due_date_input, "%d %b %Y").strftime("%d %b %Y")
                break
            except ValueError:
                print(
                    "Invalid date format. Please enter the date in \
'DD MMM YYYY' format.")
        task_completion_status = 'No'
        current_date = datetime.now().strftime("%d %b %Y")
        with open("tasks.txt", 'a+') as file:
            file.seek(0)
            lines = file.read()
            if not lines.endswith('\n'):
                file.write('\n')
            file.write(
                        (f"{username_for_task_completion}, "
                            f"{title_of_task}, "
                            f"{description_of_task}, "
                            f"{current_date}, "
                            f"{task_due_date}, "
                            f"{task_completion_status}\n")
                        )
        print("New task has been added successfully.")

    elif menu == 'va':
        with open("tasks.txt", 'r') as file:
            for line in file:
                task_details = line.strip().split(', ')
                print(f"\nTask:                {task_details[1]}")
                print(f"Assigned to:         {task_details[0]}")
                print(f"Date assigned:       {task_details[3]}")
                print(f"Due date:            {task_details[4]}")
                print(f"Task Complete?       {task_details[5]}")
                print(f"Task description:    {task_details[2]}")
                print("\n-----------------------------------\n")

    elif menu == 'vm':
        with open("tasks.txt", 'r') as file:
            # Flag to check if any tasks were found for the user
            tasks_found = False
            for line in file:
                username_task_details = line.strip().split(', ')
                if username_task_details[0].strip().lower(
                ) == logged_in_user.strip().lower():
                    tasks_found = True
                    print(f"\nTask:             {username_task_details[1]}")
                    print(f"Assigned to:      {username_task_details[0]}")
                    print(f"Date assigned:    {username_task_details[3]}")
                    print(f"Due date:         {username_task_details[4]}")
                    print(f"Task Complete?    {username_task_details[5]}")
                    print(f"Task description  {username_task_details[2]}")
                    print("\n-----------------------------------\n")
            if not tasks_found:
                print(f"No tasks have been assigned to {logged_in_user}")

    elif menu == 'ds' and logged_in_user == 'admin':
        count_users_and_tasks()

    elif menu == 'e':
        print("Exiting the program now. Thank you")
        sys.exit()

    else:
        print("You have entered an invalid input. Please try again")

# END
