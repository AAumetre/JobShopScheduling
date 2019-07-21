class Task:
    def __init__(self, ID, parents, machine, start_date, end_date):
        self.ID = ID
        self.parents = parents
        self.machine = machine
        self.start_date = start_date
        self.end_date = end_date
        self.done = False


class Machine:
    def __init__(self, ID):
        self.ID = ID
        self.tasks = []
        self.task = None
        self.end_date = 0

    def startTask(self, task, date):
        self.task = task
        self.start_date = date
        self.end_date = date + task.unit_duration

    def endTask(self, task, date):
        self.task.done = True
        self.task = None
        self.startDate = 0
        self.endDate = 0

    def newTask(self, ID, parents, date, end_date):
        task = Task(ID, parents, self, date, end_date)
        self.tasks.append(task)
        return task


class Event:
    def __init__(self, ID, type, task, date):
        self.ID = ID
        self.type = type
        self.task = task
        self.date = date


class Schedule:
    def __init__(self):
        self.next_event_ID = 0
        self.events = []

    def getNextEvent(self):
        if len(self.events) == 0:
            return None
        return self.events[0]

    def dequeueNextEvent(self):
        if len(self.events) == 0:
            return None
        return self.events.pop(0)

    def insertEvent(self, event):
        i = 0
        found = False
        while i < len(self.events) and not found:
            other = self.events[i]
            if other.date > event.date:
                found = True
            else:
                i = i + 1
        if found:
            self.events.insert(i, event)
        else:
            self.events.append(event)

    def newStartTaskEvent(self, task, date):
        self.next_event_ID = self.next_event_ID + 1
        event = Event(self.next_event_ID, "start-task", task, date)
        self.insertEvent(event)

    def newEndTaskEvent(self, task, date):
        self.next_event_ID = self.next_event_ID + 1
        event = Event(self.next_event_ID, "end-task", task, date)
        self.insertEvent(event)

    def print(self):
        for event in self.events:
            print("Event " + str(event.type) + " ID " + str(event.ID) + " scheduled at " + str(event.date))


class Simulator:
    def __init__(self, machines):
        self.machines = machines
        self.schedule = Schedule()
        self.print_trace = False

    def simulationLoop(self):
        last_date = 0
        while not len(self.schedule.events) == 0:
            event = self.schedule.dequeueNextEvent()
            self.fireEvent(event)
            next_event = self.schedule.getNextEvent()
            if next_event == None or next_event.date > event.date:
                print("Next time point or end of simulation")
            last_date = event.date
        return last_date

    def loop(self):
        current_time = 0
        while not len(self.schedule.events) == 0:
            for event in self.schedule.events:
                if event.date == current_time
                    event.task.machine.startTask(event.task, current_time)
            current_time += 1

    # Effectively calls an event
    def fireEvent(self, event):
        if event.type == "start-task":
            event.task.machine.startTask(event.task, event.date)
            self.schedule.newEndTaskEvent(event.task, event.task.machine.end_date)
            if self.print_trace:
                print(str(event.ID) + "@" + str(event.date) + ": start task " + str(event.task.ID))
        else:
            event.task.machine.endTask(event.task, event.date)
            if self.print_trace:
                print(str(event.ID) + "@" + str(event.date) + ": end task " + str(event.task.ID))

    # Go through the machines, extract the tasks and add them to the schedule
    def loadTasks(self):
        for machine in self.machines:
            print("Machine " + str(machine.ID))
            for task in machine.tasks:
                print("    Task " + str(task.ID))
                this_date = task.start_date
                self.schedule.newStartTaskEvent(task, this_date)
                self.schedule.newEndTaskEvent(task, this_date + task.unit_duration)


# =============================================================================
machine0 = Machine(0)
machine1 = Machine(1)
machine2 = Machine(2)
machine3 = Machine(3)

MACHINES = [machine0, machine1, machine2, machine3]

machine0.newTask(0, [], 0, 5)
machine0.newTask(1, [0], 5, 10)
machine1.newTask(2, [0], 5, 10)
machine2.newTask(3, [0], 5, 10)
machine3.newTask(4, [0], 5, 10)
machine0.newTask(5, [1], 10, 15)
machine1.newTask(6, [6], 10, 15)
machine2.newTask(7, [3], 10, 15)
machine3.newTask(8, [3, 4], 15, 20)

# The simulator needs to check the execution goes as planned i.e. that a given
# tasks' parents are done executing before it is, itself, executed
simulator = Simulator(MACHINES)

simulator.loadTasks()
simulator.schedule.print()
# last_date = simulator.simulationLoop()
# print("Computation completed at " + str(last_date))
