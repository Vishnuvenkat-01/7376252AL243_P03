# Project: To-Do List Manager
# Project Number: P03
# Language: Python 3

from datetime import datetime, date, timedelta

FILE_NAME = "tasks.txt"


# Load tasks from file
def load_tasks():
    tasks = []

    try:
        with open(FILE_NAME, "r") as file:
            for line in file:
                line = line.strip()

                if line:
                    fields = line.split("|")

                    if len(fields) == 5:
                        tasks.append(fields)

    except FileNotFoundError:
        # Create the file if it does not exist
        with open(FILE_NAME, "w") as file:
            pass

    return tasks


# Save tasks to file
def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        for task in tasks:
            file.write("|".join(task) + "\n")


# Validate date
def get_valid_date():
    while True:
        due_date = input("Enter due date (DD-MM-YYYY): ").strip()

        try:
            datetime.strptime(due_date, "%d-%m-%Y")
            return due_date

        except ValueError:
            print("Invalid date! Please use DD-MM-YYYY.")


# Display all tasks

def display_tasks(tasks):
    print("\n========== ALL TASKS ==========")

    if not tasks:
        print("No tasks available.")
        return

    for task in tasks:
        print("------------------------------")
        print("Task ID :", task[0])
        print("Title   :", task[1])
        print("Priority:", task[2])
        print("Due Date:", task[3])
        print("Status  :", task[4])


# Display menu
def display_menu():
    print("\n========== TO-DO LIST MANAGER ==========")
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. Edit Task")
    print("4. Delete Task")
    print("5. Mark Task as Completed")
    print("6. View Pending Tasks")
    print("7. View Overdue Tasks")
    print("8. View Upcoming Tasks")
    print("9. View Statistics")
    print("10. Exit")


# Find a task using its ID
def find_task(tasks, task_id):
    for task in tasks:
        if task[0].upper() == task_id.upper():
            return task

    return None


# Add task
def add_task(tasks):
    print("\n========== ADD NEW TASK ==========")

    title = input("Enter task title: ").strip()

    if not title:
        print("Task title cannot be empty!")
        return

    if "|" in title:
        print("Task title cannot contain '|'.")
        return

    while True:
        priority = input(
            "Enter priority (High/Medium/Low): "
        ).strip().capitalize()

        if priority in ["High", "Medium", "Low"]:
            break

        print("Invalid priority! Enter High, Medium, or Low.")

    due_date = get_valid_date()

    # Generate the next task ID
    largest_id = 0

    for task in tasks:
        try:
            number = int(task[0][1:])

            if number > largest_id:
                largest_id = number

        except ValueError:
            continue

    task_id = "T" + str(largest_id + 1).zfill(3)

    new_task = [
        task_id,
        title,
        priority,
        due_date,
        "PENDING"
    ]

    tasks.append(new_task)
    save_tasks(tasks)

    print("\nTask added successfully!")
    print("Task ID:", task_id)


# Edit task
def edit_task(tasks):
    print("\n========== EDIT TASK ==========")

    task_id = input("Enter task ID to edit: ").strip()
    task = find_task(tasks, task_id)

    if task is None:
        print("Task not found!")
        return

    print("Leave a field blank to keep its current value.")

    new_title = input(
        f"Enter new title [{task[1]}]: "
    ).strip()

    if new_title:
        if "|" in new_title:
            print("Task title cannot contain '|'.")
            return

        task[1] = new_title

    new_priority = input(
        f"Enter new priority [{task[2]}] (High/Medium/Low): "
    ).strip().capitalize()

    if new_priority:
        if new_priority not in ["High", "Medium", "Low"]:
            print("Invalid priority!")
            return

        task[2] = new_priority

    new_date = input(
        f"Enter new due date [{task[3]}] (DD-MM-YYYY): "
    ).strip()

    if new_date:
        try:
            datetime.strptime(new_date, "%d-%m-%Y")
        except ValueError:
            print("Invalid date!")
            return

        task[3] = new_date

    save_tasks(tasks)
    print("Task updated successfully!")


