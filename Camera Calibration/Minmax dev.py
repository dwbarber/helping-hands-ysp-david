def minmax(color, layout):
    previous_evaluation = evaluate(1, layout)[0]  # all values from evaluations (yellow)
    my_evaluation_y = evaluate(1, layout)[1]  # y positions of the values from evaluation
    hypo_board = board.copy()  # makes a copy of the board array
    new_evaluation = np.zeros(7)
    print(my_evaluation_y)
    if color == 1:  # checks if it is yellows hypo turn
        for i in range(7):
            hypo_board[my_evaluation_y[i]][i] = 1
            if i >= 1:
                hypo_board[my_evaluation_y[i-1]][i-1] = 0
                hypoboards = np.zeros(7,6,7)
                hypoboards[]
    elif color == -1:
        for i in range(7):
            hypo_board[my_evaluation_y[i]][i] = 1
            if i >= 1:
                hypo_board[my_evaluation_y[i-1]][i-1] = 0
            best_yel = max(evaluate(-1, hypo_board)[0])
            compiled_maxes = np.zeros(7)  # compiles the maximum for each version of the board
            # that occurs as a result of placing the piece there
            compiled_maxes[i] = best_yel
            # adds the largest value from all of the the new boards to the old value for that position
            new_evaluation[i] = previous_evaluation[i] + max(compiled_maxes)
    return new_evaluation
