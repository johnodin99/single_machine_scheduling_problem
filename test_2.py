import pandas as pd
from algorithm.JOB import JOB
data_path = r"data.xlsx"

data = pd.read_excel(data_path, index_col=None, header=None)


def get_total_weight_tardiness(job_list):
    process_time_accumulate = 0
    total_weight_tardiness = 0
    for index, job in enumerate(job_list):
        process_time_accumulate += job.processing_time
        total_weight_tardiness += job.weights * (process_time_accumulate - job.due_date)
    return total_weight_tardiness


initial_job_list = []
for index, items in data.iteritems():
    if index == 0:
        continue
    job = JOB(jobs=items[0], processing_time=items[1], due_date=items[2], weights=items[3])
    initial_job_list.append(job)

job_list = []

# tabu
list_1 =  [11, 19, 15, 3, 4, 16, 0, 9, 8, 12, 7, 6, 13, 10, 1, 17, 5, 14, 2, 18]

# genetic
list_2 = [11, 8, 15, 4, 3, 16, 13, 0, 7, 9, 10, 6, 1, 19, 12, 17, 2, 5, 18, 14]

for order in list_1:
    job_list.append(initial_job_list[order])

print(get_total_weight_tardiness(job_list))

job_list = []
for order in list_2:
    job_list.append(initial_job_list[order])
print(get_total_weight_tardiness(job_list))