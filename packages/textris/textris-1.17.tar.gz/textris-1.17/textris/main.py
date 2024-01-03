##textris_

import curses
import keyboard
import random
import time

#python textris_.py
#Adjust time when paused
#Add Textris.starting_pos
#Add srs rotation
#Add actual score system
#Color shadow?
#Add way to quit
#Add sound to death animation
#Add rotation sound
#Make stuff go faster as time goes on
#Display FPS
#Add grid clear sound
#Make mapping part of Textris

stdscr=curses.initscr()
curses.start_color()
curses.use_default_colors()

mapping={key: item for key,item in zip("tseELlb",[chr(i+2000) for i in range(7)])}
curses_colors=[mapping[key] for key in mapping.keys()]

colors=[curses.COLOR_CYAN,curses.COLOR_BLUE,curses.COLOR_RED,
        curses.COLOR_YELLOW,curses.COLOR_MAGENTA,curses.COLOR_GREEN]

True_colors=[(160,0,240),(240,240,0),(0,240,0),
             (240,0,0),(240,160,0),(0,110,255)]

True_colors=[tuple([int(min((i/255)*1000,1000)) for i in color]) for color in True_colors]

for i,color,c in zip(range(1,8),colors,True_colors):
    curses.init_color(color,*c)
    curses.init_pair(i,color,curses.COLOR_BLACK)

curses.init_color(curses.COLOR_BLACK,*(int(10/255*1000),)*3)
curses.init_color(curses.COLOR_WHITE,*(int(255/255*1000),)*3)

paused=False

def print(text):

    stdscr.clear()

    for y,line in enumerate(str(text).split("\n")):

        for x,char in enumerate(line):

            if char in curses_colors and char!=mapping["b"]:
                stdscr.addstr(y,x,"#",curses.color_pair(curses_colors.index(char)+1))

            elif char==mapping["b"]:

                stdscr.addstr(y,x,"#",curses.color_pair(6))

            else:
                stdscr.addstr(char)

        stdscr.addstr("\n")

    stdscr.refresh()

