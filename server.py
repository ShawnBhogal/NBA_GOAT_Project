from flask import Flask 
from flask import request, render_template
from prompts import reg_stats, adv_stats, adv_desc
from methods import cat_dict, calculation

app = Flask(__name__)

# keeping tracking of weight values of stats
weight_dict = {}

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
    results_dict = calculation(weight_dict)
    return render_template(
        'results.html', 
        len_weight=len(weight_dict),
        weight=weight_dict,
        res=results_dict)

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