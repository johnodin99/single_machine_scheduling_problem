import random
import pandas as pd
from algorithm.JOB import JOB


class GENETIC:
    def __init__(self, data_path, population_size=30, crossover_rate=0.8, mutation_rate=0.1,
                 mutation_selection_rate=0.5,
                 num_iteration=5,
                 ):
        self.initial_job_list = []
        self.processing_time_list = []
        self.due_date_list = []
        self.weights_list = []

        self.population_list = []

        self.minimum_record_order_list = []
        self.tardiness_list = []
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.mutation_selection_rate = mutation_selection_rate
        self.num_mutation_jobs = len(self.initial_job_list) * self.mutation_rate
        self.num_iteration = num_iteration
        self.initial_data(data_path)

        print()
        # print(self.processing_time_list)
        print(self.due_date_list)
        print(self.weights_list)

    def initial_data(self, data_path):
        self.initial_job_list = self.read_data(data_path)
        self.population_list = self.get_population_list()
        self.processing_time_list = self.get_processing_time_list(self.initial_job_list)
        self.due_date_list = self.get_due_date_list(self.initial_job_list)
        self.weights_list = self.get_weights_list(self.initial_job_list)

    def get_processing_time_list(self, job_list):
        processing_time_list = [job.processing_time for job in job_list]
        return processing_time_list

    def get_due_date_list(self, job_list):
        due_date_list = [job.due_date for job in job_list]
        return due_date_list

    def get_weights_list(self, job_list):
        weights_list = [job.weights for job in job_list]
        return weights_list

    def get_population_list(self):

        population_list = []
        for i in range(self.population_size):
            order_list = self.get_random_order_list()
            population_list.append(order_list)
        return population_list

    def get_random_order_list(self):
        order_list = [i for i in range(len(self.initial_job_list))]
        random.shuffle(order_list)
        return order_list

    def read_data(self, data_path):
        data = pd.read_excel(data_path, index_col=None, header=None)
        initial_job_list = []
        for index, items in data.iteritems():
            print(items)
            if index == 0:
                continue
            job = JOB(jobs=items[0], processing_time=items[1], due_date=items[2], weights=items[3])
            initial_job_list.append(job)
        return initial_job_list


