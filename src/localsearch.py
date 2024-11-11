import random
import math
import numpy as np
import time

def generate_random_cube(n):
    numbers = list(range(1, n**3 + 1))
    random.shuffle(numbers)
    
    cube = np.array(numbers).reshape(n, n, n)
    return cube

def calculate_magic_score(cube):
    n = cube.shape[0]
    magic_constant = (n*(n**3 + 1)) / 2
    score = 0

    for i in range(n):
        for j in range(n):
            # rows 
            row_sum = np.sum(cube[i, j, :])
            score += abs(magic_constant - row_sum)
            
            # columns
            col_sum = np.sum(cube[i, :, j])
            score += abs(magic_constant - col_sum)
            
            # pillars
            pillar_sum = np.sum(cube[:, i, j])
            score += abs(magic_constant - pillar_sum)

    # Face diagonals
    for i in range(n):
        # Diagonals on xy planes (constant z)
        face_diag1 = np.sum([cube[j, j, i] for j in range(n)])
        face_diag2 = np.sum([cube[j, n - j - 1, i] for j in range(n)])
        score += abs(magic_constant - face_diag1)
        score += abs(magic_constant - face_diag2)
        
        # Diagonals on xz planes (constant y)
        face_diag3 = np.sum([cube[j, i, j] for j in range(n)])
        face_diag4 = np.sum([cube[n - j - 1, i, j] for j in range(n)])
        score += abs(magic_constant - face_diag3)
        score += abs(magic_constant - face_diag4)
        
        # Diagonals on yz planes (constant x)
        face_diag5 = np.sum([cube[i, j, j] for j in range(n)])
        face_diag6 = np.sum([cube[i, j, n - j - 1] for j in range(n)])
        score += abs(magic_constant - face_diag5)
        score += abs(magic_constant - face_diag6)

    # Space diagonals
    space_diag1 = np.sum([cube[i, i, i] for i in range(n)])  
    space_diag2 = np.sum([cube[i, i, n - i - 1] for i in range(n)]) 
    space_diag3 = np.sum([cube[i, n - i - 1, i] for i in range(n)]) 
    space_diag4 = np.sum([cube[n - i - 1, i, i] for i in range(n)]) 

    score += abs(magic_constant - space_diag1)
    score += abs(magic_constant - space_diag2)
    score += abs(magic_constant - space_diag3)
    score += abs(magic_constant - space_diag4)

    return score

def generate_random_neighbor(cube):
    neighbor = cube.copy()
    n = neighbor.shape[0]
    
    x1, y1, z1 = random.randint(0, n-1), random.randint(0, n-1), random.randint(0, n-1)
    x2, y2, z2 = random.randint(0, n-1), random.randint(0, n-1), random.randint(0, n-1)
    
    # Memastikan posisi berbeda
    while (x1, y1, z1) == (x2, y2, z2):
        x2, y2, z2 = random.randint(0, n-1), random.randint(0, n-1), random.randint(0, n-1)
    
    # Tukar dua elemen
    neighbor[x1, y1, z1], neighbor[x2, y2, z2] = neighbor[x2, y2, z2], neighbor[x1, y1, z1]
    
    return neighbor

def crossover(parent1, parent2, crossoverpoint):
    n = parent1.shape[0]
    child = np.zeros_like(parent1)
    
    for i in range(n):
        for j in range(n):
            if i < crossoverpoint:
                child[i, j, :] = parent1[i, j, :]
            else:
                child[i, j, :] = parent2[i, j, :]

    return child

def selection(population, scores):
    # Score di inverse agar socre makin kecil makin tinggi probabilitasnya
    inverse_scores = [(1 / score) for score in scores]  
    total_inverse_score = sum(inverse_scores)
    probabilities = [inv_score / total_inverse_score for inv_score in inverse_scores]
    
    return random.choices(population, weights=probabilities, k=len(population))

def stochastic_hill_climbing(cube, nmax=60000):
    current_cube = cube.copy()
    current_score = calculate_magic_score(current_cube)
    score_per_iteration = dict()
    start_time = time.time()

    i = 0
    while (i < nmax):
        neighbor = generate_random_neighbor(current_cube)
        neighbor_score = calculate_magic_score(neighbor)
        
        if neighbor_score < current_score:
            current_cube = neighbor
            current_score = neighbor_score

        score_per_iteration[i] = current_score
        i+=1

    elapsed_time = time.time() - start_time

    return current_cube, current_score, score_per_iteration, elapsed_time

def simulated_annealing(cube, initial_temperature=100, min_temperature=1):
    current_cube = cube.copy()
    current_score = calculate_magic_score(current_cube)
    score_per_iteration = dict()
    probability_per_iteration = dict()

    start_time = time.time()
    
    i = 0
    while True:
        elapsed_time = time.time() - start_time
        
        temperature = initial_temperature * (1 - elapsed_time / 60)  
        if temperature < min_temperature:
            break 
        
        neighbor = generate_random_neighbor(current_cube)
        neighbor_score = calculate_magic_score(neighbor)
        
        delta_score = neighbor_score - current_score

        probability = math.exp(-delta_score / temperature)
        
        if delta_score < 0 or probability > random.random():
            current_cube = neighbor
            current_score = neighbor_score
        
        score_per_iteration[i] = current_score
        probability_per_iteration[i] = probability

        i += 1
      
    return current_cube, current_score, score_per_iteration, probability_per_iteration, elapsed_time

def genetic_algorithm(n, population_size=100, generations=1000, mutation_rate=0.1):
    # Initialize population
    population = [generate_random_cube(n) for _ in range(population_size)]
    scores = [calculate_magic_score(cube) for cube in population]
    bestscore_per_iteration = dict()
    avgscore_per_iteration = dict()
    bestcube_per_iteration = dict()
    start_time = time.time()
    
    for generation in range(generations):
        # Selection
        selected_parents = selection(population, scores)
        # Create new population
        new_population = selected_parents.copy()

        child = []

        # Crossover
        for i in range(0,len(new_population),2):
            child.append(crossover(new_population[i], new_population[i+1], 2))
            child.append(crossover(new_population[i+1], new_population[i], 2))

        new_population = child.copy()

        # Mutation
        for i in range(len(new_population)):
            if random.random() < mutation_rate:
                new_population[i] = generate_random_neighbor(new_population[i])


        population = new_population
        scores = [calculate_magic_score(cube) for cube in population]
        
        best_score = min(scores)
        avg_score = sum(scores) / len(scores)
        bestscore_per_iteration[generation] = best_score
        avgscore_per_iteration[generation] = avg_score

        best_index = scores.index(min(scores))
        bestcube_per_iteration[generation] = population[best_index]

    elapsed_time = time.time() - start_time

    best_generation = min(bestscore_per_iteration, key=bestscore_per_iteration.get)
    best_cube = bestcube_per_iteration[best_generation]
    best_score = bestscore_per_iteration[best_generation]
    
    return best_cube, best_score, bestscore_per_iteration, avgscore_per_iteration, elapsed_time
