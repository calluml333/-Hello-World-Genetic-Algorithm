"""
Student Name: Callum Little
Student Number: 201775475
Class: Advanced Topics in Software Engineering
Assignment: Hello World! GA Implementation
"""


import random as r
import operator
import sys
from timeit import default_timer



#_________________________________Parameters____________________________________


letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ! .'

# I used this string for simplicity. Could use ASCII table instead...

pop_size = 100      # Desired population size
generations = 1000  # Generations to iterate over 
                    #  - (generations only applies to genetic_algorithm_1)
                    
n = pop_size/2      # Number of winners from our tournament/selection
prob = 0.3          # The probability that a letter will be changed in the string
rate = 0.2          # The rate of mutation within the population
target_string = "Hello World!"
length_target = len(target_string)




#_________________________________Population____________________________________

def new_word(target_length): 
    """
    Generates a random string from letters which is the same length as the
    target word.
    """ 
            
    return ''.join(r.choice(letters) for _ in range(length_target))


def initial_pop(poulation, length):
    """
    Creates a list of words with the desired number of elements.
    """

    return [new_word(length) for i in range(pop_size)]
    


   
#____________________________________Fitness____________________________________

def calc_fitness(guess, target):
    """
    Compares the guess with the target. The score given is how many letters of 
    the guess are in the correct position compared to the target. 0 is the 
    lowest score and len(target) is the highest.
    """
    return sum(1.0 for expected, actual in zip(target, guess)
               if expected == actual)
               

def display_best(fitness):
    """
    Orders the fintees list from fittest to weakest. Then it displays the first
    element of the ordered list, which will be one of the elements that has the 
    highest fitness.
    """
    
    ordered = sorted(fitness, key=operator.itemgetter(1), reverse = True)
    print "Example of a Good Guess From This Generation and It's Fitness Value:", ordered[0], "\n"
    return


def fitness_function(population, target):
    """
    Iterates calc_fitness through the population and outputs a 
    list of arrays containing the guess and its score.
    """
    
    word_fitness = []
    for i in population:    
        fitness = calc_fitness(i, target)    
        word_fitness.append((i, fitness))   
    return word_fitness




#________________________________Selection______________________________________
        
# This would be used instead of a tournament to select only the n fittest of the 
# population for use as parents.

def selection(fitness, n):
    """
    Inputs the fintess list and the desired number of winners and then sorts 
    this list from fittest to weakest. It then selects the elements in the list 
    upu ntil n.
    """
    
    sort_fitness =  sorted(fitness, key=operator.itemgetter(1), reverse = True)
    fittest = sort_fitness[:n]
    return fittest
    
        


#_________________________________Tournament____________________________________

def tournament(fitness, n):
    """
    Takes the fitness list and selects two random elements from the list. It 
    then compares fitness values of these elements to choose the fittest of the 
    two. If the fitness values of the two elements are the same, the function 
    randomly selects one of them as the winner. The list of winners has a length
    of n.
    """
    
    winners = []
    while len(winners) < n: 
        word = [i for i in fitness]
        word_1 = r.choice(word)
        word_2 = r.choice(word)
    
        if word_1[1] > word_2[1]:
            winners.append(word_1)

        elif word_2[1] > word_1[1]:
            winners.append(word_2)
            
        elif word_1[1] == word_2[1]:
            choose = (word_1, word_2) 
            winner = r.choice(choose)
            winners.append(winner)
    return winners




#_________________________________Crossover_____________________________________

def merge(x):
    """
    Converts x, a list of tuples, to just a list.
    """
    
    final = []
    for i in x:
        final += i     
    return final

def crossover(parents, target):
    """
    Selects two random words from the list of fittest words as parents and then 
    seperates them at the xth carachter in the string. It then cretes two 
    childern from the split components of each parent. the output is a list of 
    sublists, where each sublist is the two children. 
    """
      
#    x = len(target)/2      # As to split each parent into half
    x = r.randint(1,len(target)-2) # Splits each parent at the same random point
                                   # in the string. The -2 is to account for 
                                   # the fact that a string has length x, but 
                                   # runs from the 0th to the (x-1)th character.
                                   # We then want to avoid starting the 
                                   # crossover function at the first or last 
                                   # letters, so we only wish to crossover
                                   # from the 1st to the (x-2)th character.   
    r.shuffle(parents)
    y = r.randint(1,len(parents)/2)*2    # chooses random number of parents
    new_parents = parents[:y]
    new_generation = []  
    while len(new_generation) < len(parents)-len(new_parents)/2:  
        #creating len(parents) - len(new_parents)/2 couples of childen = len(new_parents)
         
        word = [i[0] for i in new_parents]   # Removes fitness values

        parent_1 = r.choice(word)
        parent_2 = r.choice(word) 
    
        child_1 = parent_1[:x] + parent_2[x:]
        child_2 = parent_2[:x] + parent_1[x:]
        
        children = child_1, child_2
        new_generation.append(children) 
        
    updated_generation = merge(new_generation)
    r.shuffle(updated_generation)    
    final_new_generation = word + updated_generation
    return final_new_generation
    

