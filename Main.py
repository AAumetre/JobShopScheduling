class Task:
    def __init__(self, ID, parents, machine, start_date, unitDuration):
        self.ID = ID
        self.parents = parents
        self.machine = machine
        self.unit_duration = unitDuration
        self.start_date = start_date
        self.done = False


class Machine:
    def __init__(self, ID):
        self.ID = ID
        self.tasks = []
        self.task = None
        self.start_date = 0
        self.end_date = 0

    def associateTask(self, task):
        self.tasks.append(task)

    def startTask(self, task, date):
        self.task = task
        self.start_date = date
        self.end_date = date + task.unit_duration

    def endTask(self, task, date):
        self.task.done = True
        self.task = None
        self.startDate = 0
        self.endDate = 0

    def selectTaskToStart(self, date):
        for task in self.tasks:
            if task.done == False:
                print(task)
                return task
        return None


# Group of machines
class Processor:
    def __init__(self):
        self.machines = dict()

    def getMachine(self, ID):
        return self.machines.get(ID, None)

    def newMachine(self, ID):
        machine = self.getMachine(ID)
        if machine == None:
            machine = Machine(ID)
            self.machines[ID] = machine
        return machine

    def newTask(self, ID, parents, machine, date, unitDuration):
        task = Task(ID, parents, machine, date, unitDuration)
        machine.associateTask(task)
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

    def isEmpty(self):
        return len(self.events) == 0

    def getNextEvent(self):
        if self.isEmpty():
            return None
        return self.events[0]

    def dequeueNextEvent(self):
        if self.isEmpty():
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


class Simulator:
    def __init__(self, processor):
        self.processor = processor
        self.schedule = Schedule()
        self.print_trace = False

    def simulationLoop(self):
        last_date = 0
        while not self.schedule.isEmpty():
            event = self.schedule.dequeueNextEvent()
            self.fireEvent(event)
            next_event = self.schedule.getNextEvent()
            if next_event == None or next_event.date > event.date:
                self.lookForTaskToStartInProcessor(event.date)
            last_date = event.date
        return last_date

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

    def lookForTaskToStartInProcessor(self, date):
        for machine in self.processor.machines.values():
            self.lookForTaskToStartInMachine(machine, date)

    def lookForTaskToStartInMachine(self, machine, date):
        selection = machine.selectTaskToStart(date)
        if selection == None:
            return
        self.schedule.newStartTaskEvent(selection, date)

    # Go through the machines, extract the tasks and add them to the schedule
    def loadTasks(self):
        for i in range(len(self.processor.machines)):
            machine = self.processor.getMachine(i)
            for task in machine.tasks:
                this_date = task.start_date
                self.schedule.newStartTaskEvent(task, this_date)
                self.schedule.newEndTaskEvent(task, this_date + task.unit_duration)


# =============================================================================
processor = Processor()

machine0 = processor.newMachine(0)
machine1 = processor.newMachine(1)
machine2 = processor.newMachine(2)
machine3 = processor.newMachine(3)

processor.newTask(0, [], machine0, 0, 5)
processor.newTask(1, [0], machine0, 5, 5)
processor.newTask(2, [0], machine1, 5, 5)
processor.newTask(3, [0], machine2, 5, 5)
processor.newTask(4, [0], machine3, 5, 5)
processor.newTask(5, [1], machine0, 10, 5)
processor.newTask(6, [6], machine1, 10, 5)
processor.newTask(7, [3], machine2, 10, 5)
processor.newTask(8, [3, 4], machine3, 15, 5)

# The simulator needs to check the execution goes as planned i.e. that a given
# tasks' parents are done executing before it is, itself, executed
simulator = Simulator(processor)

simulator.loadTasks()
last_date = simulator.simulationLoop()
print("Computation completed at " + str(last_date))
