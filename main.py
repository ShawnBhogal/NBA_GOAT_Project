#!/usr/bin/env python
# coding: utf-8

# import relevant libraries/frameworks
from decimal import *
import psycopg2 as pg2

# dictionary for storing values from 1-10 that user inputs for each category weight
weight_dict = {
}

# this is where the user will choose which stats they want to evaluate 
# user will also be prompted to input a number from 1 to 10 as weight for the importance of each stat
cat_dict = {
     1 : "games_played", 
     2 : "mp",
     3 : "fg" ,
     4 : "fga", 
     5 : "two_p", 
     6 : "two_pa",
     7 : "three_p", 
     8 : "three_pa",
     9 : "ft", 
    10 : "fta",
    11 : "orb", 
    12 : "drb", 
    13 : "trb", 
    14 : "ast", 
    15 : "stl",
    16 : "blk", 
    17 : "pts", 
    18 : "fg_pct", 
    19 : "two_p_pct", 
    20 : "three_p_pct", 
    21 : "efg_pct", 
    22 : "ft_pct", 
    23 : "trueshooting_pct", 
    24 : "three_par",
    25 : "ftr", 
    26 : "orb_pct", 
    27 : "drb_pct",  
    28 : "ast_pct", 
    29 : "stl_pct", 
    30 : "blk_pct", 
    31 : "ortg", 
    32 : "drtg", 
    33 : "ows", 
    34 : "dws", 
    35 : "ws", 
    36 : "obpm", 
    37 : "dbpm",  
    38 : "bpm", 
    39 : "vorp" 
}

def intro():
    print ("Welcome!\n")
    print ("This your very own NBA Greatest of All Time (G.O.A.T) Calculator!")
    print ("Here you will be able to customize and create your customized statistical G.O.A.T")
    print ("\nInstructions:")
    print ("1) Input a number from 1 to 39 in order to choose statistical category.")
    print ("2) Input a weight from 1 to 10 indicating indicating importance for G.O.A.T calculation")
    print ("3) When finished enter 40 to calculate!") 
    print ("\nUNLESS SPECIFIED, ASSUME ALL CATEGORIES ARE PER GAME\n")
    print ("REGULAR STATS:")
    print (" 1. Total Career Games Played")  
    print (" 2. Total Career Minutes Played")
    print (" 3. Field Goals Made ")
    print (" 4. Field Goals Attempted")
    print (" 5. 2-Pointers Made")
    print (" 6. 2-Pointers Attempted")
    print (" 7. 3-Pointers Made")
    print (" 8. 3-Pointers Attempted")
    print (" 9. Free Throws Made")
    print ("10. Free Throws Attempted")
    print ("11. Offensive Rebounds")
    print ("12. Defensive Rebounds")
    print ("13. Total Rebounds")
    print ("14. Assists")
    print ("15. Steals")
    print ("16. Blocks")
    print ("17. Points")
    print ("18. Field Goal Percentage")
    print ("19. 2-Point Percentage")
    print ("20. 3-Point Percentage")
    print ("\nADVANCED STATS:")
    print ("21. " + "\033[1m" + "Effective Field Goal Percentage" + "\033[0m")
    print ("    - This statistic adjusts for the fact that a 3-point field goal is worth one more point than a 2-point field goal.")
    print ("22. " + "\033[1m" + "Free Throw Percentage" + "\033[0m")
    print ("23. " + "\033[1m" + "Trueshooting Percentage" + "\033[0m")
    print ("    - A measure of shooting efficiency that takes into account 2-point field goals, 3-point field goals, and free throws.")
    print ("24. " + "\033[1m" + " 3-Point Attempt Rate" + "\033[0m")
    print ("    - Percentage of FG Attempts from 3-Point Range")
    print ("25. " + "\033[1m" +  "Free Throw Attempt Rate" + "\033[0m")
    print ("    - Number of FT Attempts Per FG Attempt")
    print ("26. " + "\033[1m" +  "Offensive Rebound Percentage" + "\033[0m")
    print ("    - An estimate of the percentage of available offensive rebounds a player grabbed while on the floor.")
    print ("27. " + "\033[1m" +  "Defensive Rebound Percentage" + "\033[0m")
    print ("    - An estimate of the percentage of available defensive rebounds a player grabbed while on the floor.")
    print ("28. " + "\033[1m" +  "Assist Percentage" + "\033[0m")
    print ("    - An estimate of the percentage of teammate field goals a player assisted while on the floor.")
    print ("29. " + "\033[1m" +  "Steal Percentage" + "\033[0m")
    print ("    - An estimate of the percentage of opponent possessions that end with a steal while on the floor.")
    print ("30. " + "\033[1m" + "Block Percentage" + "\033[0m")
    print ("    - An estimate of the percentage of opponent two-point field goal attempts blocked by while on the floor.")  
    print ("31. " + "\033[1m" + "Offensive Rating" + "\033[0m")
    print ("    - An estimate of points produced (players) or scored (teams) per 100 possessions")
    print ("32. " + "\033[1m" + "Defensive Rating" + "\033[0m")
    print ("    - An estimate of points allowed per 100 possessions")
    print ("33. " + "\033[1m" + "Offensive Win Shares" + "\033[0m")
    print ("    - An estimate of the number of wins contributed by a player due to his offense.") 
    print ("34. " + "\033[1m" + "Defensive Win Shares" + "\033[0m")
    print ("    - An estimate of the number of wins contributed by a player due to his defense.")
    print ("35. " + "\033[1m" + "Win Shares Per 48 Minutes" + "\033[0m")
    print ("    - An estimate of the number of wins contributed by a player per 48 minutes (league average is approximately .100)")
    print ("36. " + "\033[1m" + "Offensive Box Plus/Minus" + "\033[0m")
    print ("    - A box score estimate of the offensive points per 100 possessions a player contributed above a league-average player.")
    print ("37. " + "\033[1m" + "Defensive Box Plus/Minus" + "\033[0m")
    print ("    - A box score estimate of the defensive points per 100 possessions a player contributed above a league-average player.") 
    print ("38. " + "\033[1m" + "Box Plus/Minus" + "\033[0m")
    print ("    - A box score estimate of the points per 100 possessions a player contributed above a league-average player.")
    print ("39. " + "\033[1m" + "Value Over Replacement Player (VORP)" + "\033[0m")
    print ("    - An estimate of the points per 100 possessions that a player contributed above a replacement-level (-2.0) player")
    print ("40. " + "\033[1m" + "CALCULATE!" + "\033[0m")

