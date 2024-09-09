def score_board(game):
    gs = game.findLargestGroup()
    score = gs["black"] - gs["white"]
    return score