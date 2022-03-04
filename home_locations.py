import sys
import data_extract as de
import control as ct
from PIL import Image
import numpy as np
import os

class liw_flag_chart():
    dx = ct.gap_between_flags_x
    dy = ct.gap_between_flags_y

    resized_flag_x = 64
    resized_flag_y = 64

    def __init__(self) -> None:
        self.vals, self.cats, self.start_coord, self.end_coord = de.DataExtract().extract_data()
        self.main_folder = os.getcwd()
        self.n = self.resized_flag_y
        self.m = self.resized_flag_x

        if ct.portrait_view:
            self.rows = ct.life_expectancy
            self.cols = ct.standard_weeks_year

        else:
            self.rows = ct.standard_weeks_year
            self.cols = ct.life_expectancy

    def extract_home_locations(self):
        data_hold = []
        country_hold = []
        for n, ln in enumerate(self.vals):
            if ln[2] == ct.country_loc:
                #Data is held as [Country, flag div, start_loc, end_loc]
                line = [ln[5], ln[6], self.start_coord[n], self.end_coord[n]]
                country_hold.append(ln[5])
                data_hold.append(line)
        return data_hold, country_hold

    def check_flag_exists(self):
        for c in self.countries:
            path = self.main_folder + '/' + ct.flag_folder + '/' + c + '.' + ct.flag_type
            if not(os.path.isfile(path)):
                print(c + " is not in your flag folder")
                sys.exit()
        
        return 0

    @staticmethod
    def paste_image(base_im, new_im, loc: tuple):
        #Loc is a tuple
        base_im.paste(new_im, loc)
        return base_im

    def import_flag(self, country: str):
        path = self.main_folder + '/' + ct.flag_folder + '/' + country + '.' + ct.flag_type
        
        if not(os.path.isfile(path)):
            # This error occurs when the np.chararray produces nonsence strings
            print("Unexpected error where the code is looking for flag named: " + country)
            sys.exit()

            
        img = Image.open(path)
        img.thumbnail((self.new_y, self.new_x), Image.ANTIALIAS)

        #Set the transparency
        img_arr = np.array(img)
        img_arr[img_arr[...,-1]==0] = [255,255,255,0]
            
    
        return Image.fromarray(img_arr)

    def make_base_image(self):

        # TODO: make the dimentions of the base image customisable
        # TODO: make the background colour customisable

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


    def data_to_array(self):
        # takes the data and produces a numpy array that has all of the flag data layed out
        
        max_str_len = len(max(self.countries, key=len))
        
        data_hold = np.chararray((self.rows * self.cols), itemsize=max_str_len)
        data_hold[:] = ''
    
        for ln in self.reduced_data:
            start = ln[2]
            end = ln[3] + 1
            country = ln[0]
            data_hold[start:end] = country
            
        data_hold = data_hold.reshape((self.rows, self.cols))
        return data_hold

    def make_image(self, flag_data):
        #Takes the flag data for each week and produces the full image
        #Flag data is an array of flag names for each location on the chart

        # Make base image
        base = self.make_base_image()

        row_offset = ct.gap_between_flags_y if ct.portrait_view else ct.gap_between_flags_x
        col_offset = ct.gap_between_flags_x if ct.portrait_view else ct.gap_between_flags_y

        for i in range(self.rows):
            print(i)
            for j in range(self.cols):
                try:
                    flag_name = flag_data[i, j].decode()
                except:
                    flag_name = flag_data[i, j]

                if flag_name != '':
                    img_flag = self.get_flag(flag_name)
                    base = self.paste_im(base, img_flag, (col_offset, row_offset))

                if ct.portrait_view:
                    col_offset += (self.new_x + ct.gap_between_flags_x)
                else:
                    row_offset += (self.new_y + ct.gap_between_flags_y)

            if ct.portrait_view:
                row_offset += (self.new_x + ct.gap_between_flags_y)
                col_offset = ct.gap_between_flags
            else:
                col_offset += (self.new_y + ct.gap_between_flags_x)
                row_offset = ct.gap_between_flags

        base.show()

        return 0

    
    def run_flag_script(self):
        #Function which runs the required functions

        self.reduced_data, self.countries = self.extract_home_locations()
        self.check_flag_exists()

        flag_data = self.data_to_array()
        # np.savetxt('test.csv', flag_data, fmt='%s', delimiter=',')
        self.make_image(flag_data)

        return 0

                
        



    


if __name__ == "__main__":
    hl = liw_flag_chart()
    # x = hl.extract_homes()

    # flag_data = hl.data_to_array()
    # hl.prod_image(flag_data)
    # print(flag_data[20, 1])
    hl.run_flag_script()