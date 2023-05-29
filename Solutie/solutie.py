import sys
import os
import time
import random
from typing import Union

def getLines(nameOfFile) -> list:
    # List to include all lines of file
    file_lines: list = []
    
    # Populating the list of file lines
    with open(f'Subiect concurs de programare\{nameOfFile}', "r", encoding="utf-8") as file_in:
        file_lines.append(file_in.readlines())

    return file_lines


def getCoordinates(list: list) -> list:
    # List of all coordinates in test file 
    coordinates_list = []
    
    # Index of where the coordinates start and end in the test file
    index_start: int = list.index("NODE_COORD_SECTION\n") + 1
    index_end: int = list.index("GTSP_SET_SECTION:\n")
    
    # Appending the coordinates in the form of a tuple to the coordinates list
    for index in range(index_start, index_end):
        coords = list[index].strip('\n').split()
        coordinates_list.append(tuple(map(int, coords)))
    
    return coordinates_list


def distanceCalculator(point1: tuple, point2: tuple) -> int:
    # Putting tuple items in variables representing index of said point, x and y coordinates of said point
    index1, x1, y1 = point1
    index2, x2, y2 = point2
    
    return int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** (1 / 2) + 0.5)


def nearestNeighbour(points: list, points_to_visit: int) -> Union[list, int]:
    # Initialize the path to be empty
    shortest_path = None
    
    # Determine a very big integer to compare the distance to
    max_int = sys.maxsize
    shortest_distance = max_int

    for start_point in points:
        remaining_points = set(points)
        remaining_points.remove(start_point)
        current_point = start_point
        path = [current_point[0]]
        total_distance = 0

        for index in range(points_to_visit - 1):
            nearest_point = min(remaining_points, key=lambda x: distanceCalculator(current_point, x))
            total_distance += distanceCalculator(current_point, nearest_point)
            current_point = nearest_point
            remaining_points.remove(nearest_point)
            path.append(current_point[0])

        path.append(path[0])

        # Add distance to return to the starting point
        # print(distanceCalculator((9, 52, 33), (16, 52, 41))) # Testing distanceCalculator
        total_distance += distanceCalculator(current_point, start_point)

        if total_distance < shortest_distance:
            shortest_distance = total_distance
            shortest_path = path

    return shortest_path, shortest_distance
    

def populateOutputFile(file_name: str, path: list, total_distance: int):
    try:
        with open(f'Solutie\Raspunsuri\{file_name}', "w", encoding="utf-8") as file_out:
            file_out.write("--- Puncte vizitate\n") 
            file_out.write(str(len(path) - 1) + '\n')
            file_out.write("--- Ordinea de vizitare\n")
            path_str: str = ','.join(str(index) for index in path)
            file_out.write(path_str + '\n')
            file_out.write("--- Distanța totală calculată\n")
            file_out.write(str(total_distance))
            
        print(f'{file_name}: done')
    except:
        print(f'{file_name}: error')
        

def iterateThroughAllTestFiles():
    start_time = time.time()
    
    folder_path: str = 'Subiect concurs de programare'
    
    for file_name in os.listdir(folder_path):
        start_time_for_each_file = time.time()
        # Getting the name of the input and output files
        input_file: str = file_name
        output_file: str = input_file[:-5] + '.sol'
        
        # Get each line of the input file
        lines = getLines(input_file)[0]
        
        # Getting the dimention and procent values
        # dimension: int = int(lines[3][12:-1])
        dimension: int = int(lines[3].split(" ")[-1])
        # percent: int = int(input("Introduceți numarul p: "))
        percent: int = random.randint(1, 100)
        # percent: int = 100

        # Getting the number of points that need to be tresspassed 
        number_of_points: int = int(dimension * percent / 100)
        
        # Getting the coordinates of each point
        coordinates_list = getCoordinates(lines)

        # Getting the list of points travelled and the shortest distance
        path, distance = nearestNeighbour(coordinates_list, number_of_points)
        
        # Outputting to the output file
        populateOutputFile(output_file, path, distance)
        
        end_time_for_each_file = time.time()
        
        elapsed_time_for_each_file = end_time_for_each_file - start_time_for_each_file
        
        print(f'Elapsed time for {input_file} is: {elapsed_time_for_each_file} seconds with {percent}% of total points ({number_of_points} points)')

    end_time = time.time()
    
    elapsed_time = end_time - start_time
    
    print(f'Elapsed time: {elapsed_time} seconds')


if __name__ == "__main__":
    iterate: str = input("Do you want to iterate through all the test files? (yes/no): ")
    
    iterate_through_all_test_files: bool = False
    
    if iterate.lower() == 'yes':
        iterate_through_all_test_files = True
    elif iterate.lower() == 'no':
        iterate_through_all_test_files = False
    else:
        print("You introduced an invalid input.")
    
    
    if iterate_through_all_test_files is True:
        print("Iterating through all test files.")
        iterateThroughAllTestFiles()
    else:
        start_time = time.time()
        # Getting the name of the input and output files
        input_file: str = input("Introduceți numele fișierului de intrare: ")
        output_file: str = input_file[:-5] + '.sol'
        
        # Get each line of the input file
        lines = getLines(input_file)[0]
        
        # Getting the dimention and procent values
        # dimension: int = int(lines[3][12:-1])
        dimension: int = int(lines[3].split(" ")[-1])
        percent: int = int(input("Introduceți numarul p: "))

        # Getting the number of points that need to be tresspassed 
        number_of_points: int = int(dimension * percent / 100)
        
        # Getting the coordinates of each point
        coordinates_list = getCoordinates(lines)

        # Getting the list of points travelled and the shortest distance
        path, distance = nearestNeighbour(coordinates_list, number_of_points)
        
        # Outputting to the output file
        populateOutputFile(output_file, path, distance)
        
        end_time = time.time()
        
        elapsed_time = end_time - start_time
        
        print(f'Elapsed time for {input_file} is: {elapsed_time} seconds with {percent}% of total points ({number_of_points} points)')