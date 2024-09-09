def findBestMove(validMoves, game):
    maxScore = -100
    bestMove = None
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