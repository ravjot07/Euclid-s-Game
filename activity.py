#!/usr/bin/env python3
from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityToolbarButton, StopButton, ToolButton
from gi.repository import Gtk, GObject
import game_logic

class EuclidsGameActivity(activity.Activity):
    def __init__(self, handle):
        super(EuclidsGameActivity, self).__init__(handle)
        self.set_title("Euclid's Game")
        
        # Initialize game state
        self.player_moves = 0
        self.computer_moves = 0
        self.is_player_turn = True
        self.selected_numbers = []  # To store player’s selected numbers
        self.board = game_logic.initialize_board()
        
        self._setup_toolbar()
        self._build_canvas_ui()
        self._update_ui()
        self.show_all()
    
    def _setup_toolbar(self):
        toolbar_box = ToolbarBox()
        self.set_toolbar_box(toolbar_box)
        
        # Activity button
        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(activity_button, -1)
        activity_button.show()
        
        # New Game button
        new_game_button = ToolButton('view-refresh')
        new_game_button.set_tooltip("New Game")
        new_game_button.connect('clicked', self._new_game)
        toolbar_box.toolbar.insert(new_game_button, -1)
        new_game_button.show()
        
        # Separator and Stop button
        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()
        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()
        toolbar_box.show()
    
    def _build_canvas_ui(self):
        vbox = Gtk.VBox(spacing=10)
        vbox.set_border_width(15)
        
        # Label for turn information and move counts
        self.info_label = Gtk.Label(label="")
        vbox.pack_start(self.info_label, False, False, 0)
        
        # FlowBox to display board numbers as toggle buttons
        self.board_box = Gtk.FlowBox()
        self.board_box.set_max_children_per_line(10)
        self.board_box.set_selection_mode(Gtk.SelectionMode.NONE)
        vbox.pack_start(self.board_box, True, True, 0)
        
        # Button for the player to take the difference
        self.diff_button = Gtk.Button(label="Take Difference")
        self.diff_button.connect("clicked", self._on_take_difference)
        vbox.pack_start(self.diff_button, False, False, 0)
        
        # Button to clear current selection
        self.clear_button = Gtk.Button(label="Clear Selection")
        self.clear_button.connect("clicked", self._clear_selection)
        vbox.pack_start(self.clear_button, False, False, 0)
        
        # Label for game messages (e.g. move feedback, game over)
        self.message_label = Gtk.Label(label="")
        vbox.pack_start(self.message_label, False, False, 0)
        
        self.set_canvas(vbox)
        vbox.show_all()
    
    def _update_ui(self):
        # Update information label with whose turn and move counts.
        turn_text = "Your Turn" if self.is_player_turn else "Computer's Turn"
        self.info_label.set_text(f"{turn_text} | Your Moves: {self.player_moves} | Computer Moves: {self.computer_moves}")
        
        # Update board display: remove existing children and add a toggle button for each number.
        for child in self.board_box.get_children():
            self.board_box.remove(child)
        for number in self.board:
            btn = Gtk.ToggleButton(label=str(number))
            btn.set_size_request(50, 50)
            btn.connect("toggled", self._on_number_toggled, number)
            self.board_box.add(btn)
        self.board_box.show_all()
    
    def _on_number_toggled(self, button, number):
        # Track player's selection of board numbers.
        if button.get_active():
            if number not in self.selected_numbers:
                self.selected_numbers.append(number)
        else:
            if number in self.selected_numbers:
                self.selected_numbers.remove(number)
        if len(self.selected_numbers) > 2:
            self.message_label.set_text("Select only 2 numbers.")
    
    def _clear_selection(self, widget):
        self.selected_numbers = []
        for child in self.board_box.get_children():
            if isinstance(child, Gtk.ToggleButton):
                child.set_active(False)
        self.message_label.set_text("")
    
    def _on_take_difference(self, widget):
        # Process player's move only if it's their turn.
        if not self.is_player_turn:
            return
        if len(self.selected_numbers) != 2:
            self.message_label.set_text("Select exactly 2 numbers.")
            return
        
        a, b = self.selected_numbers
        diff = abs(a - b)
        if diff == 0:
            self.message_label.set_text("Difference is zero; invalid move.")
            self._clear_selection(None)
            return
        if diff in self.board:
            self.message_label.set_text("Number already present on the board.")
            self._clear_selection(None)
            return
        
        # Valid move: add the difference to the board.
        self.board = game_logic.add_number(self.board, diff)
        self.player_moves += 1
        self.message_label.set_text(f"You added {diff}.")
        self._clear_selection(None)
        self._update_ui()
        
        if game_logic.is_game_over(self.board):
            self._end_game()
            return
        
        # Switch to computer's turn.
        self.is_player_turn = False
        self._update_ui()
        GObject.timeout_add(1000, self._computer_turn)
    
    def _computer_turn(self):
        move = game_logic.computer_move(self.board)
        if move is None:
            self._end_game()
            return False
        self.board = game_logic.add_number(self.board, move)
        self.computer_moves += 1
        self.message_label.set_text(f"Computer added {move}.")
        self._update_ui()
        
        if game_logic.is_game_over(self.board):
            self._end_game()
            return False
        
        # Switch back to player's turn.
        self.is_player_turn = True
        self._update_ui()
        return False  # Stop the timeout callback.
    
    def _end_game(self):
        # Determine the winner based on even number of moves.
        # Winner is the player who has made an even number of moves.
        winner = None
        if self.player_moves % 2 == 0:
            winner = "You"
        elif self.computer_moves % 2 == 0:
            winner = "Computer"
        else:
            winner = "No one"
        self.message_label.set_text(
            f"Game Over! Winner: {winner}. (Your Moves: {self.player_moves}, Computer Moves: {self.computer_moves})"
        )
        self.diff_button.set_sensitive(False)
    
    def _new_game(self, widget):
        self.board = game_logic.initialize_board()
        self.player_moves = 0
        self.computer_moves = 0
        self.is_player_turn = True
        self.selected_numbers = []
        self.diff_button.set_sensitive(True)
        self.message_label.set_text("")
        self._update_ui()
    
    def write_file(self, file_path):
        import json
        data = {
            'board': self.board,
            'player_moves': self.player_moves,
            'computer_moves': self.computer_moves,
            'is_player_turn': self.is_player_turn,
        }
        with open(file_path, 'w') as f:
            json.dump(data, f)
    
    def read_file(self, file_path):
        import json
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            self.board = data.get('board', game_logic.initialize_board())
            self.player_moves = data.get('player_moves', 0)
            self.computer_moves = data.get('computer_moves', 0)
            self.is_player_turn = data.get('is_player_turn', True)
            self._update_ui()
        except Exception:
            self._new_game(None)
