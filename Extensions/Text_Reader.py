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

#print(get_input("Inputs/input_10.txt"))