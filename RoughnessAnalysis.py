import skimage.io
import skimage.color
import skimage.filters
import statistics
import numpy as np
import matplotlib.pyplot as plt
import math as m
from PIL import Image

def read_image(path):
    return Image.open(path)

def is_white(pixel):
    if isinstance(pixel, int):
        return pixel > 0
    else:
        return pixel[0] >= 150 and pixel[1] >= 150 and pixel[2] >= 150

def is_black(pixel):
   return not is_white(pixel)

def contains(element, array):

    for current in array:
        if element[0] == current[0] and element[1] == current[1]:
            return True

    return False

def get_neighbors(current, allpoints, process, chain):
    neighbors = []

    for point in allpoints:
        if current[0] == point[0] and current[1] == point[1]:
            continue

        if abs(current[0] - point[0]) <= 1 and abs(current[1] - point[1]) <= 1:
            if not contains(point, chain) and not contains(point, process):
                neighbors.append(point)

    return neighbors

def create_chain(allpoints, process, chain):

    chain.append(process[0])

    neighbors = get_neighbors(process[0], allpoints, process, chain)
    for neighbor in neighbors:
        process.append(neighbor)

    process.pop(0)

    pass

def find_chain(allpoints):
    chain = []
    process = []

    process.append(allpoints[0])

    while len(process) > 0:
        create_chain(allpoints, process, chain)

    return chain

def find_border_points(image):
    all_points = np.array([[0,0]])

    topLeftPixel = image.getpixel((0, 0))
    isSEM = is_black(topLeftPixel)
    isTEM = not isSEM

    for y in range(50, 1380):
        for x in range(300, 1750):
            pixel = image.getpixel((x, y))
            if (isSEM and is_white(pixel)) or (isTEM and is_black(pixel)):
                border_found = False
                for neighborhood_y in range(y - 1, y + 2):
                    for neighborhood_x in range(x - 1, x + 2):
                        if not border_found:
                            neighborhood_pixel = image.getpixel((neighborhood_x, neighborhood_y))
                            if (isSEM and is_black(neighborhood_pixel)) or (isTEM and is_white(neighborhood_pixel)):
                                border_found = True
                                point = np.array([[x,y]])
                                all_points = np.append(all_points, point, axis = 0)
                                #print(point)

    all_points = np.delete(all_points, 0, 0)

    print("Started finding real border")
    border = find_chain(all_points)
    print("Finished finding real border")

    return border

def plot_border_points(sample_name, image, border_points):
    edited_image = image.copy()
    for point in border_points:
       # print(point)
        edited_image.putpixel((point[0], point[1]), (255, 0, 0, 255))

    #edited_image.show()
    edited_image.save(sample_name + '_border.png')
    return

def calculate_initial_center(border_points):
    initial_center = np.average(border_points, axis=0)
    #print("center X,Y is ", initial_center)
    return initial_center

def search_left(optimized_center, border_points, current_stdev):
    return search_direction(-1, 0, optimized_center, border_points, current_stdev)

def search_right(optimized_center, border_points, current_stdev):
    return search_direction(1, 0, optimized_center, border_points, current_stdev)

def search_up(optimized_center, border_points, current_stdev):
    return search_direction(0, -1, optimized_center, border_points, current_stdev)

def search_down(optimized_center, border_points, current_stdev):
    return search_direction(0, 1, optimized_center, border_points, current_stdev)

def search_direction(delta_x, delta_y, optimized_center, border_points, current_stdev):
    potential_center = (optimized_center[0] + delta_x, optimized_center[1] + delta_y )
    potential_distances = calculate_distances(potential_center, border_points)
    potential_stdev = statistics.stdev(potential_distances)

    if potential_stdev < current_stdev:
        optimized_center = potential_center

    return optimized_center

def optimize_center(initial_center, border_points):
    optimized_center = initial_center

    print(optimized_center)

    current_distances = calculate_distances(optimized_center, border_points)
    current_stdev = statistics.stdev(current_distances)
    previous_stdev = current_stdev * 2

    print("Initial Standard Deviation ", current_stdev)

    while current_stdev != previous_stdev:
        print("Previous stdev was ", previous_stdev)
        print("Current stdev is ", current_stdev)

        previous_stdev = current_stdev

        optimized_center = search_left(optimized_center, border_points, current_stdev)
        optimized_center = search_right(optimized_center, border_points, current_stdev)
        optimized_center = search_up(optimized_center, border_points, current_stdev)
        optimized_center = search_down(optimized_center, border_points, current_stdev)

        current_distances = calculate_distances(optimized_center, border_points)
        current_stdev = statistics.stdev(current_distances)

    print("Final stdev is ", current_stdev)
    print("Roughness is ", current_stdev)

    mean = statistics.mean(current_distances)
    print("Mean is ", mean)

    return optimized_center

def draw_target(sample_name, image, position, color):
    image_copy = image.copy()
    for index in range(-25, 25):
        x = int(position[0])
        y = int(position[1])
        image_copy.putpixel(((x + index), y), color)
        image_copy.putpixel((x, (y + index)), color)

    #image_copy.show()
    image_copy.save(sample_name + '_optimized_center.png')

    return image_copy