class Textris:

    width=10
    height=20

    grid=[]

    pos=[4,0]

    for y in range(height):
        grid.append([])
        for x in range(width):
            grid[-1].append(0)

    t=[[(1,0),(0,1),(1,1),(2,1)],
       [(1,0),(1,1),(2,1),(1,2)],
       [(0,1),(1,1),(2,1),(1,2)],
       [(1,0),(0,1),(1,1),(1,2)]]

    b=[[(0,1),(1,1),(2,1),(3,1)],
       [(2,0),(2,1),(2,2),(2,3)],
       [(0,2),(1,2),(2,2),(3,2)],
       [(1,0),(1,1),(1,2),(1,3)]]

    s=[[(0,0),(1,0),(1,1),(0,1)] for i in range(4)]

    e=[[(1,0),(2,0),(0,1),(1,1)],
       [(1,0),(1,1),(2,1),(2,2)],
       [(1,1),(2,1),(0,2),(1,2)],
       [(0,0),(0,1),(1,1),(1,2)]]

    E=[[(0,0),(1,0),(1,1),(2,1)],
       [(2,0),(1,1),(2,1),(1,2)],
       [(0,1),(1,1),(1,2),(2,2)],
       [(1,0),(0,1),(1,1),(0,2)]]

    l=[[(0,0),(0,1),(1,1),(2,1)],
       [(1,0),(2,0),(1,1),(1,2)],
       [(0,1),(1,1),(2,1),(2,2)],
       [(1,0),(1,1),(0,2),(1,2)]]

    L=[[(2,0),(0,1),(1,1),(2,1)],
       [(1,0),(1,1),(1,2),(2,2)],
       [(0,1),(1,1),(2,1),(0,2)],
       [(0,0),(1,0),(1,1),(1,2)]]

    pieces={mapping["t"]: t,mapping["e"]: e,mapping["E"]: E,mapping["l"]: l,mapping["L"]: L,mapping["s"]: s,mapping["b"]: b}
    angle=0
    current=random.choice(list(pieces.keys()))
    held_piece=None
    base_pos=None

    gravity=0.5
    went_down=0
    rotation_down=0.2

    input_delay=0.05
    wait_from_input_start=input_delay*2
    input_start=0
    last_input=0

    lines=0
    has_swapped=False

    next_pieces=[]
    for i in range(5):
        next_pieces.append(random.choice(list(pieces.keys())))

    presses={key: [None,None] for key in ("up","enter","r","space","shift")}

    shadow=None
    is_alive=True

    click=lambda key: Textris.presses[key][-1] and not Textris.presses[key][-2]
    release=lambda key: Textris.presses[key][-2] and not Textris.presses[key][-1]

    def init():

        Textris.base_wall_kick_data=(((0,0),(-1,0),(-1,1),(0,-2),(-1,-2)),
                                     ((0,0),(1,0),(1,-1),(0,2),(1,2)),
                                     ((0,0),(1,0),(1,1),(0,-2),(1,-2)),
                                     ((0,0),(-1,0),(-1,-1),(0,2),(-1,2)))

        Textris.bar_wall_kick_data=(((0,0),(-2,0),(1,0),(-2,-1),(1,2)),
                                    ((0,0),(-1,0),(2,0),(-1,2),(2,-1)),
                                    ((0,0),(2,0),(-1,0),(2,1),(-1,-2)),
                                    ((0,0),(1,0),(-2,0),(1,-2),(-2,1)))

        Textris.wall_kick_data={key: Textris.base_wall_kick_data for key in Textris.pieces.keys() if key!=mapping["b"]}
        Textris.wall_kick_data[mapping["b"]]=Textris.bar_wall_kick_data

    def presses_update():

        for key in Textris.presses.keys():
            Textris.presses[key][-2]=Textris.presses[key][-1]
            Textris.presses[key][-1]=keyboard.is_pressed(key)

    def check_for_clears():

        clears=0

        for y,line in enumerate(Textris.grid):
            if 0 not in line:

                Textris.lines+=1
                clears+=1
                Textris.grid[y]=[0 for i in range(Textris.width)]

                for Y in range(y,1,-1):
                    Textris.grid[Y],Textris.grid[Y-1]=Textris.grid[Y-1],Textris.grid[Y]

    def renew():

        current_pos=[(x+Textris.pos[0],y+Textris.pos[1]) for x,y in Textris.pieces[Textris.current][Textris.angle]]
        for x,y in current_pos:
            Textris.grid[y][x]=Textris.current

        Textris.current=Textris.next_pieces.pop(0)
        Textris.next_pieces.append(random.choice(list(Textris.pieces.keys())))
        Textris.angle=0
        Textris.pos=[4,0]

        Textris.check_for_clears()

        current_pos=[(x+Textris.pos[0],y+Textris.pos[1]) for x,y in Textris.pieces[Textris.current][Textris.angle]]
        if not all([0<=x<Textris.width and 0<=y<Textris.height and not Textris.grid[y][x] for x,y in current_pos]):
            Textris.is_alive=False

        Textris.has_swapped=False

    def restart():

        Textris.grid=[]

        for y in range(Textris.height):
            Textris.grid.append([])
            for x in range(Textris.width):
                Textris.grid[-1].append(0)

        Textris.held_piece=()
        Textris.went_down=0
        Textris.last_input=0

        Textris.lines=0
        Textris.is_alive=True

        Textris.current=random.choice(list(Textris.pieces.keys()))
        Textris.angle=0
        Textris.pos=[4,0]
        Textris.has_swapped=False

        Textris.next_pieces=[]
        for i in range(5):
            Textris.next_pieces.append(random.choice(list(Textris.pieces.keys())))

    def try_to_rotate():

        #Textris.went_down=time.perf_counter()-Textris.rotation_down

        offsets=Textris.wall_kick_data[Textris.current][Textris.angle]

        ex_angle=Textris.angle
        Textris.angle+=1
        Textris.angle%=4

        for x_offset,y_offset in offsets:

            Textris.pos[0]+=x_offset
            Textris.pos[1]+=y_offset

            current_pos=[(x+Textris.pos[0],y+Textris.pos[1]) for x,y in Textris.pieces[Textris.current][Textris.angle]]

            if all([0<=x<Textris.width and 0<=y<Textris.height and not Textris.grid[y][x] for x,y in current_pos]):
                return(None)
            else:
                Textris.pos[0]-=x_offset
                Textris.pos[1]-=y_offset

        Textris.angle=ex_angle

    def try_to_go(x,y,is_True=True):

        has_went=0

        Textris.pos[1]+=y
        current_pos=[(x+Textris.pos[0],y+Textris.pos[1]) for x,y in Textris.pieces[Textris.current][Textris.angle]]

        if any([not(0<=x<Textris.width and 0<=y<Textris.height and not Textris.grid[y][x]) for x,y in current_pos]):
            Textris.pos[1]-=y
            has_went+=1

        Textris.pos[0]+=x
        current_pos=[(x+Textris.pos[0],y+Textris.pos[1]) for x,y in Textris.pieces[Textris.current][Textris.angle]]

        if any([not(0<=x<Textris.width and 0<=y<Textris.height and not Textris.grid[y][x]) for x,y in current_pos]):
            Textris.pos[0]-=x
            has_went+=1

        return(not(has_went))

    def try_to_swap():

        if Textris.has_swapped:
            return(None)

        Textris.current,Textris.held_piece=Textris.held_piece,Textris.current

        if not Textris.current:
            Textris.current=Textris.next_pieces.pop(0)
            Textris.next_pieces.append(random.choice(list(Textris.pieces.keys())))

        Textris.pos=[4,0]
        Textris.angle=0

        Textris.has_swapped=True

    def update_grid():

        if Textris.click("shift"):
            Textris.try_to_swap()

        if Textris.click("up"):
            Textris.try_to_rotate()

        if Textris.click("space"):

            while Textris.try_to_go(0,1,is_True=False):
                pass

            Textris.went_down=float("-inf")

        if time.perf_counter()-Textris.went_down>=Textris.gravity:
            Textris.pos[1]+=1
            Textris.went_down=time.perf_counter()

        if time.perf_counter()-Textris.last_input>=Textris.input_delay:

            direction=[(keyboard.is_pressed("d") or keyboard.is_pressed("right")),0]
            direction[0]-=(keyboard.is_pressed("q") or keyboard.is_pressed("left"))
            direction[1]=(keyboard.is_pressed("s") or keyboard.is_pressed("down"))

            if sum(direction):
                if not Textris.input_start:
                    Textris.input_start=time.perf_counter()
                    Textris.try_to_go(*direction)
                    Textris.last_input=time.perf_counter()
            else:
                Textris.input_start=0

            if time.perf_counter()-Textris.input_start>=Textris.wait_from_input_start or not direction[0] and direction[1]:
                Textris.try_to_go(*direction)
                Textris.last_input=time.perf_counter()

        current_pos=[(x+Textris.pos[0],y+Textris.pos[1]) for x,y in Textris.pieces[Textris.current][Textris.angle]]

        if any([not(0<=x<Textris.width and 0<=y<Textris.height and not Textris.grid[y][x]) for x,y in current_pos]):
            Textris.pos[1]-=1
            Textris.renew()

    def get_shadow(display_current=True):

        pos=Textris.pos.copy()
        grid=[i.copy() for i in Textris.grid]

        while Textris.try_to_go(0,1,is_True=False):
            pass

        shadow=[i.copy() for i in Textris.grid]

        for y,line in enumerate(shadow):
            for x,block in enumerate(line):
                shadow[y][x]=("." if not block else block)

        if not display_current:
            return(shadow)

        for x,y in [(Textris.pos[0]+X,Textris.pos[1]+Y) for X,Y in Textris.pieces[Textris.current][Textris.angle]]:
            shadow[y][x]="O"

        Textris.grid=[i.copy() for i in grid]
        Textris.pos=pos.copy()

        for x,y in [(Textris.pos[0]+X,Textris.pos[1]+Y) for X,Y in Textris.pieces[Textris.current][Textris.angle]]:
            shadow[y][x]=Textris.current

        return(shadow)

    def get_grid_string(paused=False):

        text=[" ".join(line) for line in Textris.get_shadow()]
        text=text+[" "*len(text[-1]) for i in range(64)]

        to_hold=()
        if Textris.held_piece:
            to_hold=Textris.pieces[Textris.held_piece][0]

        htext=[[Textris.held_piece if (x,y) in to_hold else "." for x in range(4)] for y in range(4)]
        htext.insert(0,["." for i in range(4)])
        htext.append(["." for i in range(4)])

        for i in range(len(htext)):
            htext[i].insert(0,".")

        htext=[" ".join(line) for line in htext]
        text=["            "+i for i in text]

        for i in range(4):
            text[i]=list(text[i])
            text[i][:len(htext[i])+1]=f" {htext[i]}"
            text[i]="".join(text[i])

        for index,piece in enumerate(Textris.next_pieces):

            piece=[[piece if (x,y) in Textris.pieces[piece][0] else "." for x in range(4)] for y in range(2)]
            piece.insert(0,["." for i in range(4)])
            piece.append(["." for i in range(4)])

            for i in range(len(piece)):
                piece[i].insert(0,".")

            piece=[" ".join(i) for i in piece]

            for i,line in enumerate(piece[:-1]):
                text[i+index*3]+="   "+line

        text[i+index*3+1]+="   "+piece[0]
        text[i+index*3+3]+=f"   Lines: {Textris.lines}."
        text[i+index*3+4]+=f"   {['||','>'][paused]}"

        for i,line in enumerate(text[::-1]):
            if line.count(" ")==len(line):
                text[len(text)-i-1]=None
            else:
                break

        text=[line for line in text if line is not None]
        text="\n"*0+"\n".join(text)

        return(text)

    def get_grid_string_no_current():
        return("            "+"\n            ".join([" ".join(line) for line in Textris.get_shadow(display_current=False)]))

