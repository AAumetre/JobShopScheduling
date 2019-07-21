class Job():
    def __init__(self, ID=0, processing_time=1, parents=[]):
        self._ID = ID
        self._p = processing_time
        self._parents = parents
        self._done = False


class Machine():
    def __init__(self, ID=0):
        self._ID = ID
        self._schedule = Schedule()


class Schedule():
    def __init__(self):
        self._key_performances = [0]
        self._schedule = []

    def update(self):
        total_time = 0
        for job in self._schedule:
            total_time += job._p
        self._key_performances[0] = total_time


JOBS = [Job(0, 5, []), Job(1, 2, [0]), Job(2, 2, [0]), Job(3, 2, [0]), Job(4, 2, [0]), Job(5, 2, [1]), Job(6, 2, [2]),
        Job(7, 2, [3]), Job(8, 2, [3, 4])]
MACHINES = [Machine(0), Machine(1), Machine(2), Machine(3)]


def buildGraph(jobs):
    remaining_jobs = jobs.copy()
    primary_jobs = []
    # Initialize with the jobs that have no parents
    for job in remaining_jobs:
        if len(job._parents) == 0:
            primary_jobs.append(job)
            remaining_jobs.remove(job)
    # Add those to the schedule, FIFO style
    for job in primary_jobs:
        submitJob(job)

    # Use the recurrence relationship to find the next jobs to be scheduled
    while len(remaining_jobs) != 0:
        # Look for jobs that can be scheduled (all parents are done)
        for job in remaining_jobs:
            schedulable = True
            for parent_ID in job._parents:
                tmp_job = getJobByID(parent_ID)
                if tmp_job._done == False:
                    schedulable = False
                    return
            # If all parents are done, go ahead
            if schedulable:
                submitJob(job)
                remaining_jobs.remove(job)


def submitJob(Job):
    target_machine = MACHINES[0]
    # Get the less-busy schedule
    for i in range(len(MACHINES)):
        # First, update them all
        MACHINES[i]._schedule.update()
        # Look for the less-busy machine
        if MACHINES[i]._schedule._key_performances[0] < target_machine._schedule._key_performances[0]:
            target_machine = MACHINES[i]
    # Assign the task to target_machine
    target_machine._schedule._schedule.append(Job)
    Job._done = True
    print("Job ID: " + str(Job._ID) + " submitted on machine " + str(target_machine._ID))


def getJobByID(job_ID):
    for job in JOBS:
        if job._ID == job_ID:
            return job


# def getChronograph(machines)

buildGraph(jobs=JOBS)
