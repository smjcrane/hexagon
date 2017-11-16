import random

def play(board, colour):
    mine = []
    allowed = []
    for t in board.tiles:
        if t.colour == colour:
            mine.append(t)
    for t in mine:
        for n in t.neighbours:
            m = board.tile_lookup[n]
            if m.colour == 0:
                allowed.append((t, m))
    if len(allowed) > 0:
        move = random.choice(allowed)
        board.clone(move[0], move[1])


#start genetics
        
import random
import sys
from answer import is_answer, get_mean_score
# You can redefine these functions with the ones you wrote previously.
# Another implementation is provided here.
from encoding import create_chromosome
from tools import selection, crossover, mutation

def create_population(pop_size, chrom_size):
    # use the previously defined create_chromosome(size) function
    # TODO: create the base population
    chrom = []
    for i in range(pop_size):
        chrom.append(create_chromosome(chrom_size))
    return chrom
    
def generation(population):
    
    # selection
    # use the selection(population) function created on exercise 2
    select = selection(population)
    
    # reproduction
    # As long as we need individuals in the new population, fill it with children
    children = []
    # TODO: implement the reproduction
    while len(children) < len(population):
        ## crossover
        parent1 = random.choice(select) # randomly selected
        parent2 = random.choice(select) # randomly selected
        # use the crossover(parent1, parent2) function created on exercise 2
        child = crossover(parent1, parent2)
        
        ## mutation
        # use the mutation(child) function created on exercise 2
        child = mutation(child)
        children.append(child)
    
    # return the new generation
    return select + children

def algorithm():
    chrom_size = int(input())
    population_size = 10
    
    # create the base population
    population = create_population(population_size, chrom_size)
    
    answers = []
    
    # while a solution has not been found :
    while not answers:
        ## create the next generation
        # TODO: create the next generation using the generation(population) function
        population = generation(population)
        
        ## display the average score of the population (watch it improve)
        print(get_mean_score(population), file=sys.stderr)
    
        ## check if a solution has been found
        for chrom in population:
            if is_answer(chrom):
                answers.append(chrom)
    
    # TODO: print the solution
    print(answers)
    
