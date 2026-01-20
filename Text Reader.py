def get_input(filename):
    file=open(f"{filename}")
    file_list=file.readlines()
    n=int(file_list[0].strip()) #removes "\n" from the first line and converts to int and stores under variable n
    time, cost=file_list[1].split() 
    time_max=int(time)
    cost_max=int(cost)
    activities=[] #creates list of activities that is blank
    for line in file_list[2:]:
        line.strip()
        name, time, cost, enjoyment=line.split()
        activities.append({"name": name, "time":time, "cost": cost, "enjoyment": enjoyment}) #adds dictionary to list of activities
    print(activities)
    file.close()
    return n, time_max, cost_max, activities

#print(get_input("Inputs/input_10.txt"))
get_input("Inputs/input_10.txt")
