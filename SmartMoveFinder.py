def findBestMove(validMoves, game, value = 0):
    maxScore = -100
    bestMove = None
    if game.first_move != True:
        for playermove2 in validMoves:
            if playermove2.get_val()==game.get_type():
                playermove2.set_val(8)
                score = score_board(game)
                if score > maxScore:
                    maxScore = score
                    bestMove = playermove2
                playermove2.set_val(playermove2.get_undo_val())
    else:
        for playermove in validMoves:
            playermove.set_val(8)
            score = score_board(game)
            if score > maxScore:
                maxScore = score
                bestMove = playermove
            playermove.set_val(playermove.get_undo_val())
    return bestMove



def score_board(game):
    try:
        gs = game.findLargestGroup()
    except(TypeError):
        return 0
    score = gs["white"] - gs["black"]
    return score