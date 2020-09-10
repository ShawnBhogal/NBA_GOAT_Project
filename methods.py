# import relevant libraries/frameworks
from decimal import *
import psycopg2 as pg2
from prompts import cat_dict, cat_name

# method for extracting weight dict values into list
def calculation(weight_dict):
    results_dict = []

    if (len(weight_dict) == 0):
        return results_dict

    values_weight_dict = list(weight_dict.values())
    keys_weight_dict = list(weight_dict.keys())

    list_size = len(values_weight_dict)

    #sql query to import stats from category user chooses
    # conn = pg2.connect(database = 'NBA GOAT Project', user = 'postgres', password = 'thebeatles')
    # conn = pg2.connect(database = 'postgres', user = 'postgres', password = 'pragath1')
    conn = pg2.connect(user="postgres", password="Lakers24fan!", host='34.66.74.23', port='5432')
    cur = conn.cursor()

    cur.execute('SELECT player, {} FROM all_stats'.format(", ".join(weight_dict)))

    players = cur.fetchall()

    player_list = []
    for row in players:
        player_list.append({'name': row[0], 'stats': row[1:]})

    cur.close()

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
        # each chosen stat of player
        person['stat_dict'] = {}
        while (index_3 < list_size):
            if (person['stats'][index_3] != None):
                # Calculate weighted stat -> (x - min)/(max - min)
                calced_result =((Decimal(person['stats'][index_3]) - min_val_array[index_3])/(max_val_array[index_3] - 
                    min_val_array[index_3]))*(Decimal(values_weight_dict[index_3]))
                calced_result = round(calced_result, 3)
                calculated_player.append(calced_result)
                # add catergory names to stats
                key = keys_weight_dict[index_3]
                person['stat_dict'][key] = Decimal(person['stats'][index_3])
            else:
                calculated_player.append(None)
            index_3 += 1

        #summing up calculated weights                            
        sum_calculated_player = 0 
        for num in calculated_player:
            if (num != None):
                sum_calculated_player = sum_calculated_player + num

        #assigning calculated weight to each name
        person['final'] = sum_calculated_player


    sorted_values = sorted(player_list, key=lambda x: x['final'], reverse=True) 

    rank = 1
    for i in range(50):
        row = sorted_values[i]
        stats = {}
        player_dict = {}
        player_dict['rank'] = rank
        player_dict['name'] = row['name']
        player_dict['final'] = row['final']

        for k in row['stat_dict']:
            # stat_dict: {name: value, name2: value2}
            stat_name = cat_name[k]
            stats[stat_name] = str(row['stat_dict'][k])

        player_dict['stats'] = stats

        results_dict.append(player_dict)

        # print(str(rank) + ". " + str(row['name']) + ":\t" + str(row['final']) + "\t" +  ' '.join(str(x) for x in stats)) 
        rank += 1
    
    return results_dict