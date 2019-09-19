#maze solver for https://github.com/noops-challenge/mazebot
#this is going to solve mazes given from this challenge
#their api must be used



#~~~~~~~~~~~~~NOTES~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`
# Dealing with the problem of the end-pos x and y are flipped at some point and dont know why

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`

#map items
# ' ' = space is a place to walk
# 'X' = wall
# 'A' 'B' = start and stop

#getting maze from online
import urllib.request
import urllib.parse
import json
import queue
import requests

def data_processing(data):
    #print(data)
    post_url = data['mazePath']
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
    return x_map_size, y_map_size, start_pos, end_pos, post_url

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
    #Useful Info
    #print(list(q.queue)) = prints the queue
    #q.get = removes front of Queue
    #q.put = puts at back of queue
    #for x in map:
    #    print(x)
    #print("")
    #x_pos[y corrdinate][x corrdinate]
    #bc of 2d array format ^ is true
    #que holds all the nodes that are going to visited
    q = queue.Queue()
    #put the first item in the que
    q.put(start_pos)
    #print("Starting position is = ",end="")
    #print(start_pos)

    #THIS MIGHT BE BAD
    ppath[start_pos[0],start_pos[1]] = (-1,-1)
    #THIS MIGHT BE BAD

    #startt the maze solve with the first pos making this a v
    #marking as visited will just change to
    #print("start pos = ")
    #print(start_pos[0],start_pos[1])
    map[start_pos[1]][start_pos[0]] = "v"
    #while we have not found the solution
    while(q.empty() == False):
        '''
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        for x in map:
            print(x)
        print("")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        '''
        #recent in the node first in the que to be visited
        #print(list(q.queue))
        recent = q.queue[0]
        #print("Recent is = ",end="")
        #print(recent)
        #if we have found the end print
        '''
        if(map[recent[1]][recent[0]] == 'B'):
            print("dont want this to happen")
            print('found it')
            return True
        '''
        #pop that recent item

        q.get(recent)
        #print("recent is the most recent point = ",end="")
        #print(recent)
        #this is to get the x and y cord to find neighbors
        xcord = recent[0]
        ycord = recent[1]

        '''
        print("x cord of recent = ",end="")
        print(xcord)
        print("y cord of recent = ",end="")
        print(ycord)
        '''
        #get all the neighbors

        neighbors =  [[xcord+1,ycord], #right
                      [xcord-1,ycord], #left
                      [xcord,ycord+1], #above
                      [xcord,ycord-1],] #below
        #for in all the nieghbors find if it is the end
        for x in neighbors:
            try:
                if(map[x[1]][x[0]] == 'B' and x[0] >= 0 and x[1] >= 0):
                    ppath[x[0],x[1]] = (recent[0],recent[1])
                    #print("found it at ",end = "")
                    #print((x[0],x[1]))
                    return map,ppath
                if(map[x[1]][x[0]] != 'v' and map[x[1]][x[0]] != 'X' and x[0] >= 0 and x[1] >= 0): #this is to see if it has been previously been visited or unable
                    #if it has not been visited put it into the queue
                    q.put(x)
                    #mark it as visited
                    map[x[1]][x[0]] = 'v'
                    ppath[x[0],x[1]] = (recent[0],recent[1])
            except IndexError:
                pass
        #print("--------------------------------")
        #for x in map:
        #    print(x)
    return map, ppath


    #we now have solved the maze and want to print the final product
def direction_solver(map,start_pos,end_pos,ppath):
    #print("OUT OF MAZE SOLVER")
    #print("value of end pos = ",end="")
    #print(end_pos)
    map[start_pos[0]][start_pos[1]] = "A"
    #for x in map:
    #    print(x)

    new1 = end_pos
    #print("start pos",start_pos)
    #print("end_pos",end_pos)
    '''
    print("Parent of end pos ",end = "")
    print(ppath[end_pos[0],end_pos[1]])
    end1=ppath[end_pos[0],end_pos[1]]
    print("The parent of that parent", end = "")
    print(ppath[end1[0],end1[1]])
    ''
    print("THIS IS A TEST   ",end="")
    print(ppath[3,7])
    '''
    #temp1 = ppath[temp1[0],temp1[1]]
    direction = ""
    while(new1[0] != start_pos[0] or new1[1] != start_pos[1]):
        #print("The parent of the new node is ",end = "")
        #print(ppath[new1[0],new1[1]],end="")
        recent = new1
        new1 = ppath[new1[0],new1[1]]
        if(new1[0]>recent[0]):
            #print(temp1,recent)
            #print("from "+ str(recent)+" to "+str(new1))
            #print("E",end = '')
            direction = direction + "W"
        if(new1[0]<recent[0]):
            #print(temp1,recent)
            #print("from "+ str(recent)+" to "+str(new1))
            #print("W",end = '')
            direction = direction + "E"
        if(new1[1]>recent[1]):
            #print(temp1,recent)
            #print("from "+ str(recent)+" to "+str(new1))
            #print("S",end = '')
            direction = direction + "N"
        if(new1[1]<recent[1]):
            #print(temp1,recent)
            #print("from "+ str(recent)+" to "+str(new1))
            #print("N",end = '')
            direction = direction + "S"
    return direction


def main():
    x_map_size = 0
    y_map_size = 0
    start_pos = [0,0]
    end_pos = [0,0]
    map = []

    #PARENT DICT
    #problem max size is around 100
    theurl = 'https://api.noopschallenge.com/mazebot/random?minSize=10&maxSize=20'
    ppath = {}
    #get the json data from the site
    data = requests.get(theurl).json()
    '''
    with urllib.request.urlopen(theurl) as url:
        data = json.loads(url.read().decode())
    '''
    #process the raw data and get variables below
    #
    x_map_size, y_map_size, start_pos, end_pos, post_url = data_processing(data)
    #print("start_pos")
    #print(start_pos)
    #
    #create the map just a 2D array of points


    #so with map indeces map[position on vertical][position on horizontal]
    #                    map[what row][what column]
    #                    map[how many down][how many sideways]
    #                    map[y][x]
    #
    map = create_map(data,x_map_size,y_map_size)

    #
    #map is currently made up of 'X',' ','A','B', could move and make spaces into v for visited
    #make the map

    map,ppath = solve_maze(map,start_pos,end_pos,ppath)

    directions = direction_solver(map,start_pos,end_pos,ppath)

    reverse_directions = ""
    #print("Directions = "+directions)
    for x in directions:
        reverse_directions = x + reverse_directions

    base_url = 'https://api.noopschallenge.com'
    post_url = base_url+post_url


    p = requests.post(post_url, json={"directions":reverse_directions})
    print(p.status_code)
    print(p.json)
    print(p.text)

    

if __name__ == "__main__":
    main()
