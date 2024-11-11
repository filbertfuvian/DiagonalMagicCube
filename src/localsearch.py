import random
import math
import numpy as np
import time
import matplotlib.pyplot as plt

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
    space_diag1 = np.sum([cube[i, i, i] for i in range(n)])  # (0,0,0) to (n-1,n-1,n-1)
    space_diag2 = np.sum([cube[i, i, n - i - 1] for i in range(n)])  # (0,0,n-1) to (n-1,n-1,0)
    space_diag3 = np.sum([cube[i, n - i - 1, i] for i in range(n)])  # (0,n-1,0) to (n-1,0,n-1)
    space_diag4 = np.sum([cube[n - i - 1, i, i] for i in range(n)])  # (n-1,0,0) to (0,n-1,n-1)

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
        
        if delta_score < 0 or math.exp(-delta_score / temperature) > random.random():
            current_cube = neighbor
            current_score = neighbor_score
        
        score_per_iteration[i] = current_score
        i += 1
      
    return current_cube, current_score, score_per_iteration, elapsed_time

def crossover(parent1, parent2):
    n = parent1.shape[0]
    child = np.zeros_like(parent1)
    
    # Simple crossover: take half from parent1 and half from parent2
    for i in range(n):
        for j in range(n):
            if random.random() < 0.5:
                child[i, j, :] = parent1[i, j, :]
            else:
                child[i, j, :] = parent2[i, j, :]
    
    return child

def weighted_random_selection(population, scores):
    # Calculate inverse scores for weighting
    inverse_scores = [1 / (score + 1e-6) for score in scores]  # Adding a small value to avoid division by zero
    total_inverse_score = sum(inverse_scores)
    probabilities = [inv_score / total_inverse_score for inv_score in inverse_scores]
    
    return random.choices(population, weights=probabilities, k=2)

def genetic_algorithm(n, population_size=100, generations=1000, mutation_rate=0.1):
    # Initialize population
    population = [generate_random_cube(n) for _ in range(population_size)]
    scores = [calculate_magic_score(cube) for cube in population]
    
    for generation in range(generations):
        # Select parents based on their weighted scores
        selected_parents = weighted_random_selection(population, scores)

        # Create new population
        new_population = selected_parents.copy()

        # Crossover and mutation
        while len(new_population) < population_size:
            parent1, parent2 = weighted_random_selection(population, scores)
            child = crossover(parent1, parent2) q

            # Mutate the child
            if random.random() < mutation_rate:
                child = generate_random_neighbor(child)

            new_population.append(child)

        population = new_population
        scores = [calculate_magic_score(cube) for cube in population]

        # Print the best score of the generation
        best_score = min(scores)
        print(f"Generation {generation + 1}: Best Score = {best_score}")

    # Return the best solution found
    best_index = scores.index(min(scores))
    return population[best_index]


