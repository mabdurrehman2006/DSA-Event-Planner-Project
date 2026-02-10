#Dynamic Programming part of the coursework (0/1 Knapsack)
from Text_Reader import get_input
#main function!
def dp(number_of_activities, time, budget, activities, mode):

    #this part here decides which variable we will choose to be the constraint
    if mode == "time":
        capacity = time
        weight_key = 1 #cost is the 2nd element in list so index 1
    else:
        capacity = budget
        weight_key = 2 #cost is the 3rd element in list so index 2
    enjoyment_index=3 #enjoyment is the 4th element in the list so index 3

    #now we need to create the dp table using a 2D grid
    dp_grid = []
    
    for activities_considered in range(number_of_activities + 1):
        row = []
        for column in range(capacity + 1):
            row.append(0)
        dp_grid.append(row)

    #now we pretty much do the exact same thing but for a keep table now so we can choose the activities that are the best
    keep_grid = []

    for activities_considered in range(number_of_activities + 1):
        row = []
        for column in range(capacity + 1):
            row.append(False)
        keep_grid.append(row)

    
    #here is now where the main algorithm logic will be. we are going to here fill the dp table
    for activities_considered in range(1, number_of_activities + 1):
        activity_i = activities[activities_considered - 1] 
        weight = activity_i[weight_key] #this part is where it will take either time or cost as the constraint
        value = activity_i[enjoyment_index]
    
        #ok here is the dp filling part
        for current_capacity_limit in range(capacity + 1):
            
            #option 1 is to skip the activity
            skip = dp_grid[activities_considered - 1][current_capacity_limit]

            #option 2 is to take the activity if it fits
            if weight <= current_capacity_limit:
                take = dp_grid[activities_considered - 1][current_capacity_limit - weight] + value
            else:
                take = - 1 #if it doesn't work

            #this part will compare whether taking it or skipping it was the better decision
            if take > skip:
                dp_grid[activities_considered][current_capacity_limit] = take
                keep_grid[activities_considered][current_capacity_limit] = True
            else:
                dp_grid[activities_considered][current_capacity_limit] = skip
                keep_grid[activities_considered][current_capacity_limit] = False


    #this part here is the backtracking step. it will reconstruct the set of activities that produce max enjoyment calculated by the DP table
    chosen_activities = []
    current_capacity_limit = capacity

    activities_considered = number_of_activities
    while activities_considered > 0:
        if keep_grid[activities_considered][current_capacity_limit] == True:
            activity_i = activities[activities_considered - 1]
            chosen_activities.append(activity_i)
            current_capacity_limit = current_capacity_limit - activity_i[weight_key]
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


#function for running the time constraint
def run_time_constraint(number_of_activities, time, budget, activities):
    return dp(number_of_activities, time, budget, activities, mode = "time")

#function for running the budget constraint
def run_budget_constraint(number_of_activities, time, budget, activities):
    return dp(number_of_activities, time, budget, activities, mode = "budget")

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


#n, time, cost, activities=get_input("Inputs/input_10.txt")
#run_budget_constraint(n, time, cost, activities)




n, time, cost, activities = get_input("Inputs/input_10.txt")
chosen_activities, total_enjoyment, total_time, total_cost = run_budget_constraint(
    n, time, cost, activities
)


print_dp_output(
    chosen_activities,
    total_enjoyment,
    total_time,
    total_cost,
    exec_time=float(),
)


