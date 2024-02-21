import os
import random 
import pandas as pd
from pandas.errors import EmptyDataError

class QLearning:
    def __init__(self, states, actions, filename='q_table.csv', epsilon=0.1, alpha=0.1, gamma=0.6):
        self.states = states
        self.actions = actions
        self.filename = filename
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.q_table = self.load_or_initialize_q_table()

    def load_or_initialize_q_table(self):
        if os.path.exists(self.filename):
            try:
                q_table = pd.read_csv(self.filename, index_col=0)
                if q_table.empty or not set(self.actions).issubset(q_table.columns) or not set(self.states).issubset(q_table.index):
                    print("CSV is empty or incorrectly structured. Initializing new Q-table.")
                    q_table = self.initialize_q_table()
            except EmptyDataError:
                print("CSV file is empty or invalid. Initializing new Q-table.")
                q_table = self.initialize_q_table()
        else:
            q_table = self.initialize_q_table()
        return q_table

    def initialize_q_table(self):
        return pd.DataFrame(0, index=self.states, columns=self.actions)

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        else:
            self.ensure_state_in_q_table(state)
            return self.q_table.loc[state].idxmax()

    def update_q_values(self, state, action, reward):
        self.ensure_state_action_in_q_table(state, action)
        next_max = self.q_table.loc[state].max()
        q_value = self.q_table.at[state, action]
        self.q_table.at[state, action] = q_value + self.alpha * (reward + self.gamma * next_max - q_value)

    def ensure_state_in_q_table(self, state):
        if state not in self.q_table.index:
            self.q_table = self.q_table.append(pd.Series(0, index=self.q_table.columns, name=state))

    def ensure_state_action_in_q_table(self, state, action):
        if state not in self.q_table.index or action not in self.q_table.columns:
            self.initialize_q_table()  # Reinitialize to include new state or action

    def save_q_table(self):
        self.q_table.to_csv(self.filename)

    def calculate_reward(self, feedback):
        # Basic logic to calculate reward based on feedback
        reward = 0
        if feedback['duration'] >= feedback['target_duration']:
            reward += 1  # Positive feedback for meeting/exceeding target duration
        if feedback['feeling'] == 'motivated':
            reward += 1  # Additional reward for positive well-being feedback
        elif feedback['feeling'] == 'dread':
            reward -= 2  # Negative reward for indication of potential burnout
        return reward
