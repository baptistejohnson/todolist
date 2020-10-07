from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

session = Session()

#new_task = Table(task='Do homework',
 #                deadline=datetime.strptime('10-06-2020', '%m-%d-%Y').date())

#session.add(new_task)
#session.commit()
#first_task = session.query(Table).filter(Table.deadline == datetime.today().date()).first()

#if first_task:
#    session.delete(first_task)
#session.commit()

#rows = session.query(Table).all()
#print(rows)


def todays_tasks():
    print("Today " + datetime.today().strftime("%d").lstrip("0") + datetime.today().strftime(" %b") + ":")
    list_of_tasks = []
    task_number = 1
    for task in session.query(Table):
        # print(datetime.today().date())
        # print(task.deadline)
        if task.deadline == datetime.today().date():
            print("{}. ".format(task_number) + str(task))
            task_number += 1
            list_of_tasks.append(task)
    if not list_of_tasks:
        print("Nothing to do!")
    print("\n")
    main_menu()


def add_tasks():
    print("Enter task")
    input_task = input()
    print("Enter deadline")
    string_deadline = input()
    input_deadline = datetime.strptime(string_deadline, '%Y-%m-%d').date()
    new_task = Table(task='{}'.format(input_task),
                     deadline=input_deadline)
    session.add(new_task)
    session.commit()
    print("The task has been added!")
    print("\n")
    main_menu()


def all_tasks():
    print("All tasks:")
    list_of_all_tasks = session.query(Table).order_by(Table.deadline).all()
    #print(list_of_all_tasks)
    index = 1
    for item in list_of_all_tasks:
        print(str(index) + ". " + str(item) + ". " + item.deadline.strftime("%d").lstrip("0") + item.deadline.strftime(" %b"))
        index += 1
    print("\n")
    main_menu()


def weeks_tasks():
    list_of_all_tasks = session.query(Table).order_by(Table.deadline).all()
    for x in range(7):
        next_day = datetime.today().date() + timedelta(days=x)
        print(next_day.strftime("%A ") + next_day.strftime("%d").lstrip("0") + next_day.strftime(" %b:"))
        day_tasks = session.query(Table).filter(Table.deadline == next_day).all()
        if day_tasks:
            index = 1
            for item in day_tasks:
                print(str(index) + ". " + str(item))
                index += 1
        else:
            print("Nothing to do!")
        print()
    print("\n")
    main_menu()


def del_task():
    print("Choose the number of the task you want to delete:")
    list_of_all_tasks = session.query(Table).order_by(Table.deadline).all()
    #print(list_of_all_tasks)
    index = 1
    for item in list_of_all_tasks:
        print(str(index) + ". " + str(item) + ". " + item.deadline.strftime("%d").lstrip("0") + item.deadline.strftime(" %b"))
        index += 1
    task_index = int(input()) - 1
    session.delete(list_of_all_tasks[task_index])
    session.commit()
    print("The task has been deleted!")
    main_menu()


def missed_tasks():
    print("Missed tasks:")
    list_of_missed_tasks = session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
    index = 1
    for item in list_of_missed_tasks:
        print(str(index) + ". " + str(item) + ". " + item.deadline.strftime("%d").lstrip("0") + item.deadline.strftime(" %b"))
        index += 1
    print()
    main_menu()


def main_menu():
    print("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
    choice = int(input())
    if choice == 1:
        todays_tasks()
    elif choice == 2:
        weeks_tasks()
    elif choice == 3:
        all_tasks()
    elif choice == 4:
        missed_tasks()
    elif choice == 5:
        add_tasks()
    elif choice == 6:
        del_task()
    else:
        print("Bye!")
        return


#rows = session.query(Table).all()
#print(rows)


main_menu()
