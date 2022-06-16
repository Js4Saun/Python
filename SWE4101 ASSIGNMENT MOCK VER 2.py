######################################           JOSEPH SAUNDERSON 0707476 SWE4101 INTRODUCTION TO SOFTWARE DEVELOPMENT BAI CALCULATOR        ###################################################################################################################

import statistics

#########################  Lists/arrays for main variables
Age=[]
Height=[]
Hip_Circumference=[]
BAI=[]

########################## Lists/arrays for percentages
underweight=[]
healthy=[]
overweight=[]
obese=[]

underweight1=0
healthy2=0
overweight3=0
obese4=0

############################   Program purpose and welcome

#------------------------------------------------------------------------------------------------
def Main_menu():
    print("Welcome to the BAI (Body Apository Index) calculator")
    print()
    print("Note: this program will only calculate your BAI if you are 20 years old or over")
    print()
    print("This program will calculate your BAI based on your height and hip-waist ratio")
    ###############    goes to continue_Choice function   
    continue_Choice()

#--------------------------------------------------------------------------------------------------
            
############################    Giving the user the choice to continue or quit            
def continue_Choice():
    ################    continues based on Y or N input from the user
    print("Do you wish to continue or exit?, please choose Y/N:")
    ################    Converts user input to uppercase    
    choice = input().upper()
    
    
    if choice != "Y" and choice != "N":
        ############################    validation for continue choice       
        print("There was an error with your choice, Please retry")
        choice = input().upper()
    ##############     goes to choice_Gender function if Y is the input
    elif choice == "Y":
        choice_Gender()
    #########     kills program if N is the input
    elif choice == "N":
        statistics2()
        percentages(underweight, underweight1, healthy, healthy2, overweight, overweight3, obese, obese4)
        SystemExit()
         
#--------------------------------------------------------------------------------------------------    
     
    ############################    Fuction choice_Gender, press 1 for Female or 2 for Male   

def choice_Gender():
    print("Please enter your Gender, choose 1 for Female or 2 for Male:")
    Gender = input()
    ######################     User choice validation
    while Gender != "1" and Gender != "2":
        print("There was an error with your choice, Please retry")
        Gender = input()
    ######################  If the user chooses option 1, goes to Female function    
    if Gender == "1":
            BAI = Female()
            
    ######################  If the user chooses option 2, goes to Male function      
    else:
            BAI = Male()
               
    return Gender
    
#---------------------------------------------------------------------------------------------------

