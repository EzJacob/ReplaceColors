import sys
import os
from PIL import Image


# get all files with a specific extension
def select_files_with_specific_extension(file_path, extension):
    extension_files = []
    for root, dirs, files in os.walk(file_path):
        for file in files:
            if file.lower().endswith(extension):
                extension_files.append(os.path.join(root, file))
    return extension_files


# swap a pixel color with another pixel color
def swap_pixel_color_with_another_color(image, pixel_cord, other_pixel_color):
    other_color = list(other_pixel_color)
    other_color.append(255)
    other_pixel_color = tuple(other_pixel_color)
    image.putpixel(pixel_cord, other_pixel_color)


# check if the pixel color you want to swap is in the list of colors that consists of lists of a color to be swapped
# with another color
def get_color_in_colors_list(color, colors):
    for color_swap in colors:
        if color_swap[0] == color:
            return color_swap[1]
    return None


# return RGB of a pixel with no alpha value
def get_pixel_color_with_no_alpha(pixel_color):
    color = list(pixel_color)
    if len(color) > 3:
        color = color[:-1]
    color = tuple(color)
    return color


# swap the desired pixel color with another pixel color in an image
def swap_colors(image, colors):
    width, height = image.size
    for y in range(height):
        for x in range(width):
            pixel_color = image.getpixel((x, y))
            if pixel_color[3] == 0:
                continue
            pixel_color = get_pixel_color_with_no_alpha(pixel_color)
            other_pixel_color = get_color_in_colors_list(pixel_color, colors)
            if other_pixel_color is not None:
                swap_pixel_color_with_another_color(image, (x, y), other_pixel_color)


def from_file_get_three_variables(file_path):
    try:
        f = open(file_path, 'r')
        file_contents = f.read()
        variables = file_contents.split('\n', 2)
        f.close()
        return variables
    except Exception as e:
        print(f"Failed to open the file {file_path}: {e}")
        sys.exit(1)


if __name__ == '__main__':

    number_or_arguments = len(sys.argv)

    if number_or_arguments < 2:
        print("To use this script you need to write variables in a file")
        print("The format for example: ")
        argument_file_format = ("directory_path = [insert the directory path to the files with your "
                                "pictures. For example C:\\file_name1\\file_name2]\nextension = [insert a specific "
                                "file extension of an image (e.g.,"
                                "'.png',"
                                "'.jpeg', etc.). For example: '.png']\ncolors = [insert list of lists of tuples that "
                                "consists of ("
                                "color_to_replace, color_to_place_instead). For example: colors = [[(95, 205, 228), "
                                "(248, 199, 167)], [(106, 190, 48), (248, 199, 167)]]")
        print(argument_file_format)
        print("Make sure to make the format as python variables")
        sys.exit()

    arguments_list = sys.argv[1:]

    for arg in arguments_list:

        variables = from_file_get_three_variables(arg)

        # get the directory path to the files with your pictures
        # Use eval() to evaluate the content as Python code
        directory_path = variables[0].split("=")[1].strip()
        try:
            directory_path = eval(directory_path)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

        # Check if the directory path exists
        if os.path.exists(directory_path):
            pass
        else:
            print(f"The directory '{directory_path}' does not exist or is invalid.")
            sys.exit(1)

        # get the specific extension files you want to perform color swap on them
        # Use eval() to evaluate the content as Python code
        extension = variables[1].split("=")[1].strip()
        try:
            extension = eval(extension)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

        if extension.startswith('.'):
            pass
        else:
            print("Invalid input. Please start with a dot ('.') and provide a valid file extension.")
            sys.exit(1)

        extension_files = select_files_with_specific_extension(directory_path, extension)

        # test if those are the pictures you want to swap colors
        for file in extension_files:
            print(file)

        print("\nCheck if those are the pictures you want to swap colors")

        # Confirm if yes or no
        while True:
            user_input = input("Enter 'y' for yes or 'n' for no: ")
            if user_input == 'y' or user_input == 'Y':
                break
            elif user_input == 'n' or user_input == 'N':
                print(f"Operation canceled because of {arg}")
                sys.exit(1)
            else:
                print("Invalid input. Please enter 'y' for yes or 'n' for no.")

        # get list of lists of tuples that consists of (color_to_replace, color_to_place_instead)
        # Use eval() to evaluate the content as Python code
        colors = variables[2].split("=")[1].strip()
        try:
            colors = eval(colors)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

        # replace the colors in every image
        for file in extension_files:
            try:
                image = Image.open(file)
                swap_colors(image, colors)
                image.save(file)
                image.close()
            except Exception as e:
                print(f"Failed to open the file {file}: {e}")

        print(f"Script is finished with {arg}")

    print("Script of replacing pixel colors is finished. Exiting script...")

