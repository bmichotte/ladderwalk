stars_per_rank = {
        25:2,
        24:2,
        23:2,
        22:2,
        21:2,
        20:3,
        19:3,
        18:3,
        17:3,
        16:3,
        15:4,
        14:4,
        13:4,
        12:4,
        11:4,
        10:5,
        9:5,
        8:5,
        7:5,
        6:5,
        5:5,
        4:5,
        3:5,
        2:5,
        1:5}

stars_at_rank = {}
s = 0
for rank in range(25,-1,-1):
    stars_at_rank[rank] = s
    if rank > 0:
        s += stars_per_rank[rank]

def rank_from_stars(stars):
    s = 0
    for rank in range(25,0,-1):
        if stars <= s + stars_per_rank[rank]:
            return rank
        s += stars_per_rank[rank]
    return 0

if __name__ == "__main__":
    print rank_from_stars(10)
