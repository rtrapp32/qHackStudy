from flask import Flask, render_template, request, redirect, url_for
import os
import sys

# Ensure the QLearning module can be found by Python
current_dir = os.getcwd()
sys.path.append(current_dir)

from qlearning import QLearning

# Configuration parameters for Q-learning
ALPHA = 0.1
GAMMA = 0.6
EPSILON = 0.1

# Define your states and actions, including the new leisure action
states = ['before_exercise_high_energy', 'before_exercise_low_energy',
          'after_exercise_high_energy', 'after_exercise_low_energy']
actions = ['study_30min', 'study_1hr', 'complete_lab', 'read_10pages', 'take_break', 'leisure_30min']

# Initialize the QLearning class with dynamic parameters
qlearning = QLearning(states, actions, epsilon=EPSILON, alpha=ALPHA, gamma=GAMMA)

# Mapping actions to their respective durations in seconds
action_durations = {
    'study_30min': 30 * 60,
    'study_1hr': 60 * 60,
    'complete_lab': 120 * 60,
    'read_10pages': 45 * 60,
    'take_break': 15 * 60,
    'leisure_30min': 30 * 60
}

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        exercise = request.form.get('exercise')
        energy = request.form.get('energy')
        combined_state = f"{exercise}_{energy}"
        
        action = qlearning.choose_action(combined_state)
        duration_seconds = action_durations.get(action, 30 * 60)  # Default to 30 minutes if action not found
        
        return render_template('action.html', action=action, state=combined_state, duration=duration_seconds)
    
    return render_template('index.html', exercises=['before_exercise', 'after_exercise'], energies=['high_energy', 'low_energy'])

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        state = request.form.get('state')
        action = request.form.get('action')
        actual_duration = int(request.form.get('duration', 0))
        feeling = request.form.get('feeling')

        reward = qlearning.calculate_reward({
            'actual_duration': actual_duration,
            'feeling': feeling
        })

        qlearning.update_q_values(state, action, reward)
        qlearning.save_q_table()

        return redirect(url_for('index'))
    else:
        # Assuming state and action need to be passed for rendering the form
        return render_template('feedback_form.html')

if __name__ == "__main__":
    app.run(debug=True)

