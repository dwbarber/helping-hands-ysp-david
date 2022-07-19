import numpy as np

EMPTY  = 0
RED    = 1
YELLOW = 2

class ConnectFourGame:
    def __init__(self, render_mode: str='silent'):
        self.board = np.zeros((6,7), dtype=int)
        self.turn = None

        self.render_mode = render_mode

    def reset(self, first_player=None):
        '''Place piece on board if possible, returns board state, turn and
        (for consistency) winner

        If invalid move is made (either invalid column or the column is full),
        then no change to the board is made and the turn will not change
        '''
        if first_player is None:
            self.turn = np.random.choice([RED, YELLOW])
        else:
            assert first_player in (RED, YELLOW), 'Invalid player selection on reset'
            self.turn = first_player

        self.board[:, :] = 0

        winner = EMPTY

        self.render()

        return self.board.copy(), self.turn, winner

    def place_piece(self, player: int, column: int):
        '''Place piece on board if possible, returns board state, turn, and winner

        If invalid move is made (incorrect player's turn or the column is full),
        then no change to the board is made and the turn will not change
        '''
        assert player in (RED, YELLOW), \
                f'Invalid player, must be {RED}(RED) or {YELLOW}(YELLOW).'
        assert 0 <= column < 7, f'Invalid column, must be in range 0 to 6'

        # check that move is allowed
        correct_turn = player == self.turn
        nonfull_column = self.board[5, column] == 0
        if correct_turn and nonfull_column:
            # find first empty row to place new piece
            empty_row = np.where(self.board[:, column] == 0)[0][0]
            self.board[empty_row, column] = self.turn

            # swap turns
            self.turn = RED if self.turn == YELLOW else YELLOW

        # check for winner
        winner = self.check_winner()

        # render board
        self.render()

        return self.board.copy(), self.turn, winner

    def check_winner(self):
        # slow solution from
        # https://stackoverflow.com/questions/27996106/python-connect-4-check-for-winners-processing-2
        nrows, ncols = self.board.shape

        def fours(arr):
            return len(arr) == 4 and ( (arr == RED).all() or (arr == YELLOW).all() )

        # check horizontals
        for row in self.board:
            for i in range(ncols-4):
                if fours(row[i:i+4]):
                    return row[i]

        # check verticals
        for i in range(ncols):
            for j in range(nrows-4):
                if fours(self.board[j:j+4,i]):
                    return self.board[j][i]

        # check NW -> SE diagonals
        for i in range(ncols-4):
            for j in range(nrows-4):
                if fours(self.board[range(j,j+4),range(i,i+4)]):
                    return self.board[j,i]

        # check NE -> SW diagonals
        for i in range(3, ncols):
            for j in range(nrows-4):
                if fours(self.board[range(j,j+4),range(i,i-4,-1)]):
                    return self.board[j,i]

        return EMPTY

    def get_random_valid_move(self):
        '''get random valid move for current turn'''
        nonfull_columns = [i for i in range(7) if self.board[5,i] == 0]

        return np.random.choice(nonfull_columns)

    def render(self):
        if self.render_mode == 'text':
            self._render_text()

    def _render_text(self):
        def get_token(piece: int):
            return {EMPTY: '   ', RED : ' R ', YELLOW : ' Y '}[piece]

        text = ''
        text += ' '.join([f' {i} ' for i in range(7)]) + '\n'
        text += '-'.join(7*['---']) + '\n'
        for row in self.board[::-1]:
            text += '|'.join(map(get_token, row)) + '\n'
            text += '-'.join(7*['---']) + '\n'

        text += f"TURN = {self.turn}({'RED' if self.turn==RED else 'YELLOW'})"

        print('\n' + text + '\n')

def play_against_random():
    # play as yellow agent
    me = YELLOW
    opp = RED

    game = ConnectFourGame(render_mode='text')

    board, turn, winner = game.reset()

    while winner == EMPTY:
        if turn == me:
            # query move
            try:
                column =  int(input('Enter your column: '))
            except:
                print('[ERROR] invalid column entered, must enter integers from 0 to 6')
                exit()

            board, turn, winner = game.place_piece(me, column)

        else:
            # choose random action for opponent
            column = game.get_random_valid_move()
            board, turn, winner = game.place_piece(opp, column)

    if winner == me:
        print('YOU WIN!')
    else:
        print('YOU LOSE!')

3
if __name__ == "__main__":
    play_against_random()