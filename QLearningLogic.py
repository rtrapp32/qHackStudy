import os
import random
import pandas as pd

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
            # Attempt to load the CSV file
            q_table = pd.read_csv(self.filename, index_col=0)
            # Check if the loaded table is empty or if it doesn't contain the expected columns
            if q_table.empty or not all(col in q_table.columns for col in self.actions) or not all(idx in q_table.index for idx in self.states):
                # Initialize Q-table since the file is empty or corrupted
                print("Found CSV is empty or not correctly structured. Initializing new Q-table.")
                q_table = pd.DataFrame(0, index=self.states, columns=self.actions)
            return q_table
        else:
            # File doesn't exist, initialize a new Q-table
            q_table = pd.DataFrame(0, index=self.states, columns=self.actions)
            return q_table

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        else:
            return self.q_table.loc[state].idxmax()

    def update_q_values(self, state, action, reward):
        next_max = self.q_table.loc[state].max()
        q_value = self.q_table.at[state, action]
        self.q_table.at[state, action] = q_value + self.alpha * (reward + self.gamma * next_max - q_value)

    def save_q_table(self):
        self.q_table.to_csv(self.filename)
