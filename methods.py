# import relevant libraries/frameworks
from decimal import *
import psycopg2 as pg2

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

# method for extracting weight dict values into list
def calculation(weight_dict):
    results_dict = []
    values_weight_dict = list(weight_dict.values())

    list_size = len(values_weight_dict)

    #sql query to import stats from category user chooses
    # conn = pg2.connect(database = 'NBA GOAT Project', user = 'postgres', password = 'thebeatles')
    conn = pg2.connect(database = 'postgres', user = 'postgres', password = 'pragath1')
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
                calced_result =((person['stats'][index_3] - min_val_array[index_3])/(max_val_array[index_3] - 
                    min_val_array[index_3]))*(Decimal(values_weight_dict[index_3]))
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
        stats = []
        player_dict = {}
        # [{rank: 1, name: bob, final: 5.5, stats: [3, 4]}, {rank: 1, name: bob, final: 5.5, stats: [3, 4]}]
        player_dict['rank'] = rank
        player_dict['name'] = row['name']
        player_dict['final'] = row['final']

        for x in row['stats']:
            stats.append(str(x))
        player_dict['stats'] = stats

        results_dict.append(player_dict)

        # print(str(rank) + ". " + str(row['name']) + ":\t" + str(row['final']) + "\t" +  ' '.join(str(x) for x in stats)) 
        rank += 1
    
    return results_dict