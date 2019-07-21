def getStartDate(task):
    return task._start_date


class Task:
    def __init__(self, ID, parents, start_date, end_date):
        self._ID = ID
        self._parents = []
        self._start_date = start_date
        self._end_date = end_date

    def execute(self):
        print("    Task " + str(self._ID) + " executed")


# class Machine:
#     def __init__(self, ID):
#         self._ID = ID
#         self._tasks = []
#     def addTask(self, ID, parents, start_date, end_date):
#         new_task = Task(ID, parents, start_date, end_date)
#         self._tasks.append(new_task)

class Schedule:
    def __init__(self):
        self._events_list = []

    def addEvent(self, task):
        self._events_list.append(task)

    def sortEvents(self):
        self._events_list = sorted(self._events_list, key=getStartDate)

    def printEvents(self):
        for event in self._events_list:
            print("Event " + str(event._ID) + " scheduled at " + str(event._start_date))


class Simulator:
    def __init__(self):
        self._schedule = Schedule()

    def loop(self):
        date = 0
        while len(self._schedule._events_list) != 0:
            self._schedule.sortEvents()
            # for event in self._schedule._events_list :
            #     print(str(event._start_date))
            i = 0
            self._schedule.printEvents()
            while self._schedule._events_list[i]._start_date == date:
                current_event = self._schedule._events_list[i]
                current_event.execute()
                self._schedule._events_list.remove(current_event)
                i += 1
            date += 1
            print("Date: " + str(date))
            if date > 20:
                print("Returned")
                return


# The simulator needs to check the execution goes as planned i.e. that a given
# tasks' parents are done executing before it is, itself, executed
simulator = Simulator()

simulator._schedule.addEvent(Task(0, [], 0, 5))
simulator._schedule.addEvent(Task(1, [0], 5, 10))
simulator._schedule.addEvent(Task(2, [0], 5, 10))
simulator._schedule.addEvent(Task(3, [0], 5, 10))
simulator._schedule.addEvent(Task(4, [0], 5, 10))
simulator._schedule.addEvent(Task(5, [1], 10, 15))
simulator._schedule.addEvent(Task(6, [6], 10, 15))
simulator._schedule.addEvent(Task(7, [3], 10, 15))
simulator._schedule.addEvent(Task(8, [3, 4], 15, 20))

simulator.loop()
