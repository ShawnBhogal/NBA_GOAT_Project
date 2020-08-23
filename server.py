from flask import Flask, flash, request, render_template, redirect, url_for
from prompts import reg_stats, adv_stats, adv_desc, cat_dict, cat_name
from methods import calculation

app = Flask(__name__)
app.secret_key = "kobe is the goat"

# keeping tracking of weight values of stats
weight_dict = {}
stat_names = []

# results page
@app.route("/results", methods=['GET', 'POST'])
def results():
    if request.method == "POST":
        # check weight entried for all categories
        for i in range(0, (len(reg_stats)+len(adv_stats))):
            weight = request.form['weight'+str(i)]
            # if user entered weight for category, add it to weight dict
            if (weight):
                weight_dict[cat_dict[i+1]] = weight
                # add stat name for printing purposes
                stat_name = cat_name[cat_dict[i+1]]
                if stat_name not in stat_names:
                    stat_names.append(stat_name)
        # if user did not select any stats, send alert
        if len(weight_dict) == 0:
            flash('Must select at least one statistic', 'error')
            return redirect(url_for('home'))
    # calculate goat players
    results_dict = calculation(weight_dict)
    # display results
    return render_template(
        'results.html', 
        len_weight=len(weight_dict),
        weight_dict=weight_dict,
        stat_names=stat_names,
        cat_name=cat_name,
        res=results_dict)


# edit entry
@app.route("/edit_entry", methods=['GET', 'POST'])
def edit():
    return render_template(
        'edit_entry.html',
        reg_len=len(reg_stats),
        adv_len=len(adv_stats),
        reg_stats=reg_stats, 
        adv_stats=adv_stats, 
        adv_desc=adv_desc,
        cat_dict=cat_dict,
        weight_dict=weight_dict)


# home page
@app.route("/", methods=['GET', 'POST'])
def home():
    # new entry
    if request.method == 'GET':
        weight_dict.clear()
        stat_names.clear()
    return render_template(
        'index.html', 
        reg_len=len(reg_stats),
        adv_len=len(adv_stats),
        reg_stats=reg_stats, 
        adv_stats=adv_stats, 
        adv_desc=adv_desc,
        weight_dict=weight_dict)

if __name__ == '__main__':
    app.run(debug=True)