from flask import Flask 
from flask import request, render_template
from prompts import reg_stats, adv_stats, adv_desc
from main import cat_dict

app = Flask(__name__)

# keeping tracking of weight values of stats
weight_dict = {}

# results of top bball players
results_dict = {}

# TODO: import calculation function
# TODO: have it take weight dict as argument
# TODO: have it return results dict
# TODO: feed results dict to results.html

# results page
@app.route('/results', methods=['POST'])
def results():
    # check weight entried for all categories
    for i in range(0, (len(reg_stats)+len(adv_stats))):
        weight = request.form['weight'+str(i)]
        # if user entered weight for category, add it to weight dict
        if (weight):
            weight_dict[cat_dict[i+1]] = weight
    return render_template(
        'results.html', 
        len=len(weight_dict),
        res=weight_dict)

# home page
@app.route('/')
def home():
    return render_template(
        'index.html', 
        reg_len=len(reg_stats),
        adv_len=len(adv_stats),
        reg_stats=reg_stats, 
        adv_stats=adv_stats, 
        adv_desc=adv_desc)

if __name__ == '__main__':
    app.run(debug=True)