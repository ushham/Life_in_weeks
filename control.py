#Database
db_loc = 'life_database_test.csv'

col_dic = {
    'date_from' : 0,
    'date_to' : 1,
    'cat' : 2,
    'sub_cat' : 3,
    'colour' : 4
}

life_expectancy = 90   #<- Last year that is shown in the chart.
standard_weeks_year = 52
weeks_per_year = 52.17857143  #365.25 / 7
days_per_week = 7
dob = '19/01/1992'      #<- Date of birth to be edited.

event = 'Life Event'    #<- The title in the database given to life events
country_loc = 'Loc'       #<- the title in the database given to location for the given dates

#plotting constants
radius = 150             #Size of circles on scatter graph
gap_between_flags_x = 5
gap_between_flags_y = 5 

portrait_view = True   #When true, the years of life are on the y axis.

#Flag Folder
flag_folder = 'flags'
flag_type = 'png'
base_image = 'basepic.png'

saved_outputs = 'Outputs'