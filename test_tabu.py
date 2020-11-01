from algorithm.TABU_SEARCH import TABU
from algorithm.GENETIC_SEARCH import GENETIC
data_path = r"data.xlsx"

for tabu_size in range(0, 50):
    jobs = TABU(data_path, tabu_size=tabu_size, random_seed=1)
    jobs.run()





