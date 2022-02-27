from array import array
import re
import data_extract as de
import control as ct
from PIL import Image
import numpy as np
import os

class home_locs():
    dx = ct.gap_between_flags
    dy = ct.gap_between_flags

    new_x = 64
    new_y = 64

    def __init__(self) -> None:
        self.vals, self.cats, self.start_coord, self.end_coord = de.DataExtract().extract_data()
        self.main_folder = os.getcwd()
        self.n = self.new_y
        self.m = self.new_x

        if ct.portrait_view:
            self.rows = ct.life_expectancy
            self.cols = ct.standard_weeks_year

        else:
            self.rows = ct.standard_weeks_year
            self.cols = ct.life_expectancy

    def extract_homes(self):
        data_hold = []
        for n, ln in enumerate(self.vals):
            if ln[2] == ct.country_loc:
                #Data is held as [Country, flag div, start_loc, end_loc]
                line = [ln[5], ln[6], self.start_coord[n], self.end_coord[n]]
        
                data_hold.append(line)
        return data_hold

    def get_flag(self, country):
        path = self.main_folder + '/' + ct.flag_folder + '/' + country + '.' + ct.flag_type
        img = Image.open(path)
        img.thumbnail((self.new_y, self.new_x), Image.ANTIALIAS)

        #Set the transparency
        img_arr = np.array(img)
        img_arr[img_arr[...,-1]==0] = [255,255,255,0]
    
        return Image.fromarray(img_arr)
    
    # def flag_dims(self, flag):
    #     self.n, self.m = np.array(flag).shape[:2]

    def make_base(self):

        # TODO: make the dimentions of the base image customisable
        # TODO: make the background colour customisable

        if ct.portrait_view:
            width = ct.standard_weeks_year
            length = ct.life_expectancy
        else:
            width = ct.life_expectancy
            length = ct.standard_weeks_year

        b_n = ((self.n + ct.gap_between_flags)* length) + ct.gap_between_flags * 2
        b_m = ((self.m + ct.gap_between_flags) * width) + ct.gap_between_flags * 2
        image = Image.new('RGB', (b_m, b_n), (255, 255, 255))
        return image

    def paste_im(self, base_im, new_im, loc):
        #Loc is a tuple
        base_im.paste(new_im, loc)
        return base_im

    def prod_image(self, flag_data):
        #Takes the flag data for each week and produces the full image
        #Flag data is an array of flag names for each location on the chart

        # Make base image
        base = self.make_base()

        row_offset = ct.gap_between_flags
        col_offset = ct.gap_between_flags

        for i in range(self.rows):
            print(i)
            for j in range(self.cols):
                flag_name = flag_data[i, j]
                if flag_name != '':
                    img_flag = self.get_flag(flag_name)
                    print(row_offset, col_offset)
                    base = self.paste_im(base, img_flag, (col_offset, row_offset))

                if ct.portrait_view:
                    col_offset += (self.new_x + ct.gap_between_flags)
                else:
                    row_offset += (self.new_y + ct.gap_between_flags)

            if ct.portrait_view:
                row_offset += (self.new_x + ct.gap_between_flags)
                col_offset = ct.gap_between_flags
            else:
                col_offset += (self.new_y + ct.gap_between_flags)
                row_offset = ct.gap_between_flags

        base.show()

        return 0
                
        



    


if __name__ == "__main__":
    hl = home_locs()
    x = hl.extract_homes()
    

    test = [['ireland' for j in range(53)] for i in range(101)]
    test = np.array(test)

    hl.prod_image(test)