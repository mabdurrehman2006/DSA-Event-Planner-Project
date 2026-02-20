from Text_Reader import get_input

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


#now for the testing part:

if __name__ == "__main__":
    import time
    test_files = ["input_10.txt", "input_15.txt", "input_20.txt"]

    for filename in test_files:
        print(f"\nTesting file: {filename}")
        
        n, max_time, max_budget, activities = get_input(filename)

        #calculate the time
        start_time = time.perf_counter()
        chosen_activities, total_enjoyment, total_time, total_cost = run_time_and_budget_constraint(
            n, max_time, max_budget, activities
        )
        end_time = time.perf_counter()
        exec_time = end_time - start_time

        
        print_dp_output(chosen_activities, total_enjoyment, total_time, total_cost, exec_time)