#maze solver for https://github.com/noops-challenge/mazebot
#this is going to solve mazes given from this challenge
#their api must be used

#map items
# ' ' = space is a place to walk
# 'X' = wall
# 'A' 'B' = start and stop

#getting maze from online
import urllib.request
import json
import queue


def data_processing(data):
    #print(data)
    x_map_size = 0
    y_map_size = 0
    mid_pos = 0 #this is the position of the x ie 40x40
    start_pos = [0,0]
    end_pos = [0,0]
    #getting map map size contained in name of map
    mid_pos = int(data["name"].index("x"))
    x_map_size = int(data["name"][mid_pos-2:mid_pos])
    y_map_size = int(data["name"][mid_pos+1:mid_pos+3])
    #get start and end pos
    start_pos[0] = data["startingPosition"][0]
    start_pos[1] = data["startingPosition"][1]
    end_pos[0] = data["endingPosition"][0]
    end_pos[1] = data["endingPosition"][1]
    return x_map_size, y_map_size, start_pos, end_pos

def create_map(data, x_map_size, y_map_size):
    a = 0
    b = 0
    #print(x_map_size, y_map_size)
    #print(data)
    map = [[0 for x in range(int(x_map_size))] for y in range(int(y_map_size))]
    for x in range(x_map_size):
        for y in range(y_map_size):
            map[x][y] = data["map"][x][y]
    #print(map)
    return map


def solve_maze(map,start_pos,end_pos,ppath): #start the bfs
    for x in map:
        print(x)
    print("")
    #x_pos[y corrdinate][x corrdinate]
    #bc of 2d array format ^ is true
    #que holds all the nodes that are going to visited
    q = queue.Queue()
    #put the first item in the que
    q.put(start_pos)
    #startt the maze solve with the first pos making this a v
    #marking as visited will just change to v
    map[start_pos[1]][start_pos[0]] = "v"
    #while we have not found the solution
    while(q.empty() == False):
        #recent in the node first in the que to be visited
        recent = q.queue[0]
        #if we have found the end print
        if(map[recent[1]][recent[0]] == 'B'):
            print('found it')
            return True
        #pop that recent item
        q.get(recent)
        #this is to get the x and y cord to find neighbors
        ycord = recent[0]
        xcord = recent[1]
        #get all the neighbors
        neighbors =  [[ycord+1,xcord], #above
                      [ycord-1,xcord], #below
                      [ycord,xcord+1], #right
                      [ycord,xcord-1],] #leftde
        #for in all the nieghbors find if it is the end
        for x in neighbors:
            try:
                if(map[x[1]][x[0]] == 'B'):
                    ppath[x[1],x[0]] = (recent[1],recent[0])
                    print("found it")
                    return True
                if(map[x[1]][x[0]] != 'v' and map[x[1]][x[0]] != 'X'): #this is to see if it has been previously been visited
                    #if it has not been visited put it into the queue
                    q.put(x)
                    #mark it as visited
                    map[x[1]][x[0]] = 'v'
                    ppath[x[1],x[0]] = (recent[1],recent[0])
            except IndexError:
                pass
        return map, ppath

    #we now have solved the maze and want to print the final product


def main():
    x_map_size = 0
    y_map_size = 0
    start_pos = [0,0]
    end_pos = [0,0]
    map = []
    #PARENT DICT
    ppath = {}
    #get the json data from the site
    with urllib.request.urlopen('https://api.noopschallenge.com/mazebot/random?minSize=10&maxSize=15') as url:
        data = json.loads(url.read().decode())
    #process the raw data and get variables below
    x_map_size, y_map_size, start_pos, end_pos = data_processing(data)
    #create the map just a 2D array of points
    map = create_map(data,x_map_size,y_map_size)
    #map is currently made up of 'X',' ','A','B', could move and make spaces into v for visited
    #make the map
    map,ppath = solve_maze(map,start_pos,end_pos,ppath)
    '''
    for x in map:
        print(x)
    while(True):
        try:
            print(ppath[end_pos[1],end_pos[0]])
        except SyntaxError:
            pass
            '''




if __name__ == "__main__":
    main()