############################    Function for female choice
def Female():
   
    #####################   Asking for users age in years
    print("Please enter your age in years")
    user_Age = int(input())

    Age.append(user_Age)
    
    #####################   Giving the user the option to use imperial or metric figures for height
    print("Which unit type would you like to choose to measure Height?:")
    print("Press 1 to enter Height in feet (ft)")
    print("Press 2 to enter Height in meters (m)")
    
    unit = input()
    
    while unit != "1" and unit != "2":
        ###################  Validation for user choice        
        print("There is an error with your choice, Please retry")
    
        unit = input()
    ######################   Feet choice for height         
    if unit == "1":
        print("Enter your height in feet")
        
        user_Height = float(input())
        user_Height = feet_to_meter(user_Height)
    #####################    Meter choice for height            
    else:
        print("Enter your height in meters")
        user_Height = float(input())
        user_Height = user_Height
      
    Height.append(user_Height)
    
    ####################    Giving the uer the option to use imperial or metric figures for hip circumference
    print("Which unit would you like to choose to measure Hip Circumference?:")
    print("Press 1 to enter Hip Circumference in Inches (in)")
    print("Press 2 to enter Hip Circumference in centimeters (cm)")
    
    
    hip_measurment = input()
    
    while unit != "1" and unit != "2":
        ############### Validation for hip        
        print("There is an error with your choice, Please retry")
       
        hip_measurment = input()
    ##################   Inches choice for hp
    if hip_measurment == "1":
        print("Enter hip circumference in inches")
        
        user_hc= float(input())
        user_hc = inches_to_cm(user_hc)
    #################    cm choice for hip
    else:
        print("Enter hip circumference in cm")
        user_hc= float(input())
        user_hc = user_hc
                
    Hip_Circumference.append(user_hc)    

    #####################    BAI calculation        
    BodyAIndex = (user_hc/(user_Height**1.5))-18
    
    #######################     Output BAI        
    print("Your BAI is", round(BodyAIndex,2))
            
    #######################     if statements for health status 
    if (BodyAIndex <= 21) and (user_Age >= 20) and (user_Age <= 39):
            print("You are currently Underweight")
            underweight1=+1
            underweight.append(underweight1)
        
    
    elif (BodyAIndex >= 21) and (BodyAIndex <=33) and (user_Age >= 20) and (user_Age <= 39):
            print("You are currently Healthy")
            healthy2=+1
            healthy.append(healthy2)
        

    elif (BodyAIndex >= 34) and (BodyAIndex <=39) and (user_Age >= 20) and (user_Age <= 39):
            print("You are currently Overweight")
            overweight3=+1
            overweight.append(overweight3)
        
      
    elif (BodyAIndex >= 39)  and (user_Age >= 20) and (user_Age <= 39):
            print("You are currently Obese")
            obese4=+1
            obese.append(obese4)
        

    elif (BodyAIndex <= 23)  and (user_Age >= 40) and (user_Age <= 59):
            print("You are currently Underweight")
            underweight1=+1
            underweight.append(underweight1)
        

    elif(BodyAIndex >= 23) and (BodyAIndex <= 35)  and (user_Age >= 40) and (user_Age <= 59):
            print("You are currently Healthy")
            healthy2=+1
            healthy.append(healthy2)
        

    elif(BodyAIndex >= 35) and (BodyAIndex <= 41)  and (user_Age >= 40) and (user_Age <= 59):
            print("You are currently Overweight")
            overweight3=+1
            overweight.append(overweight3)
        

    elif (BodyAIndex >= 43) and (user_Age >= 40) and (user_Age <= 59):
            print("You are currently Obese")
            obese4=+1
            obese.append(obese4)
    

    elif (BodyAIndex <= 25) and (user_Age >= 60) and (user_Age <= 79):
            print("You are currently Underweight")
            underweight1=+1
            underweight.append(underweight1)
        

    elif (BodyAIndex >= 25) and (BodyAIndex <= 38) and (user_Age >= 60) and (user_Age <= 79):
            print("You are currently Healthy")
            healthy2=+1
            healthy.append(healthy2)
        

    elif (BodyAIndex >= 38) and (BodyAIndex <= 43) and (user_Age >= 60) and (user_Age <= 79):
            print("You are currently Overweight")
            overweight3=+1
            overweight.append(overweight3)
                
    elif (BodyAIndex >= 43) and (user_Age >= 60) and (user_Age <= 79):
            print("You are currently obese")
            obese4=+1
            obese.append(obese4)

    BAI.append(round(BodyAIndex,2))

    return continue_Choice()
    
