# Q-HackStudy
 Use Q Learning reinforcment on your own mind. Go forth, Hack,  and get those rewards!

This project implements a Q-Learning algorithm to suggest study actions based on the current state. The user can input their current state, such as energy level and exercise status, and the system suggests an appropriate study action using reinforcement learning.
I was inspired after reading about Skinners "behaviorism" and how it is used to train animals. Humans are animals. Maybe I can optimize my own study habits

## Overview

The Q-Learning algorithm is implemented using Python, Flask, and Pandas. Flask is used to create a web interface where users can input their current state and receive study action suggestions. Pandas is used for data manipulation and storage of the Q-table. Q-Learning is a form of reinforcement learning where an agent learns to make decisions by maximizing its expected long-term reward. The goal is to create study habits that lead to you studying more and avoiding burnout.

## Requirements

- Python 3.x
- Flask
- Pandas

## Installation

1. Clone this repository to your local machine:
2. cd to the repo from the Windows terminal
3. Install the required Python packages using pip:  ``pip install -r requirements.txt``
4. From inside your windows terminal, Start the program like ``python app.py``
5. Open your web browser and go to `http://localhost:5000` to access the application.
6. Enter your current state information and click submit to receive a study action suggestion.

