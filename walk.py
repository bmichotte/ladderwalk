import random
import ranks

def step(stars, pwin, lastres):
    rank = ranks.rank_from_stars(stars)
    if random.random() < pwin: #won the game
        if lastres>=2 and rank > 5: #win streak stars
            return stars+2, lastres+1
        else:
            return stars+1, lastres+1
    else: # lost the game
        # We can lose stars at rank 20 and better
        if stars > ranks.stars_at_rank[20]:
            return stars-1, 0
        else: # can't otherwise
            return stars, 0

    