#---------------------------------------------------------------------------------------------
#######################     Function for Male choice
def Male():
    ###################     Age inpuy
    print("Please enter your age in years")
    user_Age = int(input())
    ###################     Appends user age to 
    Age.append(user_Age)
    ###################     Height inputs unit choices
    print("Which unit type would you like to choose to measure Height?:")
    print("Press 1 to enter Height in feet (ft)")
    print("Press 2 to enter Height in meters (m)")
    
    height_mes = input()
    ###################     While loop and error checking for the correct choice
    while height_mes != "1" and height_mes != "2":
                
        print("There is an error with your choice, Please retry")
    
        height_mes = input()
            
    if height_mes == "1":
        print("Enter your height in feet")
        
        user_Height = float(input())
        user_Height = feet_to_meter(user_Height)
                
    else:
        print("Enter your height in meters")
        user_Height = float(input())
        user_Height = user_Height
    
    Height.append(user_Height)    
    ####################     Hip Circumference inputs for choice
    print("Which unit would you like to choose to measure Hip Circumference?:")
    print("Press 1 to enter Hip Circumference in Inches (in)")
    print("Press 2 to enter Hip Circumference in centimeters (cm)")
    
    
    hip_measurment = input()
    ###################      While loop and error checking for the correct choice
    while hip_measurment != "1" and hip_measurment != "2":
                
        print("There is an error with your choice, Please retry")
       
        hip_measurment = input()
    ###################      Conversion to inches
    if hip_measurment == "1":
        print("Enter hip circumference in inch")
        
        user_hc= float(input())
        user_hc = inches_to_cm(user_hc)
    ###################      Conversion to cm    
    else:
        print("Enter hip circumference in cm")
        user_hc= float(input())
        user_hc = user_hc
                
    Hip_Circumference.append(user_hc)    
    ###################       Calculation for BAI    
    BodyAIndex = (user_hc/(user_Height**1.5))-18
      
    print("Your BAI is", round(BodyAIndex,2))
            
    ###################       If statements for displaying the health of the user based on their BAI and age         
    if (BodyAIndex <= 8) and (user_Age >= 20) and (user_Age <= 39):
            print("You are currently Underweight")
            underweight1=+1
            underweight.append(underweight1)
        
      
    elif (BodyAIndex >= 8) and (BodyAIndex <= 21) and (user_Age >= 20) and (user_Age <= 39):
            print("You are currently Healthy")
            healthy2=+1
            healthy.append(healthy2)
        

    elif (BodyAIndex >= 21) and (BodyAIndex <= 26) and (user_Age >= 20) and (user_Age <= 39):
            print("You are currently Overweight")
            overweight3=+1
            overweight.append(overweight3)
        
          
    elif (BodyAIndex >= 26) and (user_Age >= 20) and (user_Age <= 39):
            print("You are currently Obese")
            obese4=+1
            obese.append(obese4)
        

    elif (BodyAIndex <= 11) and (user_Age >= 40) and (user_Age <= 59):
            print("You are currently Underweight")
            underweight1=+1
            underweight.append(underweight1)
        
        
    elif (BodyAIndex >= 11) and (BodyAIndex <= 23) and (user_Age >= 40) and (user_Age <= 59):
            print("You are currently Healthy")
            healthy2=+1
            healthy.append(healthy2)
        
          
    elif (BodyAIndex >= 23) and (BodyAIndex <= 29) and (user_Age >= 40) and (user_Age <= 59):
            print("You are currently Overweight")
            overweight3=+1
            overweight.append(overweight3)
        
          
    elif (BodyAIndex >= 29) and (user_Age >= 40) and (user_Age <= 59):
            print("You are currently Obese")
            obese4=+1
            obese.append(obese4)
        

    elif(BodyAIndex <= 13) and (user_Age >= 60) and (user_Age <= 79):
            print("You are currently Underweight")
            underweight1=+1
            underweight.append(underweight1)
        

    elif (BodyAIndex >= 13) and (BodyAIndex <= 25) and (user_Age >= 60) and (user_Age <= 79):
            print("You are currently Healthy")
            healthy2=+1
            healthy.append(healthy2)
        
          
    elif (BodyAIndex >= 25) and (BodyAIndex <= 31) and (user_Age >= 60) and (user_Age <= 79):
            print("You are currently Overweight")
            overweight3=+1
            overweight.append(overweight3)
        

    elif (BodyAIndex >= 31) and (user_Age >= 60) and (user_Age <= 79):
            print("You are currently Obese")
            obese4=+1
            obese.append(obese4)
      
    BAI.append(round(BodyAIndex,2))

    return continue_Choice()
