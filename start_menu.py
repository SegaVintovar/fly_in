import glob
import subprocess

running = True
while running:
    all_the_maps = glob.glob("maps/**/*.txt")
    print("Choose the map:")
    for i in range(len(all_the_maps)):
        print(f"{i + 1}. {all_the_maps[i]}")
    print("Enter 0(Zero) to quit!")
    try:
        next_map = int(input("Your choice: ")) - 1
    except ValueError:
        print(f"Choice has to be an int in range {len(all_the_maps)}")
    else:
        if next_map == -1:
            running = False
        else:
            subprocess.run(
                ["virt_env/bin/python3", "main.py", all_the_maps[next_map]])
