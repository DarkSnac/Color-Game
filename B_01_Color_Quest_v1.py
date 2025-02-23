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
    highest = int_scores[-1]

    return round_colors, median, highest


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

        # Strings for labels
        intro_string = "In each round you will be invited to choose a color. Your goal is " \
                       "to beat the target score and win the round (and keep your points)."

        # Choose_string = "Oops - please choose a whole number more than zero."
        choose_string = "How many rounds do you want to play?"

        # List of labels to be made (text | font | fg)
        start_labels_list = [
            ["Color Quest", "Arial 16 bold", None],
            [intro_string, "Arial 12", None],
            [choose_string, "Arial 12 bold", "#009900"]
        ]

        # Create labels and add them to the reference list...

        start_label_ref = []
        for count, item in enumerate(start_labels_list):
            make_label = Label(self.start_frame, text=item[0],
                               font=item[1], fg=item[2],
                               wraplength=350, justify='left',
                               pady=10, padx=20)
            make_label.grid(row=count)

            start_label_ref.append(make_label)

        # Extract choice label so that it can be changed to an
        # error message if necessary
        self.choose_label = start_label_ref[2]

        # Frame so that the entry box and button can be in the same row
        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=3)

        self.num_rounds_entry = Entry(self.entry_area_frame,
                                      font="Arial 20 bold", width=10)
        self.num_rounds_entry.grid(row=0, column=0, padx=10, pady=10)

        # Create play button...
        self.play_button = Button(self.entry_area_frame,
                                  font="Arial 16 bold",
                                  fg="#FFFFFF", bg="#0057d8",
                                  text="Play", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1)

    def check_rounds(self):
        """
        Checks users have 1 or more rounds
        """

        # Retrieve temperature to be converted
        rounds_wanted = self.num_rounds_entry.get()

        # Reset label and entry box (for when users come back to home screen)
        self.choose_label.config(fg="#009900", font="Arial 12 bold")
        self.num_rounds_entry.config(bg="#FFFFFF")

        error = "Oops - Please choose a whole number more than zero."
        has_errors = "no"

        # Checks that number of rounds is more than zero
        try:
            rounds_wanted = int(rounds_wanted)
            if rounds_wanted > 0:
                # Invoke Play Class (and take across number of rounds)
                Play(rounds_wanted)
                # Hide root window (ie: hide rounds choice window).
                root.withdraw()
                # Clear out the input box and reset label
                self.num_rounds_entry.delete(0, END)
                self.choose_label.config(text="How many rounds do you want to play?")

            else:
                has_errors = "yes"
        except ValueError:
            has_errors = "yes"

        # Display the error if necessary
        if has_errors == "yes":
            self.choose_label.config(text=error, fg="#990000",
                                     font="Arial 10 bold")
            self.num_rounds_entry.config(bg="#F4CCCC")
            self.num_rounds_entry.delete(0, END)


