import ranks
import walk
import math

import os
import argparse
import time
import sqlite3

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--target', type = int, required=True, help="Target rank (0 = Legend)")
parser.add_argument('-p', type = float, required=True, help="Win probability (0.0 - 1.0)")
parser.add_argument('-o', type=str, default="grid.db", help="Output db file")
parser.add_argument('--maxtime', type=float, default=5.0, help="Maximum run time (in minutes)")
parser.add_argument('--threshold', type=float, default=0.5, help="Convergence criterion (error of the mean, in games)")
parser.add_argument('--maxsteps', type=int, default = 1500, help="Maximum steps before cutting off a walk (Higher values yield better means)")
args = parser.parse_args()

target_rank = args.target
threshold = args.threshold
winp = args.p
nstars = ranks.stars_at_rank[0]
target = ranks.stars_at_rank[target_rank]
data = {}
max_steps = args.maxsteps
time_cutoff = args.maxtime

for star in range(nstars+1):
    data[star] = {}
    for bonus in range(3):
        data[star][bonus] = []


def do_walk(start, end, winp, streak=0):
    start_stars = start
    stars = start_stars
    last = streak

    run = []
    run.append((start_stars, streak))
    nsteps = 0
    terminated = False
    while True:
        if stars >= end:
            break
        stars, last = walk.step(stars, winp, last if last is not None else 0)

        run.append((stars, last))

        nsteps += 1
        if nsteps > max_steps:
            terminated = True
            break

    return run, terminated

def proc_run(run,terminated):
    for i in range(len(run)-1):
        run_slice = run[i:]
        stars, bonus = run_slice[0]
        bonus = min(bonus,2)
        if terminated:
            data[stars][bonus].append(max_steps+1)
        else:
            data[stars][bonus].append(len(run_slice)-1)

    # edge case of being above rank
    if len(run) == 1:
        stars, bonus = run[0]
        bonus = min(bonus,2)
        data[stars][bonus].append(0)

def mean(arr):
    s = 0.0
    for i in range(len(arr)):
        s += arr[i]
    return s/len(arr)

def semf(arr):
    m = mean(arr)
    s = 0.0
    for i in range(len(arr)):
        s += (arr[i] - m)**2
    s /= len(arr)-1
    return math.sqrt(s)/math.sqrt(len(arr))

def print_chart(maxsem):
    #os.system('clear')
    os.system('date')
    print "Win p: %.2f  Target: %d" % (winp, target_rank)
    print 
    for star in range(60):
        data_s = [data[star][bonus] for bonus in range(3)]
        lens = map(len, data_s)
        means = map(mean, data_s)
        sems = map(semf, data_s)
        fstr = [star] + sems + means + lens
        print "%2d | %4.1f  %4.1f  %4.1f | %5d %5d %5d | %8d %8d %8d" % tuple(fstr)
    print
    print "Max error: %f" % maxsem
    print


# Burn in
for burn in range(30):
    for star_i in range(nstars+1):
        for bonus_i in range(3):
            run, terminated = do_walk(star_i, target, winp, bonus_i)
            proc_run(run,terminated)
# Replace later with threshhold
max_err = 1e300
iterations = 0

start_time = time.time()
while max_err > threshold:
    max_err = -1
    smax, bmax = None,None
    for star in range(nstars+1):
        for bonus in range(3):
            sem = semf(data[star][bonus])
            if sem > max_err:
                max_err = sem
                smax = star
                bmax = bonus
    run, terminated = do_walk(smax, target, winp, bmax)
    proc_run(run, terminated)
    if iterations % 500 == 0:
        print_chart(max_err)
        if time.time() - start_time > 60*time_cutoff: 
            break

    iterations += 1

print_chart(max_err)

# data output
con = sqlite3.connect(args.o)
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS grid(target_rank INT, winp REAL, stars INT, bonus INT, games REAL, sem REAL)")

for star in range(nstars+1):
    for bonus in range(3):
        cur.execute("INSERT INTO grid VALUES(?, ?, ?, ?, ?, ?)", (target_rank, winp, star, bonus, mean(data[star][bonus]), semf(data[star][bonus])))

con.commit()
con.close()





