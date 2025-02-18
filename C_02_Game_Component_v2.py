from tkinter import *
from functools import partial  # To prevent unwanted windows
import csv
import random


# Helper functions go here
def round_ans(val):
    """
    Rounds the answer to the nearest whole number
    :param val: Number to be rounded
    :return: Rounded number
    """
    var_rounded = (val * 2 + 1) // 2
    raw_rounded = f"{var_rounded:.0f}"
    return int(raw_rounded)


def get_colors():
    """
    Retrieves colors from csv file
    :return: List of colors which where each list item has the
    color name, associated score and foreground color for the text
    """

    # Retrieve colors from csv file and put them in a list
    file = open("00_colour_list_hex_v3.csv", 'r')
    all_colors = list(csv.reader(file, delimiter=","))
    file.close()

    # Remove the first row
    all_colors.pop(0)

    return all_colors


def get_round_colors():
    """
    Choose four colors from larger list ensuring that the scores are all different.
    :return: List of colors and score to beat (Median of scores)
    """

    all_color_list = get_colors()

    # Set up lists
    round_colors = []
    color_scores = []

    # Loop until we have four colors with different scores...
    while len(round_colors) < 4:
        potential_color = random.choice(all_color_list)

        # Get the score and check it's not a duplicate
        if potential_color[1] not in color_scores:
            round_colors.append(potential_color)
            color_scores.append(potential_color[1])

    # Find target score (median)

    # Change scores to integers
    int_scores = [int(x) for x in color_scores]
    int_scores.sort()

    median = (int_scores[1] + int_scores[2]) / 2
    median = round_ans(median)

    return round_colors, median


# Classes start here
class StartGame:
    """
    Initial Game interface (asks users how many
    rounds they would like to play)
    """

    def __init__(self):
        """
        Gets number of round from user
        """

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # Create play button...
        self.play_button = Button(self.start_frame,
                                  font="Arial 16 bold",
                                  fg="#FFFFFF", bg="#0057d8",
                                  text="Play", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1)

    def check_rounds(self):
        """
        Checks users have 1 or more rounds
        """

        Play(5)
        # Hide root window (ie: hide rounds choice window).
        root.withdraw()


class Play:
    """
    Interface for playing the color quest game
    """

    def __init__(self, how_many):
        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        # Body font for most labels
        body_font = "Arial 12"

        # List for label details (text | font | background | row)
        play_label_list = [
            ["Round # of #", "Arial 16 bold", None, 0],
            ["Score to beat: #", body_font, "#FFF2CC", 1],
            ["Choose a colour below. Good luck. 🍀", body_font, "#D5E8D4", 2],
            ["You chose, result", body_font, "#D5E8D4", 4]
        ]

        play_labels_ref = []
        for item in play_label_list:
            make_label = Label(self.game_frame, text=item[0],
                               font=item[1], bg=item[2],
                               wraplength=300, justify='left')
            make_label.grid(row=item[3], pady=10, padx=10)

            play_labels_ref.append(item)

        # Retrieve labels so they can be configured later
        self.heading_label = play_labels_ref[0]
        self.target_label = play_labels_ref[1]
        self.results_label = play_labels_ref[3]

        # Set up color buttons
        self.color_frame = Frame(self.game_frame)
        self.color_frame.grid(row=3)

        # Create four buttons in a 2 x 2 grid
        for item in range(0, 4):
            self.color_button = Button(self.color_frame, font=body_font,
                                       text="Color Name", width=15)
            self.color_button.grid(row=item // 2,
                                   column=item % 2,
                                   padx=5, pady=5)

        # Frame to hold hints and stats buttons
        self.hints_stats_frame = Frame(self.game_frame)
        self.hints_stats_frame.grid(row=6)

        # List for buttons (frame | text | bg | command | width | row | column)
        control_button_list = [
            [self.game_frame, "Next Round", "#0057D8", "", 21, 5, None],
            [self.hints_stats_frame, "Hints", "#FF8000", "", 10, 0, 0],
            [self.hints_stats_frame, "Stats", "#333333", "", 10, 0, 1],
            [self.game_frame, "End", "#990000", self.close_play, 21, 7, None]
        ]

        # # Create buttons and add to list
        control_ref_list = []
        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1],
                                         bg=item[2], command=item[3],
                                         font="Arial 16 bold", fg="#FFFFFF",
                                         width=item[4])
            make_control_button.grid(row=item[5], column=item[6], pady=5, padx=5)

            control_ref_list.append(make_control_button)

    def close_play(self):
        # Reshow root (ie: choose rounds) and end
        # current game / allow new game to start
        root.deiconify()
        self.play_box.destroy()


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Color Quest")
    StartGame()
    root.mainloop()
