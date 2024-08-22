import random
import string 

#mySecretPassword = "649908896413"
mySecretPassword = "z49ai8P894"
untrustedPassword = b''
passwordSize = 10
# -------------------------------------------- # 

def generate_digit_password(length):
    """"
     Define the pool
        - ascii_letters : abcdefghijklmnopqrstuvwxyz & ABCDEFGHIJKLMNOPQRSTUVWXYZ
        - digits : 0123456789
    """
    chars = string.ascii_letters + string.digits
    
    
    password = ''.join(random.choice(chars) for i in range(length))
    
    return password
# -------------------------------------------- #

# --------------------- #

def generate_population(pop_size, chromosome_length):
    """
    This function generate members of the population. 
    """
    population = []

    for i in range(pop_size):
        chromosome = generate_digit_password(chromosome_length)
        
        # Set fitness to 0, not evaluate yet
        row = [0, chromosome]
        
        population.append(row)

    
    return population

# --------------------- # 

def evaluate_fitness(chromosome, pop_size):
    """
    This function evaluate the fitness of each member of the population.
    The more fitness tend to 1 the better is. 
    """
    population = []

    for i in range(pop_size):
        #fitness = verifyPassword(mySecretPassword,chromosome[i].decode('utf-8'))
        fitness = verifyPassword(mySecretPassword,chromosome[i][1])
        #fitness = random.uniform(0, 1)
        row = [fitness, chromosome[i][1]]
        population.append(row)
    
    return population

# --------------------- # 

def select_parents(population, num_of_parent, elitism_percentage):
    """
    This function select members of population based on elitism criteria and tournament.  
    """
    parents = []

    # Step 1 is "Elitism", select the best parents to reproduce
    # Compute number of elite parents
    elit_folks =  int((elitism_percentage/100)*100)
    #print (elit_folks)
    
    # Compute number of random parents
    randomParent_folks =  int(num_of_parent-elit_folks)
    
    i = 0
    
    while i  < elit_folks:
        parents.append(population[i])
        i += 1

    # Step 2 is "Tournament", select the random parents to reproduce with the elite
    for j in range(randomParent_folks): 
        #for i in population:
            # Pick parent 1 from the population
            parent1 = population[random.randint(0, len(population)-1)]
            parent1Fitness = parent1[0]
        
            # Pick parent 2 from the population
            parent2 = population[random.randint(0, len(population)-1)]
            parent2Fitness = parent2[0]
        
            # Choose the best of both
            if parent1Fitness > parent2Fitness:
                parents.append(parent1)
            else:
                parents.append(parent2)
    
    return parents

# --------------------- # 

def crossover_and_mutate(parents, offspring_size, mutation_rate):
    # Initialize the child pool 
    offspring = []
    
    #for i in range(offspring_size):
    i = 0
    while i < offspring_size:
        
        # Pick parent 1 from the population
        parent1 = random.choice(parents)
        parent1Fitness = parent1[0]
        parent1Password = parent1[1]
        
        # Pick parent 2 from the population
        parent2 = random.choice(parents)
        parent2Fitness = parent2[0]
        parent2Password = parent2[1]

        # Initialize empty child
        childPassword = ""
        
        # Compare parents and always keep cross the best parents against the poor one
        if parent1Fitness > parent2Fitness:
            
            # Find the crossover point
            # i.e. Parent1 = 12354 and Parent2 = 12784 and the password we are looking for is 12345. 
            # crossover point will be Parent1 = 123_54
            # Child will look like this : 123_84
            crossover_point = int(parent1Fitness*passwordSize)
        
            childPassword += (parent1Password[:crossover_point])
            childPassword += (parent2Password[crossover_point:])

            # Set child fitness to 0, not evaluate yet
            child = [0, childPassword]
            offspring.append(child)
        
        # Same as above
        elif parent1Fitness < parent2Fitness:
            crossover_point = int(parent2Fitness*passwordSize)
        
            childPassword += (parent2Password[:crossover_point])
            childPassword += (parent1Password[crossover_point:])

            child = [0, childPassword]
            offspring.append(child)
        
        # If Parent1 and 2 are equal, choose parent2 for the cross (this is totally arbitrary)
        else:
            crossover_point = int(parent2Fitness*passwordSize)
        
            childPassword += (parent2Password[:crossover_point])
            childPassword += (parent1Password[crossover_point:])

            child = [0, childPassword]
            offspring.append(child)
        
            # Add some imperfections to prevent too much elitism for the next generations  
            # For each child 
            for i in range(len(offspring)):
                # Select random character to change 
                for j in range(len(offspring[i][1])):
            
                    # Pick randomly a number and if it's less than the mutation rate, mutate the child
                    if random.uniform(0, 1) < mutation_rate:
                        #offspring[0][1] = offspring[0][1].replace(random.choice(offspring[0][1]),random.choice(string.digits))
                        offspring[0][1] = offspring[0][1].replace(random.choice(offspring[0][1]),random.choice(string.digits + string.ascii_letters))
                        
        i += 1
    
    return offspring


# ------------------------------------------------------ # 

def verifyPassword(password, u_password):
    # Get password length   
    if type(password) == str:
        passwordLength = len(password)
    else:
        raise TypeError("invalid u_password type : ", type(u_password))
    # Get the user password length  
    if type(u_password) == str:
        u_passwordLength = len(u_password) 
    else:
        raise TypeError("invalid u_password type : ", type(u_password))
    
    # Initialize comparator counter 
    i = 0
    j = 0
    
    while(i < passwordLength and j < u_passwordLength):
        # Compare character by character 
        if password[i] != u_password[j]:
            # Fake function to emulate the timing attack
            # In case of mismatch. Compute verification ratio, more it tend to 1 the more likely is the password
            ratio = j / passwordLength
            return ratio

        # and to the next character.
        i += 1
        j += 1
    #Return True if the user password match the real password.  
    return True

# ------------------------------------------------------ #

# Maximum number of iterations 
num_of_generations = 500

# Generate the initial password population
passwordPopulation = generate_population(20000, passwordSize)

for i in range(num_of_generations):
    
    # Step 1 : Evaluate the population 
    passwordPopulation = evaluate_fitness(passwordPopulation, len(passwordPopulation))
    
    for _ in range (0, 3):
        print(passwordPopulation[_])

    # Step 2 : Check if password is found     
    for x  in passwordPopulation:
        if x[0] == True:
            found = x
            raise Exception("Password found : ", found, " After : ", i, "iterations")
        else:
            found = None 
    # Step 3 : Select parents for the new generations
    parents = select_parents(sorted(passwordPopulation, reverse=True), 2500, 85)
    
    
    # Step 4 : Cross the parents and mutate some childs
    childs = crossover_and_mutate(parents, 2500, 0.5)

    # Step 5 : Renew the population 
    passwordPopulation = childs
    

print(passwordPopulation)