from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Tuple
import time as time1
import sys

def get_input(filename):
    '''Function that reads a file and returns n(number of activities), time constraint, cost constraint and activities list with their respective name, time, cost and enjoyment values'''
    file=open(f"{filename}") #opens file
    file_list=file.readlines() #reads all lines in file
    n=int(file_list[0].strip()) #removes "\n" from the first line and converts to int and stores under variable n
    time, cost=file_list[1].split() #splits 2nd line and assigns elements to variables time and cost
    time_max=int(time) #converts time to int
    cost_max=int(cost) #converts cost to int
    activities=[] #creates list of activities that is blank
    for line in file_list[2:]: #iterates through the list from the 3rd element(index 2) to the end
        line.strip() #removes "\n" from the line
        name, time, cost, enjoyment=line.split() #splits line and assigns elements to variables name, time, cost and enjoyment
        #activities.append({"name": name, "time":time, "cost": cost, "enjoyment": enjoyment}) #adds dictionary to list of activities
        activities.append([name, int(time), int(cost), int(enjoyment)]) #adds list with name, time, cost and enjoyment to list of activities
    file.close() #closes file
    return n, time_max, cost_max, activities

#for this, i have copied lots of code from the original program but have altered things
#now instead of having a 2d grid for the dp algorithm, it will now be 3d so that both time and budget can be used at the same time to calculate the results


#main function!
def dp(number_of_activities, time, budget, activities):

    enjoyment_index = 3 #enjoyment is the 4th element in the list so index 3

    #now we need to create the dp table using a 3D grid (activities, time and budget)
    dp_grid = []
    
    for activities_considered in range(number_of_activities + 1):
        time_layer = []
        for current_time_limit in range(time + 1):
            row = []
            for current_budget_limit in range(budget + 1):
                row.append(0)
            time_layer.append(row)
        dp_grid.append(time_layer)

    #now we pretty much do the exact same thing but for a keep table now so we can choose the activities that are the best
    keep_grid = []

    for activities_considered in range(number_of_activities + 1):
        time_layer = []
        for current_time_limit in range(time + 1):
            row = []
            for current_budget_limit in range(budget + 1):
                row.append(False)
            time_layer.append(row)
        keep_grid.append(time_layer)

    
    #here is now where the main algorithm logic will be. we are going to here fill the dp table
    for activities_considered in range(1, number_of_activities + 1):
        activity_i = activities[activities_considered - 1] 
        
        time_weight = activity_i[1] #time is the 2nd element in list so index 1
        cost_weight = activity_i[2] #cost is the 3rd element in list so index 2
        value = activity_i[enjoyment_index]
    
        #ok here is the dp filling part
        for current_time_limit in range(time + 1):
            for current_budget_limit in range(budget + 1):
            
                #option 1 is to skip the activity
                skip = dp_grid[activities_considered - 1][current_time_limit][current_budget_limit]

                #option 2 is to take the activity if it fits
                if time_weight <= current_time_limit and cost_weight <= current_budget_limit:
                    take = dp_grid[activities_considered - 1][current_time_limit - time_weight][current_budget_limit - cost_weight] + value
                else:
                    take = - 1 #if it doesn't work

                #this part will compare whether taking it or skipping it was the better decision
                if take > skip:
                    dp_grid[activities_considered][current_time_limit][current_budget_limit] = take
                    keep_grid[activities_considered][current_time_limit][current_budget_limit] = True
                else:
                    dp_grid[activities_considered][current_time_limit][current_budget_limit] = skip
                    keep_grid[activities_considered][current_time_limit][current_budget_limit] = False


    #this part here is the backtracking step. it will reconstruct the set of activities that produce max enjoyment calculated by the DP table
    chosen_activities = []
    current_time_limit = time
    current_budget_limit = budget

    activities_considered = number_of_activities
    while activities_considered > 0:
        if keep_grid[activities_considered][current_time_limit][current_budget_limit] == True:
            activity_i = activities[activities_considered - 1]
            chosen_activities.append(activity_i)
            current_time_limit = current_time_limit - activity_i[1]
            current_budget_limit = current_budget_limit - activity_i[2]
        activities_considered = activities_considered - 1  
    
    chosen_activities.reverse()

    
    #now finally this part will compute the totals for each variable
    total_enjoyment = 0
    total_time = 0
    total_cost = 0

    for activity in chosen_activities:
        total_enjoyment = total_enjoyment + activity[enjoyment_index]
        total_time = total_time + activity[1]
        total_cost = total_cost + activity[2]

    #now we will just return the activities and totals! and DONE!
    return chosen_activities, total_enjoyment, total_time, total_cost


#function for running the time and budget constraint at the same time now
def run_time_and_budget_constraint(number_of_activities, time, budget, activities):
    return dp(number_of_activities, time, budget, activities)

