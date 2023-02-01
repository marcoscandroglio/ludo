# Author: Marco Scandroglio
# GitHub username: marcoscandroglio
# Date: 8/12/2022
# Description: classes representing a game of Ludo and players.
# Player's token information is updated as the game is played.

class Player:
    """
    represents a player in the game of Ludo.
    """

    def __init__(self, position):
        """
        The constructor for the Player class.Takes the position the player chooses (A, B, C, or D) as a parameter.
        Initializes the required data members.All data members are private.
        """

        self._position = position
        self._start_space = self.set_start_space(position)
        self._end_space = self.set_end_space(position)
        self._current_position = {'p': 'H',
                                  'q': 'H'}
        self._current_state = False

    def set_start_space(self, position):
        """
        Takes one parameter:
        position - a string representing the position of the player.
        The purpose of this method is to help initialize the data member of the player object
        indicating the starting space on the board.  This data member is initialized as an integer.
        Used when a new player object is created.
        """

        if position == 'A':
            return 1
        if position == 'B':
            return 15
        if position == 'C':
            return 29
        if position == 'D':
            return 43

    def get_start_space(self):
        """
        Takes no parameters.
        Returns the integer stored in the data member that stores the starting space on the board for the player object.
        Used by the move_token() and play_game() methods of the LudoGame class.
        """

        return self._start_space

    def set_end_space(self, position):
        """
        Takes one parameter:
        position - a string representing the position of the player.
        The purpose of this method is to help initialize the data member
        of the player object indicating the ending space on the board (before the beginning of the player’s Home Row).
        This data member is initialized as an integer.
        Used when a new player object is created.
        """

        if position == 'A':
            return 50
        if position == 'B':
            return 8
        if position == 'C':
            return 22
        if position == 'D':
            return 36

    def get_end_space(self):
        """
        Takes no parameters.
        Returns the integer stored in the data member that stores the
        ending space on the board for the player object (before the beginning of the player’s Home Row).
        Used by the move_token() and play_game() methods of the LudoGame class.
        """

        return self._end_space

    def get_token_p_step_count(self):
        """
        Takes no parameters and returns the total number of steps taken by token ‘p’.
        Returns:
        -1 if token ‘p’ is in the home yard (‘H’),
        0 if token ‘p’ is in the ready to go position (‘R’),
        and an integer not to exceed 57 if it is located anywhere else on the board including in its home row.
        Used by the get_space_name() method to get its parameter value.
        Also used in the move_token() and play_game() methods for evaluating how and if to move a token.
        """

        position = self._current_position['p']

        if position == 'H':
            return -1
        elif position == 'R':
            return 0
        elif position == 'E':
            return 57
        elif isinstance(position, str) is True and self._position in position:
            return int(position[1]) + 50
        else:
            return int(position)

    def get_token_q_step_count(self):
        """
        Takes no parameters and returns the total number of steps taken by token ‘q’.
        Returns:
        -1 if token ‘q’ is in the home yard (‘H’),
        0 if token ‘q’ is in the ready to go position (‘R’),
        and an integer not to exceed 57 if it is located anywhere else on the board including in its home row.
        Used by the get_space_name() method to get its parameter value.
        Also used in the move_token() and play_game() methods for evaluating how and if to move a token.
        """

        position = self._current_position['q']

        if position == 'H':
            return -1
        elif position == 'R':
            return 0
        elif position == 'E':
            return 57
        elif isinstance(position, str) is True and self._position in position:
            return int(position[1]) + 50
        else:
            return int(position)

    def get_position(self):
        """
        Takes no parameters.
        Returns:
        The dictionary stored in the data member that stores the token names and positions.
        Used by the add_player() and get_opponents() methods of the LudoGame class to retrieve token information.
        """

        return self._position

    def get_current_position(self):
        """
        Takes no parameters.
        Returns:
        The dictionary stored in the data member that stores the token names and positions.
        Used by the play_game() method of the LudoGame class to retrieve token information.
        """

        return self._current_position

    def set_current_position(self, token, new_position):
        """
        Takes two parameters:
        token -  a string representing the name of the token being moved (‘p’ or ‘q’).
        position - the position the token is being moved to.
        The purpose of this method is to update the data member containing each player’s tokens during game play.
        Used by the move_token() method in the LudoGame class
        """

        self._current_position[token] = new_position

    def get_space_name(self, token_steps):
        """
        Takes as a parameter the number of steps taken by a token and
        Returns:
        The name of the space on which the token is located.
        Used by the move_token() and play_game() methods of the LudoGame class to evaluate
        if tokens are located on the same space (if they should be stacked or kicked).
        """

        if token_steps == -1:
            return 'H'
        if token_steps == 0:
            return 'R'
        if 1 <= token_steps <= 50:
            return str((token_steps + self.get_start_space() - 1) % 56)
        if 51 <= token_steps <= 56:
            return self._position + str(token_steps - 50)
        if token_steps == 57:
            return 'E'

    def get_completed(self):
        """
        Takes no parameters.
        Returns:
        True if the player has completed the game and False if the player is still playing the game.
        """

        collapsed_dict = list(set(list(self.get_current_position().values())))

        if len(collapsed_dict) == 1 and collapsed_dict[0] == 'E':
            self._current_state = True
            return self._current_state
        else:
            self._current_state = False
            return self._current_state

    def get_stacked(self):
        """
        Takes no parameters.
        Returns:
        True if the data member containing the stacking state of the player’s tokens is True.
        False if the data member containing the stacking state of the player’s tokens is False.
        Used by the play_game() method to determine if one or both tokens should be moved.
        """

        if 0 < self.get_token_p_step_count() == self.get_token_q_step_count():
            return True
        else:
            return False


