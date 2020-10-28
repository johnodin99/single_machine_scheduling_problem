from algorithm.TABU_SEARCH import TABU
from algorithm.GENETIC_SEARCH import GENETIC
data_path = r"data.xlsx"

# for tabu_size in range(3, 4):
#     print("tabu_size")
#     print(tabu_size)
#     jobs = TABU(data_path, tabu_size=tabu_size, random_seed=3)
#     jobs.run()



# jobs = TABU(data_path, tabu_size=10, random_seed=3)
# jobs.run()


jobs = GENETIC(data_path,
               population_size=30,
               crossover_rate=0.8,
               mutation_rate=0.1,
               mutation_selection_rate=0.5,
               num_iteration=1)

jobs.run()
#[3, 11, 4, 15, 8, 16, 0, 9, 7, 1, 6, 12, 19, 10, 13, 17, 14, 2, 5, 18]
# optimal value:2009.000000
# average tardiness:100.450000
# number of tardy:15

