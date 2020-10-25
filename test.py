from algorithm.TABU_SEARCH import TABU

data_path = r"data.xlsx"

for tabu_size in range(3, 20):
    # print("tabu_size")
    # print(tabu_size)
    jobs = TABU(data_path, tabu_size=tabu_size, random_seed=3)
    jobs.run()
