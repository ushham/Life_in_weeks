#Database
db_loc = 'life_database_test.csv'

col_dic = {
    'date_from' : 0,
    'date_to' : 1,
    'cat' : 2,
    'sub_cat' : 3,
    'colour' : 4
}

life_expectancy = 100   #<- Last year that is shown in the chart.
standard_weeks_year = 52
weeks_per_year = 52.17857143  #365.25 / 7
days_per_week = 7
dob = '19/01/1992'      #<- Date of birth to be edited.

event = 'Life Event'    #<- The title in the database given to life events

#plotting constants
radius = 150            #Size of circles on scatter graph

portrait_view = False   #When true, the years of life are on the y axis.