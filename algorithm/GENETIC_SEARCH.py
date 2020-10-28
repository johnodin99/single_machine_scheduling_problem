import random
import numpy as np
import pandas as pd
import copy
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
        self.num_obj = None
        self.minimum_record_order_list = []
        self.tardiness_list = []
        self.population_list = []
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.mutation_selection_rate = mutation_selection_rate
        self.num_iteration = num_iteration
        self.initial_data(data_path)
        self.num_job = len(self.initial_job_list)

    def run(self):

        num_mutation_jobs = round(self.num_job * self.mutation_selection_rate)

        '''==================== main code ==============================='''
        '''----- generate initial population -----'''
        Tbest = np.inf

        for n in range(self.num_iteration):
            # print("self.population_list")
            # print(self.population_list)

            Tbest_now = np.inf
            '''-------- crossover --------'''
            parent_list = copy.deepcopy(self.population_list)
            offspring_list = copy.deepcopy(self.population_list)
            # generate a random sequence to select the parent chromosome to crossover
            S = list(np.random.permutation(self.population_size))

            print("generate a random sequence to select the parent chromosome to crossover")
            print(S)

            for m in range(int(self.population_size / 2)):
                crossover_prob = np.random.rand()
                if self.crossover_rate >= crossover_prob:
                    parent_1 = self.population_list[S[2 * m]][:]
                    parent_2 = self.population_list[S[2 * m + 1]][:]
                    child_1 = ['na' for i in range(self.num_job)]
                    child_2 = ['na' for i in range(self.num_job)]
                    fix_num = round(self.num_job / 2)
                    g_fix = list(np.random.choice(self.num_job, fix_num, replace=False))

                    for g in range(fix_num):
                        child_1[g_fix[g]] = parent_2[g_fix[g]]
                        child_2[g_fix[g]] = parent_1[g_fix[g]]
                    c1 = [parent_1[i] for i in range(self.num_job) if parent_1[i] not in child_1]
                    c2 = [parent_2[i] for i in range(self.num_job) if parent_2[i] not in child_2]

                    for i in range(self.num_job - fix_num):
                        child_1[child_1.index('na')] = c1[i]
                        child_2[child_2.index('na')] = c2[i]
                    offspring_list[S[2 * m]] = child_1[:]
                    offspring_list[S[2 * m + 1]] = child_2[:]

            '''--------mutatuon--------'''
            for m in range(len(offspring_list)):
                mutation_prob = np.random.rand()
                if self.mutation_rate >= mutation_prob:
                    # chooses the position to mutation
                    m_chg = list(np.random.choice(self.num_job, num_mutation_jobs, replace=False))
                    # save the value which is on the first mutation position
                    t_value_last = offspring_list[m][m_chg[0]]
                    for i in range(num_mutation_jobs - 1):
                        # displacement
                        offspring_list[m][m_chg[i]] = offspring_list[m][m_chg[i + 1]]

                    # move the value of the first mutation position to the last mutation position
                    offspring_list[m][m_chg[num_mutation_jobs - 1]] = t_value_last

            '''--------fitness value(calculate tardiness)-------------'''
            # parent and offspring chromosomes combination
            total_chromosome = copy.deepcopy(parent_list) + copy.deepcopy(offspring_list)

            chrom_fitness, chrom_fit = [], []
            total_fitness = 0
            for i in range(self.population_size * 2):
                ptime = 0
                tardiness = 0
                for j in range(self.num_job):
                    ptime = ptime + self.processing_time_list[total_chromosome[i][j]]
                    tardiness = tardiness + self.weights_list[total_chromosome[i][j]] * max(
                        ptime - self.due_date_list[total_chromosome[i][j]], 0)
                chrom_fitness.append(1 / tardiness)
                chrom_fit.append(tardiness)
                total_fitness = total_fitness + chrom_fitness[i]

            '''----------selection----------'''
            pk, qk = [], []

            for i in range(self.population_size * 2):
                pk.append(chrom_fitness[i] / total_fitness)
            for i in range(self.population_size * 2):
                cumulative = 0
                for j in range(0, i + 1):
                    cumulative = cumulative + pk[j]
                qk.append(cumulative)

            selection_rand = [np.random.rand() for i in range(self.population_size)]

            for i in range(self.population_size):
                if selection_rand[i] <= qk[0]:
                    self.population_list[i] = copy.deepcopy(total_chromosome[0])
                else:
                    for j in range(0, self.population_size * 2 - 1):
                        if selection_rand[i] > qk[j] and selection_rand[i] <= qk[j + 1]:
                            self.population_list[i] = copy.deepcopy(total_chromosome[j + 1])
                            break
            '''----------comparison----------'''
            for i in range(self.population_size * 2):
                if chrom_fit[i] < Tbest_now:
                    Tbest_now = chrom_fit[i]
                    sequence_now = copy.deepcopy(total_chromosome[i])

            if Tbest_now <= Tbest:
                Tbest = Tbest_now
                sequence_best = copy.deepcopy(sequence_now)

            job_sequence_ptime = 0
            num_tardy = 0
            for k in range(self.num_job):
                job_sequence_ptime = job_sequence_ptime + self.processing_time_list[sequence_best[k]]
                if job_sequence_ptime > self.due_date_list[sequence_best[k]]:
                    num_tardy = num_tardy + 1
        '''----------result----------'''
        print("optimal sequence", sequence_best)
        print("optimal value:%f" % Tbest)
        print("average tardiness:%f" % (Tbest / self.num_job))
        print("number of tardy:%d" % num_tardy)

    def initial_data(self, data_path):
        self.initial_job_list = self.read_data(data_path)
        self.population_list = self.get_population_list()
        self.processing_time_list = self.get_processing_time_list(self.initial_job_list)
        self.due_date_list = self.get_due_date_list(self.initial_job_list)
        self.weights_list = self.get_weights_list(self.initial_job_list)
        self.num_obj = len(self.initial_job_list)

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

            if index == 0:
                continue
            job = JOB(jobs=items[0], processing_time=items[1], due_date=items[2], weights=items[3])
            initial_job_list.append(job)
        return initial_job_list
