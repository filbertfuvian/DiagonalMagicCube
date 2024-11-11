import random
import math
import numpy as np

def generate_random_cube(n):
    numbers = list(range(1, n**3 + 1))
    random.shuffle(numbers)
    
    cube = np.array(numbers).reshape(n, n, n)
    return cube

def calculate_magic_score(cube):
    n = cube.shape[0]
    magic_constant = (n*(n**3 + 1)) / 2
    score = 0

    # Row, column, and pillar checks
    for i in range(n):
        for j in range(n):
            # Sum rows along the z-axis
            row_sum = np.sum(cube[i, j, :])
            score += abs(magic_constant - row_sum)
            
            # Sum columns along the y-axis
            col_sum = np.sum(cube[i, :, j])
            score += abs(magic_constant - col_sum)
            
            # Sum pillars along the x-axis
            pillar_sum = np.sum(cube[:, i, j])
            score += abs(magic_constant - pillar_sum)

    # Face diagonals checks (on each layer perpendicular to each axis)
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

    # Face diagonals checks (on each layer perpendicular to each axis)
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

    return score

def generate_neighbor(cube):
    # Salin kubus agar perubahan tidak mempengaruhi kubus asli
    neighbor = cube.copy()
    n = neighbor.shape[0]
    
    # Pilih dua posisi acak dalam kubus untuk ditukar
    x1, y1, z1 = random.randint(0, n-1), random.randint(0, n-1), random.randint(0, n-1)
    x2, y2, z2 = random.randint(0, n-1), random.randint(0, n-1), random.randint(0, n-1)
    
    # Pastikan posisi berbeda
    while (x1, y1, z1) == (x2, y2, z2):
        x2, y2, z2 = random.randint(0, n-1), random.randint(0, n-1), random.randint(0, n-1)
    
    # Tukar dua elemen
    neighbor[x1, y1, z1], neighbor[x2, y2, z2] = neighbor[x2, y2, z2], neighbor[x1, y1, z1]
    
    return neighbor

def steepest_ascent(cube):
    current_cube = cube.copy()
    current_score = calculate_magic_score(current_cube)
    
    while True:
        best_neighbor = current_cube
        best_score = current_score
        
        # Coba beberapa tetangga untuk menemukan yang terbaik
        for _ in range(100):  # Lakukan 100 percobaan swap untuk mencari tetangga terbaik
            neighbor = generate_neighbor(current_cube)
            neighbor_score = calculate_magic_score(neighbor)
            
            if neighbor_score < best_score:
                best_neighbor = neighbor
                best_score = neighbor_score
        
        # Jika tidak ada perbaikan, berhenti
        if best_score >= current_score:
            return current_cube, current_score
        
        # Pindah ke tetangga terbaik
        current_cube = best_neighbor
        current_score = best_score


def hill_climb_with_sideways(cube, max_sideways_moves=100):
    current_cube = cube.copy()
    current_score = calculate_magic_score(current_cube)
    sideways_moves = 0
    
    while True:
        best_neighbor = current_cube
        best_score = current_score
        
        for _ in range(100):
            neighbor = generate_neighbor(current_cube)
            neighbor_score = calculate_magic_score(neighbor)
            
            # Pilih tetangga terbaik
            if neighbor_score < best_score:
                best_neighbor = neighbor
                best_score = neighbor_score
                sideways_moves = 0
            elif neighbor_score == best_score and sideways_moves < max_sideways_moves:
                best_neighbor = neighbor
                sideways_moves += 1
        
        # Jika tidak ada perbaikan dan batas sideways tercapai, berhenti
        if best_score >= current_score and sideways_moves >= max_sideways_moves:
            return current_cube, current_score
        
        # Pindah ke tetangga terbaik
        current_cube = best_neighbor
        current_score = best_score


def random_restart(cube, restarts=10):
    n = cube.shape[0]
    best_cube = cube.copy()
    best_score = calculate_magic_score(best_cube)
    
    for _ in range(restarts):
        # Mulai dengan kubus acak
        current_cube = generate_random_cube(n)
        final_cube, final_score = steepest_ascent(current_cube)  # Memakai steepest ascent atau metode lain
        
        # Periksa apakah hasil ini lebih baik
        if final_score < best_score:
            best_cube, best_score = final_cube, final_score
    
    return best_cube, best_score


def stochastic_hill_climbing(cube):
    n = cube.shape[0]
    current_cube = cube.copy()
    current_score = calculate_magic_score(current_cube)
    
    i = 0
    while (i < 10000):
        neighbor = generate_random_cube(n)
        neighbor_score = calculate_magic_score(neighbor)
        
        # Jika tetangga lebih baik, pindah
        if neighbor_score < current_score:
            current_cube = neighbor
            current_score = neighbor_score

        i+=1
    
    return current_cube, current_score



def simulated_annealing(cube, initial_temperature=100, cooling_rate=0.99, min_temperature=1):
    n = cube.shape[0]
    current_cube = cube.copy()
    current_score = calculate_magic_score(current_cube)
    temperature = initial_temperature
    
    while temperature > min_temperature:
        # Generate a neighbor
        neighbor = generate_random_cube(n)
        neighbor_score = calculate_magic_score(neighbor)
        
        # Hitung perbedaan skor
        delta_score = neighbor_score - current_score
        
        # Tentukan apakah akan menerima tetangga baru
        if delta_score < 0 or math.exp(-delta_score / temperature) > random.random():
            current_cube = neighbor
            current_score = neighbor_score
        
        # Turunkan suhu
        temperature *= cooling_rate
    
    return current_cube, current_score