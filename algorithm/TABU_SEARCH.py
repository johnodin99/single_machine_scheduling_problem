import pandas as pd
import random
import numpy as np
import os
from algorithm.JOB import JOB


class TABU:
    def __init__(self, data_path, tabu_size=10, random_seed=None):
        self.initial_job_list = []
        self.order_list = []
        self.job_list = []
        self.tabu_list = []
        self.minimum_record_order_list = []
        self.tardiness_list = []
        self.random_seed = random_seed
        self.tabu_size = tabu_size
        self.initial_data(data_path)
        self.tabu_times = 0

    def run(self):

        exchange_tabu_list_in_list = []

        the_minimum_order_list_in_list = []

        tardiness_list = []

        the_minimum_job_list, the_minimum_order_list, exchange_tabu_list, the_minimum_tardiness = \
            self.neighborhood_search_one_cycle(
                job_list=None,
                order_list=None,
                exchange_tabu_list_in_list=exchange_tabu_list_in_list,
                the_minimun_order_list_in_list=the_minimum_order_list_in_list)
        exchange_tabu_list_in_list.append(exchange_tabu_list)
        count = 1

        tardiness_list.append(the_minimum_tardiness)
        the_minimum_order_list_in_list.append(the_minimum_order_list)

        while True:
            the_minimum_job_list, the_minimum_order_list, exchange_tabu_list, tardiness = \
                self.neighborhood_search_one_cycle(
                    job_list=the_minimum_job_list,
                    order_list=the_minimum_order_list,
                    exchange_tabu_list_in_list=exchange_tabu_list_in_list,
                    the_minimun_order_list_in_list=the_minimum_order_list_in_list)
            the_minimum_order_list_in_list.append(the_minimum_order_list)
            if len(exchange_tabu_list_in_list) == self.tabu_size:
                del (exchange_tabu_list_in_list[0])
                exchange_tabu_list_in_list.append(exchange_tabu_list)
            else:
                exchange_tabu_list_in_list.append(exchange_tabu_list)

            if tardiness < the_minimum_tardiness:
                tardiness_list.append(tardiness)
                the_minimum_tardiness = tardiness
            else:
                break
            count += 1

        job_sequence_ptime = 0
        num_tardy = 0
        for k in range(len(self.initial_job_list)):
            job_sequence_ptime = job_sequence_ptime + self.processing_time_list[the_minimum_order_list[k]]
            if job_sequence_ptime > self.due_date_list[the_minimum_order_list[k]]:
                num_tardy = num_tardy + 1

        print(the_minimum_order_list)
        print(the_minimum_tardiness)
        average_tardiness = the_minimum_tardiness / len(self.initial_job_list)
        print(average_tardiness)
        print(num_tardy)

        self.save_result(the_minimum_tardiness, average_tardiness, the_minimum_order_list, num_tardy)

    def save_result(self, the_minimum_tardiness, average_tardiness, the_minimum_order_list, num_tardy,
                    record_path="tbu_record.csv"):
        if not os.path.isfile(record_path):
            record_df = pd.DataFrame([])
        else:
            record_df = pd.read_csv(record_path, index_col=0)

        temp_dict = {

            "optimal_value": the_minimum_tardiness,
            "average_tardiness": average_tardiness,
            "num_tardy": num_tardy,
            "sequence_best": the_minimum_order_list,
            "tabu_size": self.tabu_size,
            "random_seed": self.random_seed
        }
        record_df = record_df.append(temp_dict, ignore_index=True)
        record_df.to_csv(record_path)

    def get_processing_time_list(self, job_list):
        processing_time_list = [job.processing_time for job in job_list]
        return processing_time_list

    def get_due_date_list(self, job_list):
        due_date_list = [job.due_date for job in job_list]
        return due_date_list

    def get_weights_list(self, job_list):
        weights_list = [job.weights for job in job_list]
        return weights_list

    def neighborhood_search_one_cycle(self, job_list=None, order_list=None, exchange_tabu_list_in_list=[],
                                      the_minimun_order_list_in_list=[]):
        if job_list is None:
            job_list = self.job_list
        if order_list is None:
            order_list = self.order_list
        temp_job_list_in_list = []
        temp_order_list_in_list = []
        tabu_exchange_list = []
        tardiness_list = []
        for index, job in enumerate(job_list):
            temp_job_list = job_list.copy()
            temp_order_list = order_list.copy()

            if index + 1 == len(job_list):
                continue

            temp_order_list[index + 1], temp_order_list[index] = order_list[index], order_list[index + 1]

            # check exchange_list is in tabu_list or not
            if [order_list[index], order_list[index + 1]] in exchange_tabu_list_in_list:
                self.tabu_times += 1
                continue
            if [order_list[index + 1], order_list[index]] in exchange_tabu_list_in_list:
                self.tabu_times += 1
                continue
            if temp_order_list in the_minimun_order_list_in_list:
                self.tabu_times += 1
                continue

            temp_job_list[index + 1], temp_job_list[index] = job_list[index], job_list[index + 1]

            tardiness = self.get_total_weight_tardiness(temp_job_list)

            temp_job_list_in_list.append(temp_job_list)
            temp_order_list_in_list.append(temp_order_list)
            tabu_exchange_list.append([order_list[index], order_list[index + 1]])
            tardiness_list.append(tardiness)

        the_minimum_index = self.get_the_minimun_index(tardiness_list)
        the_minimum_tardiness = tardiness_list[the_minimum_index]
        the_minimum_job_list = temp_job_list_in_list[the_minimum_index]
        the_minimum_order_list = temp_order_list_in_list[the_minimum_index]
        the_tabu_list = tabu_exchange_list[the_minimum_index]

        return the_minimum_job_list, the_minimum_order_list, the_tabu_list, the_minimum_tardiness

    def get_the_minimun_index(self, tardiness_list):
        tardiness_array = np.array(tardiness_list)
        return tardiness_array.argmin()

    def initial_data(self, data_path):
        self.initial_job_list = self.read_data(data_path)
        self.order_list = self.get_initial_random_order_list()
        for order in self.order_list:
            self.job_list.append(self.initial_job_list[order])

        self.processing_time_list = self.get_processing_time_list(self.initial_job_list)
        self.due_date_list = self.get_due_date_list(self.initial_job_list)
        self.weights_list = self.get_weights_list(self.initial_job_list)

    def get_initial_random_order_list(self):
        order_list = [i for i in range(len(self.initial_job_list))]
        if self.random_seed is not None:
            random.seed(self.random_seed)
        random.shuffle(order_list)
        return order_list

    def read_data(self, data_path):
        data = pd.read_excel(data_path, index_col=None, header=None)
        initial_job_list = []
        for index, items in data.iteritems():
            if index == 0:
                continue
            job = JOB(jobs=items[0], processing_time=items[1], due_date=items[2], weights=items[3])

            initial_job_list.append(job)
        return initial_job_list

    def get_total_weight_tardiness(self, job_list):
        process_time_accumulate = 0
        total_weight_tardiness = 0
        for index, job in enumerate(job_list):
            process_time_accumulate += job.processing_time
            total_weight_tardiness += job.weights * (process_time_accumulate - job.due_date)
        return total_weight_tardiness