class LudoGame:
    """
    Represents a game of Ludo.
    """

    def __init__(self):
        """
        The constructor for the LudoGame class. Takes no parameters.
        Initializes the required data members. All data members are private.
        """

        self._player_dict = {}

    def add_player(self, player_object):
        """
        method that takes as a parameter a player object and adds it to the dictionary of players for the current game
        used by the 'play_game()' method to initialize players for the current game
        """

        self._player_dict[player_object.get_position()] = player_object

    def get_player_by_position(self, player_position):
        """
        Takes one parameter:
        player_position - a string representing the player’s position and
        Returns:
        the corresponding player object.
        “Player not found!” - if an invalid string is passed as a parameter.
        Used by the play_game() method to return the player object corresponding to the current player’s turn.
        """

        position_dict = list(self._player_dict.keys())

        if player_position in position_dict:
            return self._player_dict[player_position]

        else:
            return "Player not found!"

    def get_opponents(self, player_object):
        """
        Takes one parameter:
        player_object - the player (instance of the Player class) who’s token is being moved.
        Returns:
        A dictionary of the current player's opponents with the keys corresponding to position
        and the values corresponding to the player objects.
        """

        # for comparing moves against the spaces of opposing tokens
        new_dictionary = self._player_dict.copy()
        del new_dictionary[player_object.get_position()]
        opponent_dictionary = new_dictionary

        return opponent_dictionary

    def move_token(self, player_object, token_name, token_steps):
        """
        Takes three parameters:
        player_object - the player (instance of the Player class) who’s token is being moved.
        token_name - the name of the token being moved (‘p’ or ‘q’).
        token_steps - an integer representing the number of steps the token is being moved.
        The purpose of this method is to move the player’s token by the number of steps determined by the player’s
        current turn as well as updating the token’s step count and kicking other opponent’s tokens.
        Since each player has two tokens, the token that gets moved is determined by the priority move rules
        and if the player’s tokens are stacked.
        Used by the play_game() method to updated token position information during each turn of the game.
        """

        opponents = self.get_opponents(player_object)
        opponent_position_list = []

        for opponent in opponents:
            opp_p_pos = opponents[opponent].get_space_name(opponents[opponent].get_token_p_step_count())
            opp_q_pos = opponents[opponent].get_space_name(opponents[opponent].get_token_q_step_count())
            opponent_position_list.append(opp_p_pos)
            opponent_position_list.append(opp_q_pos)

        if token_name == 'p':
            position = player_object.get_token_p_step_count()

        if token_name == 'q':
            position = player_object.get_token_q_step_count()

        new_position = position + token_steps

        if 57 < new_position:
            token_steps = (57 - position) - (position + token_steps - 57)

        new_position = position + token_steps
        token_next_space = player_object.get_space_name(position + token_steps)

        if 0 < new_position <= 50:
            player_object.set_current_position(token_name, new_position)

        if -1 <= new_position <= 0 or 51 <= new_position <= 57:
            player_object.set_current_position(token_name, token_next_space)

        if 0 < new_position <= 50 and str(token_next_space) in opponent_position_list:

            for opp in opponents:

                if opponents[opp].get_space_name(opponents[opp].get_token_p_step_count()) == token_next_space:
                    self._player_dict[opp].set_current_position('p', 'H')

                if opponents[opp].get_space_name(opponents[opp].get_token_q_step_count()) == token_next_space:
                    self._player_dict[opp].set_current_position('q', 'H')

    def play_game(self, players_list, turns_list):
        """
        Takes two parameters:
        players_list - a list of strings representing the positions of the players in the current game.
        Used to create Player objects.
        turns_list - a list of tuples with each tuple representing one turn for one player.
        For example, (‘A’,6) represents player A rolling 6.
        Returns:
        A list of token positions for each player.
        """

        for player in players_list:
            self._player_dict[player] = Player(player)

        for turn in turns_list:
            player_object = self._player_dict[turn[0]]
            moves = turn[1]
            # for determining if a token is in the Home Yard
            collapsed_dict = list(set(list(player_object.get_current_position().values())))
            # player token information:
            token_p_steps = player_object.get_token_p_step_count()
            token_q_steps = player_object.get_token_q_step_count()
            token_p_next_space = player_object.get_space_name(player_object.get_token_p_step_count() + moves)
            token_q_next_space = player_object.get_space_name(player_object.get_token_q_step_count() + moves)
            # for comparing moves against the spaces of opposing tokens
            opponents = self.get_opponents(player_object)
            opponent_position_list = []

            for opp in opponents:
                opp_p_pos = opponents[opp].get_space_name(opponents[opp].get_token_p_step_count())
                opp_q_pos = opponents[opp].get_space_name(opponents[opp].get_token_q_step_count())
                opponent_position_list.append(opp_p_pos)
                opponent_position_list.append(opp_q_pos)

            # RULE 1:
            if len(collapsed_dict) == 1 and collapsed_dict[0] == 'H' and moves == 6:
                self.move_token(player_object, 'p', 1)

            elif 'H' in collapsed_dict and moves == 6:
                # dictionary inversion to query the dictionary by value in order to return the key (token) to move
                inverted_dict = {value: key for (key, value) in player_object.get_current_position().items()}
                token_name = inverted_dict['H']
                self.move_token(player_object, token_name, 1)

            # RULE 2:
            elif player_object.get_stacked() is True and token_q_steps + moves == 57:
                self.move_token(player_object, 'p', moves)
                self.move_token(player_object, 'q', moves)

            # IF BOTH ARE IN THE HOME ROW
            elif 51 <= token_p_steps < token_q_steps and token_p_steps + moves == 57:
                self.move_token(player_object, 'p', moves)

            elif 51 <= token_q_steps < token_p_steps and token_q_steps + moves == 57:
                self.move_token(player_object, 'q', moves)

            # IF p IS IN THE HOME ROW
            elif 51 <= token_p_steps and token_p_steps + moves == 57:
                self.move_token(player_object, 'p', moves)

            # IF q IS IN THE HOME ROW
            elif 51 <= token_q_steps and token_q_steps + moves == 57:
                self.move_token(player_object, 'q', moves)

            # RULE 3:
            elif player_object.get_stacked() is True and token_p_next_space in opponent_position_list:
                self.move_token(player_object, 'p', moves)
                self.move_token(player_object, 'q', moves)

            elif token_p_next_space in opponent_position_list:
                self.move_token(player_object, 'p', moves)

            elif token_q_next_space in opponent_position_list:
                self.move_token(player_object, 'q', moves)

            elif 0 <= token_p_steps < token_q_steps and token_p_next_space in opponent_position_list:
                self.move_token(player_object, 'p', moves)

            elif 0 <= token_q_steps < token_p_steps and token_q_next_space in opponent_position_list:
                self.move_token(player_object, 'q', moves)

            # RULE 4:
            elif player_object.get_stacked() is True and 0 < token_p_steps < 57:
                self.move_token(player_object, 'p', moves)
                self.move_token(player_object, 'q', moves)

            elif token_q_steps == token_p_steps and token_p_steps == 0:
                self.move_token(player_object, 'p', moves)

            elif 0 <= token_p_steps < token_q_steps:
                self.move_token(player_object, 'p', moves)

            elif 0 <= token_q_steps < token_p_steps:
                self.move_token(player_object, 'q', moves)

            # move token in Ready to Play position if the other is in the Home Yard
            elif 0 <= token_p_steps and token_q_steps == -1:
                self.move_token(player_object, 'p', moves)

            elif 0 <= token_q_steps and token_p_steps == -1:
                self.move_token(player_object, 'q', moves)

        end_list = []

        for player in self._player_dict.values():
            end_list.append(player.get_space_name(player.get_token_p_step_count()))
            end_list.append(player.get_space_name(player.get_token_q_step_count()))

        return end_list