def user_input():
    #user number input to select category
    cat_num = ""
    cat_weight = ""

    while cat_num != 40:
        try:
            cat_num = int(input("\nEnter a number from 1 to 39 to select statistical category: "))
            if cat_num < 0 or cat_num > 40:
                raise ValueError 
            elif cat_num == 40:
                print ("\nCalculations Complete!\n")
                break
        except ValueError:
            print("\nThis is not a valid input. \nTry again!") 
        else:
            while True:
                try:
                    # prompt user with the category that they selected
                    cat_weight = int(input((cat_dict[cat_num] + ": ")))
                    if cat_weight < 0 or cat_weight > 10:
                        raise ValueError
                except ValueError:
                    print("\nThis is not a valid input. \nTry again!")
                else:
                    # insert cat_weight in 2nd dictionary
                    weight_dict[cat_dict[cat_num]] =  cat_weight
                    print(weight_dict)
                    break
    

# method for extracting weight dict values into list
def calculation():
    values_weight_dict = list(weight_dict.values())

    list_size = len(values_weight_dict)

    #sql query to import stats from category user chooses
    conn = pg2.connect(database = 'NBA GOAT Project', user = 'postgres', password = 'thebeatles')
    # conn = pg2.connect(database = 'postgres', user = 'postgres', password = 'pragath1')
    cur = conn.cursor()

    cur.execute('SELECT player, {} FROM all_stats'.format(", ".join(weight_dict)))

    players = cur.fetchall()

    player_list = []
    for row in players:
        player_list.append({'name': row[0], 'stats': row[1:]})

    cur.close()

    # finding min max

    #inputting zeros into empty arrays for how many categories user inputs
    min_val_array = []
    max_val_array = []
    index_val = 0
    while (index_val < list_size):
        min_val_array.append(1000000000)
        max_val_array.append(0)
        index_val += 1


    #inputting min and max values into zeroed arrays
    for person in player_list:
        index = 0
        while (index < list_size):
            cur_stat = person['stats'][index]
            if (cur_stat != None):
                if (cur_stat < min_val_array[index]):
                    min_val_array[index] = cur_stat
                if (cur_stat > max_val_array[index]):
                    max_val_array[index] = cur_stat
            index += 1

    for person in player_list:
        index_3 = 0 
        calculated_player = []
        while (index_3 < list_size):
            if (person['stats'][index_3] != None):
                # (x - min)/(max - min)
                calced_result =((person['stats'][index_3] - min_val_array[index_3])/(max_val_array[index_3] - min_val_array[index_3]))*(values_weight_dict[index_3])
                calced_result = round(calced_result, 3)
                calculated_player.append(calced_result)
            else:
                calculated_player.append(None)
            index_3 += 1

        #summing up calculated weights                            
        sum_calculated_player = 0 
        for num in calculated_player:
            if (num != None):
                sum_calculated_player = sum_calculated_player + num

        #assigning name to each calculated weight
        person['final'] = sum_calculated_player

    sorted_values = sorted(player_list, key=lambda x: x['final'], reverse=True) 

    rank = 1
    for i in range(50):
        row = sorted_values[i]
        stats = row['stats']
        print(str(rank) + ". " + str(row['name']) + ":\t" + str(row['final']) + "\t" +  ' '.join(str(x) for x in stats)) 
        rank += 1

if __name__ =='__main__':
    intro()
    user_input() 
    calculation()