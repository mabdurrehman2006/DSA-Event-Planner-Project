#Greedy Heuristic Algorithm
#for this greedy algorithm, we will sort the activities by a ratio
#it will not always give the optimal answer but it should be very fast due to it always picking the closest best solution

#main function!
def greedy(number_of_activities, time, budget, activities, mode):

    #this part here decides which variable we will choose to be the constraint
    if mode == "time":
        capacity = time
        weight_key = 1 #time is the 2nd element in list so index 1
    else:
        capacity = budget
        weight_key = 2 #cost is the 3rd element in list so index 2
    enjoyment_index = 3 #enjoyment is the 4th element in the list so index 3

    #now we will calculate the ratio for each activity and store it
    activities_with_ratio = []

    for activity in activities:
        weight = activity[weight_key]
        value = activity[enjoyment_index]

        activities_with_ratio.append((ratio, activity))

    #now we sort the activities by highest ratio first
    activities_with_ratio.sort(reverse=True)

    #now we go through the sorted list and choose activities if they fit
    chosen_activities = []
    total_enjoyment = 0
    total_time = 0
    total_cost = 0
    current_capacity_used = 0

    for ratio, activity in activities_with_ratio:

        weight = activity[weight_key]

        #check if the activity fits within the constraint
        if current_capacity_used + weight <= capacity:
            chosen_activities.append(activity)
            total_enjoyment = total_enjoyment + activity[enjoyment_index]
            total_time = total_time + activity[1]
            total_cost = total_cost + activity[2]
            current_capacity_used = current_capacity_used + weight

    #now we will just return the activities and totals! and DONE!
    return chosen_activities, total_enjoyment, total_time, total_cost


#function for running the time constraint
def run_greedy_time_constraint(number_of_activities, time, budget, activities):
    return greedy(number_of_activities, time, budget, activities, mode = "time")

#function for running the budget constraint
def run_greedy_budget_constraint(number_of_activities, time, budget, activities):
    return greedy(number_of_activities, time, budget, activities, mode = "budget")