#__________________________________Mutation_____________________________________

def mutation(population, probability, mutation_rate):
    """
    Starts by shuffling the inputted population elements so that their orded in 
    the list will be randomised. Then the first x elements of the shuffled list 
    are Selected for mutation.
    
    The function then looks at every string in those x elements and generates
    a random number between 0 & 1 for every letter. If this random number is 
    less than some pre-determied "probability" then another randomly chosen 
    letter is selected from the "letters" string to replace it. If the 
    probability is higher, the letter remains the same.
    
    These mutated elements are then re-introduced back into the population, 
    which is then shuffled again to keep the randomess. 
    """

    r.shuffle(population)      # Shuffle population to create a randoom order to allow random mutation
    x = int(len(population)*mutation_rate)
    population_to_mutate = population[:x]   # Picks first x elements to mutate
    new_strings = []
    i = 0            
    
    while i < len(population_to_mutate):
        string = population_to_mutate[i]
        j = 0
        
        while j < len(string):
            value = r.random()
            if value < probability:
                new_letter = r.choice(letters)
                string = string[:j] + new_letter + string[j+1:]  #creates new string
                j += 1
            else:
                string = string    # String remains unchanged
                j += 1
        i += 1
        new_strings.append(string)

    mutated_population = new_strings + population[x:]   # Combine mutated elements with untouched elements from population
    r.shuffle(mutated_population)     # Shuffle again to maintain randomness
    return mutated_population
           
    


#________________________________Iteration__________________________________


def genetic_algorithm_1(target, size,  length, generations, number_of_winners, mutation_prob, mutation_rate):
    """
    Initializes the population using initial_pop(). Then for a specified number 
    of generations the function then calculates the fitness of the population,
    selects parents using the selection OR tournament functions, creates a new
    population using the crossover function and finally mutates some of the
    new population using the mutation function to create the next generation. 
    
    If the target is recahed within the given number of generations, the 
    function will stop and display the generation at which the algorithm 
    succeeded.
    
    If the target is not reached within the given number of gnerations, the 
    function will print a message confirming this and also print the final
    generation list.    
    """
    
    start = default_timer()
    population = initial_pop(size, length)
    print(population)   
    i = 0
    while i < generations:
        print "Generation: ", str(i)        
        fitness = fitness_function(population, target)        
        display_best(fitness)
        #winners = selection(fitness, number_of_winners)        # Creates winners using selection()
        winners = tournament(fitness, number_of_winners)        # Creates winners using tournament()
        new_gen = crossover(winners, target)
        population = mutation(new_gen, mutation_prob, mutation_rate)                    
        i += 1
        
        j = 0
        while j < len(fitness):
            fit = fitness[j]
            if [fit] == fitness_function([target], target):
                print "Target Reached:", '"{}"'.format(fit[0]), "|", str(i), "Generations,", default_timer()-start, "seconds."
                sys.exit() 
            j += 1      
    print "Target Not Reached in", generations, "Generations.", "Time Taken:", default_timer()-start, "seconds.", "The Final Population is: \n"
    print(new_gen)
    return new_gen




def genetic_algorithm_2(target, size,  length, number_of_winners, mutation_prob, mutation_rate):
    """
    Initializes the population using initial_pop(). The function then calculates
    the fitness of the population, selects parents using the selection OR 
    tournament function, creates a new population using the crossover function 
    and finally mutates some of the new population using the mutation function
    to create the new generation. 
    
    The function will continue to run until the target has been reached. At this 
    point the function will stop and display at the generation at which the 
    algorithm succeeded and the time value.
    
    If the target is not reached within the given number of gnerations, the 
    function will print a message confirming this, the time taken 
    and the final population.    
    """
    
    start = default_timer()
    population = initial_pop(size, length)    
    i = 0
    for string in population:
        while string != target:
            print "Generation:", str(i)
            fitness = fitness_function(population,target)        
            display_best(fitness)
            #winners = selection(fitness, number_of_winners)        # Creates winners using selection()
            winners = tournament(fitness, number_of_winners)        # Creates winners using tournament()
            new_gen = crossover(winners, target)
            population = mutation(new_gen, mutation_prob, mutation_rate)
            
            j = 0       
            while j < len(fitness):
                fit = fitness[j]
                if [fit] == fitness_function([target], target):
                    print "Target Reached:", '"{}"'.format(fit[0]), "|", str(i), "Generations,", default_timer()-start, "seconds."
                    sys.exit() 
                j += 1                    
            i += 1                 
    return 


#___________________________________RUN_________________________________________

"""
You can uncomment the algorithm that you wish to run. The first is the 
generation-dependant algorithm, the second continues to run until completion. 
"""

#genetic_algorithm_1(target_string, pop_size, length_target, generations,  n, prob, rate)

genetic_algorithm_2(target_string, pop_size, length_target, n, prob, rate)




