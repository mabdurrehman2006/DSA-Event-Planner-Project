#Performance Analysis Extension

import time as time
import matplotlib.pyplot as plt
from event_planner import get_input, run_budget_constraint, brute_force_optimal_plan, Activity


#these are the test input files we will use
test_sizes = [10, 15, 20, 25, 30]

dp_times = []
bf_times = []
speedups = []


#this will run both algorithms on every input file
for n in test_sizes:

    filename = f"input_{n}.txt"

    print(f"\nRunning test for n = {n}")

    #load input
    n_val, time_max, cost_max, activities = get_input(filename)

    #dp algorithm
    start = time.perf_counter()
    run_budget_constraint(n_val, time_max, cost_max, activities)
    end = time.perf_counter()
    dp_time = end - start
    dp_times.append(dp_time)

    #change the activities for brute force
    activities_objects = []
    for x in activities:
        act = Activity(name = x[0], time = x[1], cost = x[2], enjoyment = x[3])
        activities_objects.append(act)

    #brute force algorithm 
    #i had to skip n > 25 because n = 30 was taking too long
    if n <= 25:  
        start = time.perf_counter()
        brute_force_optimal_plan(activities_objects, max_time = time_max, max_budget = cost_max)
        end = time.perf_counter()
        bf_time = end - start
    else:
        print(f"Skipping brute force for n = {n} as it is too slow!")
        bf_time = None
    bf_times.append(bf_time)

    #speedup factor (which is brute force runtime/dynamic programming runtime)
    if bf_time is not None:
        speedup = bf_time / dp_time
    else:
        speedup = None
    speedups.append(speedup)


#the line graph which is execution time
#we also need to filter out the none values produced by skipping n = 30 for the brute force algorithm 
plot_sizes_bf = [s for s, t in zip(test_sizes, bf_times) if t is not None]
plot_bf_times = [t for t in bf_times if t is not None]

plt.figure()
plt.plot(test_sizes, dp_times, label = "Dynamic Programming")
plt.plot(plot_sizes_bf, plot_bf_times, label = "Brute Force")
plt.xlabel("Number of Activities (n)")
plt.ylabel("Execution Time (seconds)")
plt.title("Execution Time vs Number of Activities")
plt.legend()
plt.savefig("execution_time_comparison.png")
plt.close()



#the log scale graph
plt.figure()
plt.plot(test_sizes, dp_times, label = "Dynamic Programming")
plt.plot(plot_sizes_bf, plot_bf_times, label = "Brute Force")
plt.yscale("log")
plt.xlabel("Number of Activities (n)")
plt.ylabel("Execution Time (log scale)")
plt.title("Execution Time Comparison (Log Scale)")
plt.legend()
plt.savefig("log_time_comparison.png")
plt.close()



#the speedup factor bar chart
plot_sizes_speedup = [s for s, sp in zip(test_sizes, speedups) if sp is not None]
plot_speedups = [sp for sp in speedups if sp is not None]

plt.figure()
plt.bar(plot_sizes_speedup, plot_speedups)
plt.xlabel("Number of Activities (n)")
plt.ylabel("Speedup Factor (BF time / DP time)")
plt.title("Speedup of Dynamic Programming over Brute Force")
plt.savefig("speedup_chart.png")
plt.close()

print("\nGraphs generated:")
print("time_comparison.png")
print("log_time_comparison.png")
print("speedup_chart.png")