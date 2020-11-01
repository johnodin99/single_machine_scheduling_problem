from algorithm.TABU_SEARCH import TABU
from algorithm.GENETIC_SEARCH import GENETIC

data_path = r"data.xlsx"

random_seed = 1
for population_size in range(5, 50, 5):
    for crossover_rate in range(1, 10):
        crossover_rate = crossover_rate / 10
        for mutation_rate in range(1, 10):
            mutation_rate = mutation_rate / 10
            for mutation_selection_rate in range(1, 10):
                mutation_selection_rate = mutation_selection_rate / 10
                for num_iteration in range(20, 100, 10):
                    jobs = GENETIC(data_path,
                                   population_size=population_size,
                                   crossover_rate=crossover_rate,
                                   mutation_rate=mutation_rate,
                                   mutation_selection_rate=mutation_selection_rate,
                                   num_iteration=num_iteration,
                                   random_seed=1)
                    jobs.run()

# jobs = GENETIC(data_path,
#                population_size=30,
#                crossover_rate=0.8,
#                mutation_rate=0.1,
#                mutation_selection_rate=0.5,
#                num_iteration=20,
#                random_seed=1)
#
# jobs.run()
