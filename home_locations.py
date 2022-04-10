import sys
import data_extract as de
import control as ct
from PIL import Image
import numpy as np
import os

class Liw_Flag_Chart():
    """A class that creates an image showing a flag for the location every week of your life

    Attributes:
    -----------
    resized_flag_x : int
        The horizontal number of pixels of the resized flag used in the image
    resized_flag_y : int
        The horizontal number of pixels of the resized flag used in the image

    Methods:
    --------
    extract_home_locations(): 
    """

    resized_flag_x = 64
    resized_flag_y = 64

    def __init__(self) -> None:
        self.vals, self.cats, self.start_coord, self.end_coord = de.DataExtract().extract_data(whole_num=False)
        self.main_folder = os.getcwd()
        self.n = self.resized_flag_y
        self.m = self.resized_flag_x

        self.reduced_data = sorted(self.extract_locations(), key=lambda x: x[2])
        self.countries = [ln[0] for ln in self.reduced_data]

        if ct.portrait_view:
            self.rows = ct.life_expectancy
            self.cols = ct.standard_weeks_year

        else:
            self.rows = ct.standard_weeks_year
            self.cols = ct.life_expectancy

    def extract_locations(self):
        """
            Takes the raw data from csv database and extracts the key country data

        Returns:
            List consisting of Country, How the flag is to be divided, start week, end week
        """
        data_hold = []
        for n, ln in enumerate(self.vals):
            if ln[2] == ct.country_loc:
                #Data is held as [Country, flag div, start_loc, end_loc]
                line = [ln[5], ln[6], self.start_coord[n], self.end_coord[n]]

                data_hold.append(line)

        return data_hold

    def check_flag_exists(self):
        """
            Ensures the flag that is provided is in the given sub-folder
        Returns:
            0, script will exit with error if flag does not exist.
        """

        for c in self.countries:
            path = self.main_folder + '/' + ct.flag_folder + '/' + c + '.' + ct.flag_type
            if not(os.path.isfile(path)):
                print(c + " is not in your flag folder")
                sys.exit()

        return 0

    def import_flag(self, country: str):
        """
            Imports flag image as Pillow file. The transparent background is converted to white.

        Parameters:
            country: str
                Name of the country or flag to import

        Returns:
            img_arr: Image
                Pillow image of the specified flag

        """

        path = self.main_folder + '/' + ct.flag_folder + '/' + country + '.' + ct.flag_type

        if not(os.path.isfile(path)):
            # This error occurs when the np.chararray produces nonsence strings
            print("Unexpected error where the code is looking for flag named: " + country)
            sys.exit()


        img = Image.open(path)
        img.thumbnail((self.resized_flag_y, self.resized_flag_x), Image.ANTIALIAS)

        #Set the transparent section to white
        img_arr = np.array(img)
        img_arr[img_arr[..., -1] == 0] = [255, 255, 255, 0]

        return Image.fromarray(img_arr)

    def stack_flags(self, base, new_flag, start_share, end_share, division_type):
        """
            Creates a combined flag for weeks when there are multiple flags

            Parameters:
                base: Image
                    The first or base flag

                new_flag: Image
                    The flag to paste onto the base flag

                start_share: Float
                    Starting location for pasting the new_flag, as a % of the original image
                
                end_share: Float
                    End location for pasting the new_flag as % of the original image

                division_type: Str
                    How the pasting division is set

            Returns:
                base: Image
                    The comnbined image

        """
        # Lower Diagonal mask
        if division_type == "Diagonal":
            mask_array = [[(i + j) / (2) for j in range(self.resized_flag_x)] for i in range(self.resized_flag_y)]

        # Horizontal mask
        elif division_type == "Horizontal":
            mask_array = [[i for j in range(self.resized_flag_x)] for i in range(self.resized_flag_y)]

        # Vertical mask
        elif division_type == "Vertical":
            mask_array = [[j for j in range(self.resized_flag_x)] for i in range(self.resized_flag_y)]
        
        else:
            print("The program doesnt recognise the flag division definition " + division_type)
            sys.exit()
    
        mask_array = np.array(mask_array) / np.max(mask_array)
        mask_array = (mask_array > start_share) * (mask_array <= end_share)
        
        mask_for_flag = Image.fromarray(np.uint8(255 * mask_array))
        base.paste(new_flag, (0, 0), mask_for_flag)
        return base
        
    def produce_flag(self, data, week_num):
        """
            Takes the list of flags for a given week to produce a composite flag

            Parameters:
                data: list
                    list of Country, Division type, start week, end week data
                
                week_num: int
                    The week number the program is focusing on

            Returns:
                base_flag: Image
                    Composite flag
        """

        base_flag = self.import_flag(data[0][0])

        if len(data) > 1:

            # Logic for working out the division of flags
            # Everything is Diagonal, unless the types match
            division_type = [x[1] for x in data]
            same_div_type = (len(set(division_type)) == 1)

            division_type = division_type[0] if same_div_type else "Diagonal"

            for i in range(1, len(data)):
                start_share = data[i][2] - int(data[i][2]) if int(data[i][2]) == week_num else data[i][3] - int(data[i][3])
                end_share = 1 if int(data[i][3]) >= week_num else data[i][3] - int(data[i][3])

                new_flag = self.import_flag(data[i][0])
                base_flag = self.stack_flags(base_flag, new_flag, start_share, end_share, division_type)
            
        return base_flag

    def make_base_image(self):
        """
            Produces the background image used in the program

            Returns:
                image: Image
                    Background image
        """
        if ct.portrait_view:
            width = ct.standard_weeks_year
            length = ct.life_expectancy
        else:
            width = ct.life_expectancy
            length = ct.standard_weeks_year

        base_image_size_y = ((self.n + ct.gap_between_flags_y)* length) + ct.gap_between_flags_y * 2
        base_image_size_x = ((self.m + ct.gap_between_flags_x) * width) + ct.gap_between_flags_x * 2
        image = Image.new('RGB', (base_image_size_x, base_image_size_y), (255, 255, 255))
        return image

    def produce_image(self):
        """
            Produce the final image

            Returns:
                base: Image
                    Final image
        """

        # Make base image
        base = self.make_base_image()

        row_offset = ct.gap_between_flags_y if ct.portrait_view else ct.gap_between_flags_x
        col_offset = ct.gap_between_flags_x if ct.portrait_view else ct.gap_between_flags_y

        for i in range(self.rows):
            print("Making year " + str(i))
            
            for j in range(self.cols):
                week_number = i * self.cols + j

                #Filter the list of places to include only flags with given week number
                filtered_flag = [x for x in self.reduced_data if int(x[2]) - week_number == 0 or (int(x[3]) - week_number == 0 and x[3] > week_number) or (x[2] <= week_number and x[3] > week_number)] 

                if len(filtered_flag) > 0:
                    prod_flag = self.produce_flag(filtered_flag, week_number)
                    base.paste(prod_flag, (col_offset, row_offset))

                if ct.portrait_view:
                    col_offset += (self.resized_flag_x + ct.gap_between_flags_x)
                else:
                    row_offset += (self.resized_flag_y + ct.gap_between_flags_y)

            if ct.portrait_view:
                row_offset += (self.resized_flag_x + ct.gap_between_flags_y)
                col_offset = ct.gap_between_flags_x
            else:
                col_offset += (self.resized_flag_y + ct.gap_between_flags_x)
                row_offset = ct.gap_between_flags_y

        base.show()

        return 0

    def run_flag_script(self):
        #Function which runs the required functions

        self.check_flag_exists()
        # np.savetxt('test.csv', flag_data, fmt='%s', delimiter=',')
        self.produce_image()

        return 0

if __name__ == "__main__":
    hl = Liw_Flag_Chart()
    hl.produce_image()

