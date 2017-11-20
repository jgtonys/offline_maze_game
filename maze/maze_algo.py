from random import shuffle, randrange
def make_maze(w = 24,h = 12):
    vis = [[0]*w+[1] for _ in range(h)] + [[1]*(w+1)]
    ver = [["|  "]*w+['|'] for _ in range(h)] + [[]]
    hor = [["+--"]*w+['+'] for _ in range(h+1)]


    def walk(x,y):
        vis[y][x] = 1

        d = [(x-1,y),(x,y+1),(x+1,y),(x,y-1)]
        shuffle(d)
        for (xx,yy) in d:
            if vis[yy][xx]:continue
            if xx == x: hor[max(y,yy)][x] = "+  "
            if yy == y: ver[y][max(x,xx)] = "   "
            walk(xx,yy)

    M = [[0]*w+[1] for _ in range(h)] + [[1]*(w+1)]
    walk(randrange(w),randrange(h))
    parse,maze = [],[]
    ver[h-1][w-1] = "  E"
    for (a,b) in zip(hor,ver):
        parse.append(''.join(a + ['\n'] + b))
    for i in range(len(parse)):
        tmp = parse[i].split("\n")
        maze += tmp
    for i in range(30):
        t1,t2 = randrange(len(maze)-1),randrange(len(maze[0])-1)
        if maze[t1][t2].find(" ")!=-1:
            maze[t1] = maze[t1][:t2] + "C" + maze[t1][t2+1:]
    return maze
