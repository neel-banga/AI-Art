from PIL import Image
from random import randint, randrange, choices
import numpy as np
import fitness

np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)

def save_image(data, path):
    image = Image.fromarray(data)
    image.save(path)

def generate_genome():
    data = np.zeros((fitness.FRAME, fitness.FRAME, 3), dtype=np.uint8)
    combos = fitness.make_combos()
    for i in range(len(combos)):
        x, y = combos[i]
        data[y-1][x-1] = (randrange(256), randrange(256), randrange(256))

    save_image(data, 'image.png')
    return list(data)

def generate_population(population_size):
    return [generate_genome() for _ in range(population_size)]

def selection(population, fitness_scores):
    return choices(population=population, weights=fitness_scores, k=2)

def crossing_over(genome1, genome2):

    if len(genome1) != len(genome2):
        raise ValueError('Genomes must be of equal size')

    if len(genome1) < 2:
        return genome1, genome2
    
    genome1, genome2 = list(genome1), list(genome2) # make sure its not a numpy array

    index = randint(0, len(genome1)-1)
    return genome1[0:index]+genome2[index:], genome2[0:index]+genome1[index:]

def mutation(genome, mutations_amt, probability=0.4):
    genome = list(genome) # make sure it's not a numpy array
    probability = 10 - (int(probability*10))
    for _ in range(mutations_amt):

        index = randint(0, len(genome)-1)
        if randint(0, 10) > probability:
            genome[index] = (randrange(256), randrange(256), randrange(256))
             
    return genome

def evolve(fitness_limit=15, generation_limit = 100):

    population = generate_population(6)

    for i in range(generation_limit):
        print(f'Generation {i}')

        fitness_scores = []
        for genome in population:
            # here is where we face a problem
            print(genome[0])
            fitness.save_image(np.array(genome), 'fitness.png')
            fitness_scores.append(fitness.fitness('fitness.png'))

        sorted_population = sorted(range(len(population)), key=lambda x: fitness_scores[x], reverse=True)

        best_index = sorted_population[0]

        #if fitness_scores[best_index] >= fitness_limit: fix fitness limit
        #    break
        fitness.save_image(np.array(population[best_index]), 'image.png')
        next_generation = [population[0], population[1]]

        for i in range(2):
            parents = selection(population, fitness_scores) # This function takes fitness
            child1, child2 = crossing_over(parents[0], parents[1])

            next_generation += [child1, child2]

        next_generation = [mutation(genome, mutations_amt=randint(0, 5)) for genome in next_generation]

        population = next_generation

    return population


evolve()

x = generate_population(2)
a, y = crossing_over(x[0], x[1])
# convert back to numpy
# so normal array for literally everything except for numpy

a = np.array(a)
fitness.save_image(a, 'image.png')