class Play:
    """
    Interface for playing the color quest game
    """

    def __init__(self, how_many):

        # Integers / String Variables
        self.target_score = IntVar()

        # Rounds played - start with zero
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        # Color lists and score list
        self.round_color_list = []
        self.all_scores_list = []
        self.all_medians_list = []
        self.all_high_score_list = []

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
            self.make_label = Label(self.game_frame, text=item[0],
                                    font=item[1], bg=item[2],
                                    wraplength=300, justify='left')
            self.make_label.grid(row=item[3], pady=10, padx=10)

            play_labels_ref.append(self.make_label)

        # Retrieve labels so they can be configured later
        self.heading_label = play_labels_ref[0]
        self.target_label = play_labels_ref[1]
        self.results_label = play_labels_ref[3]

        # Set up color buttons
        self.color_frame = Frame(self.game_frame)
        self.color_frame.grid(row=3)

        self.color_button_ref = []
        self.button_color_list = []

        # Create four buttons in a 2 x 2 grid
        for item in range(0, 4):
            self.color_button = Button(self.color_frame, font=body_font,
                                       text="Color Name", width=15,
                                       command=partial(self.round_results, item))
            self.color_button.grid(row=item // 2,
                                   column=item % 2,
                                   padx=5, pady=5)
            self.color_button_ref.append(self.color_button)

        # Frame to hold hints and stats buttons
        self.hints_stats_frame = Frame(self.game_frame)
        self.hints_stats_frame.grid(row=6)

        # List for buttons (frame | text | bg | command | width | row | column)
        control_button_list = [
            [self.game_frame, "Next Round", "#0057D8", self.new_round, 21, 5, None],
            [self.hints_stats_frame, "Hints", "#FF8000", self.to_hints, 10, 0, 0],
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

        # Retrieve next, stats and end button so that they can be configured
        self.next_button = control_ref_list[0]
        self.hints_button = control_ref_list[1]
        self.stats_button = control_ref_list[2]
        self.end_game_button = control_ref_list[3]

        # Once interface has been created, invoke new
        # round function for first round.
        self.new_round()

    def new_round(self):
        """
        Chooses four colors, works out median for score to beat.
        configures buttons with chosen colors.
        """

        # Retrieve number of rounds played, add one to it and configure heading
        rounds_played = self.rounds_played.get()
        rounds_played += 1
        self.rounds_played.set(rounds_played)

        rounds_wanted = self.rounds_wanted.get()

        # Get round colors and median score...
        self.round_color_list, median, highest = get_round_colors()

        # Set target score as median (for later comparison)
        self.target_score.set(median)

        self.all_medians_list.append(median)

        self.all_high_score_list.append(highest)

        # Update heading and score to beat labels. "hide" results label
        self.heading_label.config(text=f"Round {rounds_played} of {rounds_wanted}")
        self.target_label.config(text=f"Target Score: {median}", font="Arial 14 bold")
        self.results_label.config(text=f"{'=' * 7}", bg="#F0F0F0")

        # Configure buttons using foreground and background colors from list
        # enable color buttons (disabled at the end of the last round)
        for count, item in enumerate(self.color_button_ref):
            item.config(fg=self.round_color_list[count][2],
                        bg=self.round_color_list[count][0],
                        text=self.round_color_list[count][0],
                        state=NORMAL)

        self.next_button.config(state=DISABLED)

    def round_results(self, user_choice):
        """
        Retrieves which button was pushed (index 0 - 3), retrieves
        score and then compares it with median, updates results and
        adds results to stats list.
        """

        # Get user score and color based on button press...
        score = int(self.round_color_list[user_choice][1])

        # Alternate way to get button name. Good for if buttons have been scrambled
        color_name = self.color_button_ref[user_choice].cget('text')

        # Retrieve target score and compare with user score to find round result
        target = self.target_score.get()

        if score >= target:
            result_text = f"Success! {color_name} earned you {score} points."
            result_bg = "#82B366"
            self.all_scores_list.append(score)
        else:
            result_text = f"Oops {color_name} ({score}) is less than the target."
            result_bg = '#F8CECC'
            self.all_scores_list.append(0)

        self.results_label.config(text=result_text, bg=result_bg)

        # Printing area to generate text data for stats (delete when done)
        print("All Scores", self.all_scores_list)
        print("All Medians:", self.all_medians_list)
        print("Highest Scores: ", self.all_high_score_list)

        # Enable stats & next buttons, disable color buttons
        self.next_button.config(state=NORMAL)
        self.stats_button.config(state=NORMAL)

        # Check to see if game is over
        rounds_played = self.rounds_played.get()
        rounds_wanted = self.rounds_wanted.get()

        if rounds_played == rounds_wanted:
            self.next_button.config(state=DISABLED, text="Game Over")
            self.end_game_button.config(text="Play Again", bg="#006600")

        for item in self.color_button_ref:
            item.config(state=DISABLED)

    def close_play(self):
        # Reshow root (ie: choose rounds) and end
        # current game / allow new game to start
        root.deiconify()
        self.play_box.destroy()

    def to_hints(self):
        """
        Displays hints for playing game
        """
        DisplayHints(self)


class DisplayHints:
    """
    Displays hints for color quest game
    """

    def __init__(self, partner):
        # setup dialogue box and background color
        background = "#ffe6cc"
        self.hint_box = Toplevel()

        # Disable help button
        partner.hints_button.config(state=DISABLED)

        # If users press cross at top, closes help
        # and enables help button
        self.hint_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_hints, partner))

        # Set up the frame
        self.hint_frame = Frame(self.hint_box, width=300,
                                height=200)
        self.hint_frame.grid()

        # Set up heading
        self.hint_heading_label = Label(self.hint_frame,
                                        text="Hints",
                                        font="Arial 14 bold")
        self.hint_heading_label.grid(row=0)

        hint_text = "The score for each color relates to it's hexadecimal code.\n\n" \
                    "Remember, the hex code for which is #FFFFFF which is th best possible score.\n\n" \
                    "The hex code for black is #000000 which is the worst possible score.\n\n" \
                    "The first color in the code is red, so if you had to choose between red " \
                    "(#FF0000), green (#00FF00) and blue (#0000FF), then red would be the best choice.\n\n" \
                    "Good Luck!"

        # Set up text
        self.hint_text_label = Label(self.hint_frame,
                                     text=hint_text,
                                     wraplength=350,
                                     justify="left")
        self.hint_text_label.grid(row=1, padx=10)

        # Set up dismiss button
        self.dismiss_button = Button(self.hint_frame,
                                     font="Arial 12 bold",
                                     text="Dismiss",
                                     bg="#cc6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_hints, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        # List and loop to set background color on
        # everything except the buttons
        recolor_list = [self.hint_frame, self.hint_heading_label,
                        self.hint_text_label]

        for item in recolor_list:
            item.config(bg=background)

    def close_hints(self, partner):
        """
       Closes help dialogue box (and enables help button)
        """
        # Put help button back to normal...
        partner.hints_button.config(state=NORMAL)
        self.hint_box.destroy()


# Main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Color Quest")
    StartGame()
    root.mainloop()
