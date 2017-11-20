import maze,DBcon

def start_maze(user):
    rtlist = maze.start_maze(user)
    update_after_maze(user.username,user.level,rtlist[1],rtlist[0])

def update_after_maze(username,level,coin,elapsed_time):
    DBcon.db_update(username,level,coin,elapsed_time)