# Delete task
def delete_task(tasks):
    print("\n========== DELETE TASK ==========")

    task_id = input("Enter task ID to delete: ").strip()
    task = find_task(tasks, task_id)

    if task is None:
        print("Task not found!")
        return

    print("Task:", task[1])

    confirmation = input(
        "Are you sure you want to delete this task? (yes/no): "
    ).strip().lower()

    if confirmation == "yes":
        tasks.remove(task)
        save_tasks(tasks)
        print("Task deleted successfully!")
    else:
        print("Deletion cancelled.")


# Mark task as completed
def mark_completed(tasks):
    print("\n========== COMPLETE TASK ==========")

    task_id = input("Enter task ID: ").strip()
    task = find_task(tasks, task_id)

    if task is None:
        print("Task not found!")
        return

    if task[4] == "COMPLETED":
        print("This task is already completed.")
        return

    task[4] = "COMPLETED"

    save_tasks(tasks)
    print("Task marked as completed!")


# View pending tasks
def view_pending(tasks):
    print("\n========== PENDING TASKS ==========")

    pending = [
        task for task in tasks
        if task[4] == "PENDING"
    ]

    priority_order = {
        "High": 1,
        "Medium": 2,
        "Low": 3
    }

    pending.sort(
        key=lambda task: (
            priority_order.get(task[2], 4),
            datetime.strptime(task[3], "%d-%m-%Y")
        )
    )

    if not pending:
        print("No pending tasks.")
        return

    display_tasks(pending)


# View overdue tasks
def view_overdue(tasks):
    print("\n========== OVERDUE TASKS ==========")

    today = date.today()
    overdue = []

    for task in tasks:
        due_date = datetime.strptime(
            task[3], "%d-%m-%Y"
        ).date()

        if task[4] == "PENDING" and due_date < today:
            overdue.append(task)

    if not overdue:
        print("No overdue tasks.")
        return

    display_tasks(overdue)


# View upcoming tasks
def view_upcoming(tasks):
    print("\n========== UPCOMING TASKS ==========")

    today = date.today()
    upcoming_limit = today + timedelta(days=7)
    upcoming = []

    for task in tasks:
        due_date = datetime.strptime(
            task[3], "%d-%m-%Y"
        ).date()

        if (
            task[4] == "PENDING"
            and today <= due_date <= upcoming_limit
        ):
            upcoming.append(task)

    upcoming.sort(
        key=lambda task: datetime.strptime(
            task[3], "%d-%m-%Y"
        )
    )

    if not upcoming:
        print("No upcoming tasks in the next 7 days.")
        return

    display_tasks(upcoming)


# View statistics
def view_statistics(tasks):
    print("\n========== TASK STATISTICS ==========")

    total = len(tasks)
    completed = sum(
        1 for task in tasks
        if task[4] == "COMPLETED"
    )
    pending = sum(
        1 for task in tasks
        if task[4] == "PENDING"
    )

    today = date.today()
    overdue = 0

    for task in tasks:
        due_date = datetime.strptime(
            task[3], "%d-%m-%Y"
        ).date()

        if task[4] == "PENDING" and due_date < today:
            overdue += 1

    print("Total Tasks     :", total)
    print("Completed Tasks :", completed)
    print("Pending Tasks   :", pending)
    print("Overdue Tasks   :", overdue)

    print("\n--- Priority Breakdown ---")

    for priority in ["High", "Medium", "Low"]:
        count = sum(
            1 for task in tasks
            if task[2] == priority
            and task[4] == "PENDING"
        )

        print(f"{priority} Priority Pending Tasks: {count}")

    if total > 0:
        percentage = (completed / total) * 100
        print(f"\nCompletion Rate: {percentage:.2f}%")
    else:
        print("\nCompletion Rate: 0.00%")


# Main program
def main():
    tasks = load_tasks()

    while True:
        display_menu()

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_task(tasks)

        elif choice == "2":
            display_tasks(tasks)

        elif choice == "3":
            edit_task(tasks)

        elif choice == "4":
            delete_task(tasks)

        elif choice == "5":
            mark_completed(tasks)

        elif choice == "6":
            view_pending(tasks)

        elif choice == "7":
            view_overdue(tasks)

        elif choice == "8":
            view_upcoming(tasks)

        elif choice == "9":
            view_statistics(tasks)

        elif choice == "10":
            print("Thank you for using To-Do List Manager!")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 10.")


if __name__ == "__main__":
    main()