#function that prints the dp output
#exec_time is not defined as this is what comes from the testing of the program I believe
def print_dp_output(chosen_activities, total_enjoyment, total_time, total_cost, exec_time):
    print("--- DYNAMIC PROGRAMMING ALGORITHM ---")
    print("Selected Activities:")

    for activity in chosen_activities:
        print(
            f" - {activity[0]} "
            f"({activity[1]} hours, £{activity[2]}, enjoyment {activity[3]})"
        )

    print(f"Total Enjoyment: {total_enjoyment}")
    print(f"Total Time Used: {total_time} hours")
    print(f"Total Cost: £{total_cost}")
    print(f"Execution Time: {exec_time} seconds")



#function that prints the brute force output
#exec_time is not defined as this is what comes from the testing of the program I believe
def print_bf_output(chosen_activities, total_enjoyment, total_time, total_cost, exec_time):
    print("--- BRUTE FORCE ALGORITHM ---")
    print("Selected Activities:")

    for activity in chosen_activities:
        print(
            f" - {activity[0]} "
            f"({activity[1]} hours, £{activity[2]}, enjoyment {activity[3]})"
        )

    print(f"Total Enjoyment: {total_enjoyment}")
    print(f"Total Time Used: {total_time} hours")
    print(f"Total Cost: £{total_cost}")
    print(f"Execution Time: {exec_time} seconds")




@dataclass(frozen=True)
class Activity:
    name: str
    time: int          
    cost: float        
    enjoyment: int     

def brute_force_optimal_plan(
    activities: List[Activity],
    max_time: Optional[int] = None,
    max_budget: Optional[float] = None
) -> Dict[str, Any]:
    """
    Brute-force search over all 2^n subsets of activities.

    Requirements satisfied:
    - Generates all subsets (2^n) via bitmasks.
    - Checks feasibility against time and/or budget constraints.
    - Computes total enjoyment for feasible subsets.
    - Tracks and returns the best feasible subset (max enjoyment).
    - Returns chosen activities, total enjoyment, time used, and cost.

    If max_time is None, time is unconstrained.
    If max_budget is None, budget is unconstrained.
    """

    n = len(activities)

    best_subset: List[Activity] = []
    best_enjoyment = float("-inf")
    best_time = 0
    best_cost = 0.0

    # Enumerate all subsets: masks 0..(2^n - 1)
    for mask in range(1 << n):
        subset: List[Activity] = []
        total_time = 0
        total_cost = 0.0
        total_enjoyment = 0

        # Build subset and compute totals
        for i in range(n):
            if mask & (1 << i):  # bit i is set => include activity i
                a = activities[i]
                subset.append(a)
                total_time += a.time
                total_cost += a.cost
                total_enjoyment += a.enjoyment

        # Feasibility check
        if max_time is not None and total_time > max_time:
            continue
        if max_budget is not None and total_cost > max_budget:
            continue

        if total_enjoyment > best_enjoyment:
            best_enjoyment = total_enjoyment
            best_subset = subset
            best_time = total_time
            best_cost = total_cost

    # Handle the case where nothing is feasible
    if best_enjoyment == float("-inf"):
        return [], 0, 0, 0
    
    #returns results in the same form as dp algorithm
    formatted_subset=[]
    for x in best_subset:
        formatted_subset.append([x.name, x.time, x.cost, x.enjoyment])
    return formatted_subset, int(best_enjoyment), best_time, float(best_cost)




# Executing code:
if __name__ == "__main__":

    #checks if input file name was provided
    if len(sys.argv)<2:
        print("Use the following format: python event_planner.py <input_file_path>")
        sys.exit(1)
    filename=sys.argv[1]

    #gets variables from input file
    n, time_max, cost_max, activities = get_input(filename)

    #runs dp algorithm and measures time taken
    start=time1.perf_counter()
    chosen_activities, total_enjoyment, total_time, total_cost = run_time_and_budget_constraint(
        n, time_max, cost_max, activities
    )
    end=time1.perf_counter()
    dp_time=end-start

    #prints results in the format in the specification
    print(f"""========================================\n
EVENT PLANNER - RESULTS\n
========================================\n
Input File: {filename}\n
Available Time: {time_max} hours\n
Available Budget: £{cost_max}\n""")
    
    #prints dp results
    print_dp_output(
    chosen_activities,
    total_enjoyment,
    total_time,
    total_cost,
    dp_time,
    )

    #makes inputs compatible with bf algorithm as Aidan programmed it to use diffrent input format than Lorenzo's dp algorithm
    activities_objects=[]
    for x in activities:
        act=Activity(name=x[0], time=x[1], cost=x[2], enjoyment=x[3])
        activities_objects.append(act)

    #runs bf algorithm and measures time taken
    start=time1.perf_counter()
    chosen_activities_bf, total_enjoyment_bf, total_time_bf, total_cost_bf = brute_force_optimal_plan(activities_objects, max_time=time_max, max_budget=cost_max)
    end=time1.perf_counter()
    bf_time=end-start

    #prints bf results
    print_bf_output(
    chosen_activities_bf,
    total_enjoyment_bf,
    total_time_bf,
    total_cost_bf,
    bf_time,
    )


