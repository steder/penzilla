from hotshot import stats
s = stats.load("hotshot_life_stats")
s.sort_stats("time").print_stats()
