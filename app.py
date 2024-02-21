from flask import Flask, render_template, request, redirect, url_for
from qlearning import QLearning

# Configuration parameters for Q-learning
ALPHA = 0.1  # Learning rate
GAMMA = 0.6  # Discount factor
EPSILON = 0.1  # Exploration rate

# Define your states and actions
states = ['before_exercise', 'after_exercise', 'low_energy', 'high_energy']
actions = ['study_30min', 'study_1hr', 'complete_lab', 'read_10pages', 'take_break']

# Initialize the QLearning class with dynamic parameters
qlearning = QLearning(states, actions, epsilon=EPSILON, alpha=ALPHA, gamma=GAMMA)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        state = request.form['state']
        action = qlearning.choose_action(state)
        return render_template('action.html', action=action, state=state)
    return render_template('index.html', states=states)

@app.route('/update', methods=['POST'])
def update():
    state = request.form['state']
    action = request.form['action']
    reward = int(request.form['reward'])
    qlearning.update_q_values(state, action, reward)
    qlearning.save_q_table()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