def func():

    stdscr=curses.initscr()
    curses.start_color()
    curses.use_default_colors()

    mapping={key: item for key,item in zip("tseELlb",[chr(i+2000) for i in range(7)])}
    curses_colors=[mapping[key] for key in mapping.keys()]

    colors=[curses.COLOR_CYAN,curses.COLOR_BLUE,curses.COLOR_RED,
            curses.COLOR_YELLOW,curses.COLOR_MAGENTA,curses.COLOR_GREEN]

    True_colors=[(160,0,240),(240,240,0),(0,240,0),
                 (240,0,0),(240,160,0),(0,110,255)]

    True_colors=[tuple([int(min((i/255)*1000,1000)) for i in color]) for color in True_colors]

    for i,color,c in zip(range(1,8),colors,True_colors):
        curses.init_color(color,*c)
        curses.init_pair(i,color,curses.COLOR_BLACK)

    curses.init_color(curses.COLOR_BLACK,*(int(10/255*1000),)*3)
    curses.init_color(curses.COLOR_WHITE,*(int(255/255*1000),)*3)

    paused=False

    Textris.init()
    #audio.play_music()

    while not keyboard.is_pressed("ctrl+alt+shift+esc"):

        Textris.presses_update()

        if Textris.click("r"):
            Textris.grid=[[0 for i in range(Textris.width)] for i in range(Textris.height)]

        if Textris.click("enter"):
            paused=not(paused)
        if paused:
            print(Textris.get_grid_string(paused=True))
            continue

        Textris.update_grid()
        print(Textris.get_grid_string())

        if not Textris.is_alive:

            time.sleep(0.4)

            for y in range(Textris.height):

                frame_start=time.perf_counter()

                Textris.grid[y]=[0 for i in range(Textris.width)]
                print(Textris.get_grid_string_no_current())

                while time.perf_counter()-frame_start<1/20:
                    pass

            Textris.restart()