def calculate_center(image, border_points):
    initial_center = calculate_initial_center(border_points)
    edited_image = draw_target(sample_name, image, initial_center, (255, 0, 0, 255))

    optimized_center = optimize_center(initial_center, border_points)
    draw_target(sample_name, edited_image, optimized_center, (0, 0, 255, 255))
    print("Optimized center is ", optimized_center)
    return optimized_center

def plot_distance_distribution(sample_name, distances):
    x_array = []

    index = 0
    for item in distances:
        x_array.append(index)
        index = index +1

    #plt.plot(x_array, distances, 'o')
    #plt.title('distances from origin to border')
    #plt.xlabel('detected border points')
    #plt.ylabel('distance in nm')
    #plt.legend(['particle'])

    #plt.xlim(0, len(distances) * 1.1)
    #plt.ylim(np.min(distances)*0.9, np.max(distances)*1.1)

    #plt.style.use('ggplot')
    plt.hist(distances, bins=50, edgecolor='black', linewidth=1.2)
    plt.xlabel('Radius [nm]', fontsize=16)
    plt.ylabel('Frequency [N]', fontsize=16)
    plt.grid(axis='y', alpha=0.5)
    plt.grid(axis='x', alpha=0.5)
    plt.tick_params(axis='x', labelsize=16)
    plt.tick_params(axis='y', labelsize=16)
    #plt.xlim(900, 1200)
    #plt.ylim(0, 450)
    plt.xlim(300, 1200)
    plt.ylim(0, 1500)

    #plt.show()

    N = len(distances)
    print("Number of detected border points is ", N)

    plt.savefig(sample_name + '_distance_distribution.png')
    return

def calculate_distances(center, border_points):
    return_value = np.empty(0)

    x1 = center[0]
    y1 = center[1]

    for border_point in border_points:
        x2 = border_point[0]
        y2 = border_point[1]
        distance = (m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)) * (3760/2048)
        #distance = (m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
        # print("%.2f" % distance)
        return_value = np.append(return_value, distance)

    #print(return_value)
    return return_value

def calculate_angles(center, border_points):
    return_value = np.empty(0)
    length = len(border_points)
    #first_vector = np.array(border_points[0]) - np.array(center)
    first_vector = np.array([1, 0])
    #print("Finding angles")

    for index in range(0, length):
        next_vector = np.array(border_points[index]) - np.array(center)
        angle = np.math.atan2(np.linalg.det([first_vector, next_vector]), np.dot(first_vector, next_vector))
        degrees = np.degrees(angle)

        if degrees < 0:
            degrees = 360 + degrees

        degrees = 360 - degrees

        #print(index, ": ", degrees)
        return_value = np.append(return_value, degrees)

    return return_value

def plot_angles_and_distances(sample_name, angles, distances):
    plt.plot(angles, distances, 'o', markersize=2)
    #plt.title('contour profile')
    plt.xlabel('Angle [degree]', fontsize=16)
    plt.ylabel('Distance [nm]', fontsize=16)
    #plt.legend(['particle'])
    plt.tick_params(axis='x', labelsize=16)
    plt.tick_params(axis='y', labelsize=16)
    plt.xlim(0, 360)
    plt.ylim(500, 1500)
    #plt.ylim(600, 1200)
    #plt.ylim(np.min(distances)*0.9, np.max(distances)*1.1)

    #plt.show()
    plt.savefig(sample_name + '_angles_and_distance.png')

    return

def save_data(sample_name, angles, distances):
    a = np.array(distances)
    b = np.array(angles)
    f = open(sample_name + "_angles_and_distances.csv", "w")

    for i in range(0, len(a)):
        f.write("{} {}\n".format(a[i], b[i]))

    f.close()

    return

def IsoData_threshold(source):
    #blurred_image = skimage.filters.gaussian(source, sigma=1.0)
    #plt.imshow(blurred_image, cmap='gray')
    #plt.show()

    thold = skimage.filters.threshold_isodata(source)
    #thold = skimage.filters.threshold_mean(blurred_image)
    #thold = skimage.filters.thresholding.apply_hysteresis_threshold(blurred_image, 0, 0.1)

    print("Threshold is ", thold)

    applied = source > thold
    colored = skimage.color.gray2rgb(applied)
    skimage.io.imsave(sample_name + "_IsoData_threshold.tif", colored)

    #plt.imshow(image, cmap='gray')
    #plt.show()

    return thold


sample_name = "2110553"
image_path = sample_name + ".tif"
source = skimage.io.imread(image_path)
threshold = IsoData_threshold(source)
image = read_image(sample_name + "_IsoData_threshold.tif")
border_points = find_border_points(image)
plot_border_points(sample_name, image, border_points)
center = calculate_center(image, border_points)
distances = calculate_distances(center, border_points)
plot_distance_distribution(sample_name, distances)
angles = calculate_angles(center, border_points)
plot_angles_and_distances(sample_name, angles, distances)
save_data(sample_name, angles, distances)
print("Threshold is ", threshold)