#----------------------------------------------------------------------------
def statistics2():

    ##########################   statistics AGE        
    n= len(Age)
    age_mean = sum(Age)/n
    
    range_max = max(Age)
    range_min = min(Age)
    range_mode = range_max - range_min

    #########################    statisitcs HEIGHT
    n= len(Height)
    height_mean = sum(Height)/n
    
    range_height_max = max(Height)
    range_height_min = min(Height)
    height_range = range_height_max - range_height_min

    #########################    statistics HIP CIR

    n= len(Hip_Circumference)
    hip_mean = sum(Hip_Circumference)/n
    
    hip_max = max(Hip_Circumference)
    hip_min = min(Hip_Circumference)
    hip_range = hip_max - hip_min
    
    ########################     statistics BAI
    n= len(BAI)
    B_mean = sum(BAI)/n
    
    range_baimax = max(BAI)
    range_baimin = min(BAI)
    bai_range = range_baimax - range_baimin

    ########################    Outputs the statisitcs for AGE
    print("The age's you entered are",(Age))
    print("The highest age you entered was",max(Age))
    print("The lowest age you entered was", min(Age))
    print("The mean of your ages is", (age_mean))
    print("The range of your ages is", (range_mode))
    print_MAge = ModeA() 
    print("The mode of your ages is", (print_MAge ))
    print()
    ########################    Ouputs the statistics for HEIGHT
    print("The Height's you entered are",(Height))
    print("The highest Height you entered was", max(Height))
    print("The lowest Height you entered was", min(Height))
    print("The mean of your entered Heights is", (height_mean))
    print("The range of your entered Heights is", (height_range))
    print_Mhi = ModeHi()
    print("The mode of your Heights is", (print_Mhi))
    print()
    #######################     Outputs the statisitcs for HIP CIRCUMFERENCE
    print("The Hip Circumference's you entered are",(Hip_Circumference))
    print("The highest age you entered was",max(Hip_Circumference))
    print("The lowest Height you entered was", min(Hip_Circumference))
    print("The mean of your Hip Circumferences is", (hip_mean))
    print("The range of your Hip Circumferences is", (hip_range))
    print_Mhc = ModeHip()
    print("The mode of your Hip Circumferences is", (print_Mhc))
    print()
    ######################     Outputs the statisitcs for BAI
    print("The BAI results are",(BAI))
    print("The highest BAI result is",max(BAI))
    print("The lowest BAI result is", min(BAI))
    print("The mean the BAI results is", (B_mean))
    print("The range of the BAI results is", (bai_range))
    print_BaI = ModeBAI() 
    print("The mode of your ages is", (print_BaI ))

#----------------------------------------------------------------------------------------------
    ######################     percentages function
def percentages(underweight, underweight1, healthy, healthy2, overweight, overweight3, obese, obese4):
    
    per = sum(underweight) + sum(healthy) + sum(overweight) + sum(obese)
    print("Percent of underweight",sum(underweight)/per * 100)
    print("Percent of healthy",sum(healthy)/per * 100)
    print("Percent of overweight",sum(overweight)/per * 100)
    print("Percent of obese",sum(obese)/per * 100)

#------------------------------------------------------------------------

######################    Function conversion inches to cm
def inches_to_cm(user_hc):
    unit = user_hc * 2.54
    return unit

######################    Function conversion feet to meters
def feet_to_meter(user_Height):
    unit = user_Height / 3.28
    return unit
######################    Function for age mode
def ModeA():
    try:
        mode_age = statistics.mode(Age)
        return mode_age
    except:
        return "Not available"
######################    Function for Height mode
def ModeHi():
    try:
        mode_height = statistics.mode(Height)
        return mode_height
    except:
        return "Not available"
######################    Function for Hip Cicrumference mode
def ModeHip():
    try:
        mode_hip = statistics.mode(Hip_Circumference)
        return mode_hip
    except:
        return "Not available"
######################    Function for BAI mode
def ModeBAI():
    try:
        mode_Body = statistics.mode(BAI)
        return mode_Body
    except:
        return "Not available"
 
Main_menu()
     


   


    
                    

