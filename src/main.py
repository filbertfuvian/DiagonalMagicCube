from localsearch import (generate_random_cube, stochastic_hill_climbing, simulated_annealing, genetic_algorithm, calculate_magic_score)
import matplotlib.pyplot as plt

def print_cube(cube):
    """Fungsi untuk menampilkan kubus 3D dengan cara yang mudah dibaca."""
    n = cube.shape[0]
    for z in range(n):
        print(f"Layer {z+1}:")
        print(cube[:, :, z])
        print()

def user_input():
    """Fungsi untuk meminta input dari pengguna."""
    print("Pilih metode pencarian lokal:")
    print("1. Stochastic Hill Climbing")
    print("2. Simulated Annealing")
    print("3. Genetic algorithm (Merandomize kubus lagi)")
    print("4. Randomize Cube")
    print("0. End")
    
    choice = int(input("Masukkan pilihan (1-4): "))
    return choice


def main():
    n = 5
    print("Membuat kubus acak 5x5x5...")
    cube = generate_random_cube(n)
    
    print("Kubus yang dihasilkan:")
    print_cube(cube)
    
    print(f"Skor Kubus Awal: {calculate_magic_score(cube)}")
    print()

    #Genetic algorithm
    population_size = 100

    while True:
        choice = user_input()
        
        if choice == 1:
            print()
            print("Menggunakan Stochastic Hill Climbing...")
            print()
            final_cube, final_score, data, time = stochastic_hill_climbing(cube)

        elif choice == 2:
            print()
            print("Menggunakan Simulated Annealing...")
            print()
            final_cube, final_score, data, probability_data, time = simulated_annealing(cube)

        elif choice == 3:
            print()
            print("Menggunakan Genetic Algorithm...")
            print()
            final_cube, final_score, best_score, avg_score, time = genetic_algorithm(5, population_size, 1000)

        elif choice == 4:
            print()
            print("Membuat kubus acak 5x5x5...")
            cube = generate_random_cube(n)
            print("Kubus yang dihasilkan:")
            print_cube(cube)
            print(f"Skor Kubus Awal: {calculate_magic_score(cube)}")
            print()
            continue

        elif choice == 0:
            print()
            print("Menghentikan program")
            print()
            return
        
        else:
            print()
            print("Input tidak valid")
            print()
            continue


        if (choice == 1):
            print("\nKubus yang ditemukan:")
            print_cube(final_cube)
            print(f"Skor magic cube akhir: {final_score}")

            iterations = list(data.keys())
            length_iterations = len(iterations)
            score = list(data.values())

            print(f'Numbers of iterations : {length_iterations} iterations')
            print(f'Time Elapsed : {time} s')

            # Supaya scatter plot tidak terlalu dense
            iterations = iterations[::len(iterations)//50]
            score = score[::len(score)//50]
            colors = score

            # Membuat scatter plot
            plt.scatter(iterations, score, c=colors, cmap='viridis')
            plt.title('Scatter Plot')
            plt.xlabel('Iterations')
            plt.ylabel('Score')
            
            plt.show()

        elif(choice ==2):
            print("\nKubus yang ditemukan:")
            print_cube(final_cube)
            print(f"Skor magic cube akhir: {final_score}")

            iterations = list(data.keys())
            length_iterations = len(iterations)
            score = list(data.values())
            probability = list(probability_data.values())

            print(f'Numbers of iterations : {length_iterations} iterations')
            print(f'Time Elapsed : {time} s')

            # Supaya scatter plot tidak terlalu dense
            iterations = iterations[::len(iterations)//50]
            iterations_copy = iterations
            score = score[::len(score)//50]
            probability = probability[::len(probability)//50]
            colors = score

            # Membuat scatter plot
            plt.scatter(iterations, score, c=colors, cmap='viridis')
            plt.title('Scatter Plot')
            plt.xlabel('Iterations')
            plt.ylabel('Score')
            
            plt.show()

            plt.scatter(iterations_copy, probability, color='red')
            plt.title('Scatter Plot')
            plt.xlabel('Iterations')
            plt.ylabel('e')

            plt.show()

        elif (choice == 3):
            print("\nKubus terbaik yang ditemukan:")
            print_cube(final_cube)
            print(f"Skor magic cube terbaik: {final_score}")
            
            generations = list(best_score.keys())
            length_generations = len(generations)
            best_score = list(best_score.values())
            avg_score = list(avg_score.values())

            print(f'Numbers of generation : {length_generations} generations')
            print(f'Population size : {population_size}')
            print(f'Time Elapsed : {time} s')

            # Supaya scatter plot tidak terlalu dense
            generations = generations[::len(generations)//50]
            best_score = best_score[::len(best_score)//50]
            avg_score = avg_score[::len(avg_score)//50]

            # Membuat scatter plot
            plt.scatter(generations, best_score, color = 'red', label = 'Best Score')
            plt.scatter(generations, avg_score, color = 'blue', label = 'Average Score')
            plt.title('Scatter Plot')
            plt.xlabel('Generations')
            
            plt.show()

if __name__ == "__main__":
    main()