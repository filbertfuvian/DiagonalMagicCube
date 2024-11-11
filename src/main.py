from localsearch import (generate_random_cube, steepest_ascent, hill_climb_with_sideways, random_restart, 
                          stochastic_hill_climbing, simulated_annealing, calculate_magic_score)

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
    print("1. Steepest Ascent Hill Climbing")
    print("2. Hill Climbing with Sideways Moves")
    print("3. Random Restart Hill Climbing")
    print("4. Stochastic Hill Climbing")
    print("5. Simulated Annealing")
    
    choice = int(input("Masukkan pilihan (1-5): "))
    return choice


def main():
    # Membuat kubus acak 5x5x5
    n = 5
    print("Membuat kubus acak 5x5x5...")
    cube = generate_random_cube(n)
    
    print("Kubus yang dihasilkan:")
    print_cube(cube)
    
    print(f"Skor Kubus Awal: {calculate_magic_score(cube)}")
    print()
    # Memilih metode pencarian lokal
    choice = user_input()
    
    # Menjalankan pencarian lokal berdasarkan pilihan
    if choice == 1:
        print("Menggunakan Steepest Ascent Hill Climbing...")
        final_cube, final_score = steepest_ascent(cube)
    elif choice == 2:
        print("Menggunakan Hill Climbing with Sideways Moves...")
        final_cube, final_score = hill_climb_with_sideways(cube)
    elif choice == 3:
        print("Menggunakan Random Restart Hill Climbing...")
        final_cube, final_score = random_restart(cube)
    elif choice == 4:
        print("Menggunakan Stochastic Hill Climbing...")
        final_cube, final_score = stochastic_hill_climbing(cube)
    elif choice == 5:
        print("Menggunakan Simulated Annealing...")
        final_cube, final_score = simulated_annealing(cube)
    else:
        print("Pilihan tidak valid. Menghentikan program.")
        return

    # Menampilkan hasil akhir
    print("\nKubus yang ditemukan:")
    print_cube(final_cube)
    print(f"Skor magic cube akhir: {final_score}")
    # print(f"Magic constant: {n * (n**3 + 1) // 2}")

if __name__ == "__main__":
    main()