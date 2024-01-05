##textris_

import curses
import keyboard
import random
import time
import art

#python textris_.py
#Adjust time when paused
#Add Textris.starting_pos
#Add srs rotation
#Add better score system
#Add sound to death animation
#Add rotation sound
#Display FPS
#Add grid clear sound
#Make mapping part of Textris
#Add title screen music and sound
#Add controller support
#Add way to remap controls
#Fix keyboard string
#Add a bot
#Add way to duo the bot
#Add other game modes
#Make new clears display based on combo
#Improve credits
#Add increasing speed level

#█░███▓▒░░██▓ ▒██▒░██████▒░▒████▓  ██▓
#░ ▓░▒ ▒  ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░░ ▒░▓  ░ ▒▒▓  ▒  ▒▓▒
#  ▒ ░ ░    ░ ▒ ▒░   ░▒ ░ ▒
#Anti-Shadow
#ingame: shift enter space (r) esc up down left right
#menu: up down left right enter shift

version="1.19.11"

lines_number=973
char_number=26515

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

def print_title(text):
    pass

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
    score=0
    has_swapped=False

    new_clears_display_duration=2
    last_new_clears=float("-inf")
    new_clears=0

    next_pieces=[]
    for i in range(5):
        next_pieces.append(random.choice(list(pieces.keys())))

    presses={key: [None,None] for key in ("up","down","left","right","esc","enter","r","space","shift")}

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

        if clears:

            #audio.play_line_clear_sound()
            Textris.score+=(40,100,300,1200)[clears-1]

            Textris.last_new_clears=time.perf_counter()
            Textris.new_clears=clears

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

        #audio.play_death_sound()

        Textris.grid=[]

        for y in range(Textris.height):
            Textris.grid.append([])
            for x in range(Textris.width):
                Textris.grid[-1].append(0)

        Textris.held_piece=()
        Textris.went_down=0
        Textris.last_input=0

        Textris.lines=0
        Textris.score=0
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

        if is_True and x+y:
            #audio.play_press_sound()
            pass

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

        #audio.play_switch_sound()

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

            #audio.play_hard_drop_sound()

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
        text[i+index*3+4]+=f"   Score: {Textris.score}."
        text[i+index*3+5]+=f"   {['||','>'][paused]}"

        if time.perf_counter()-Textris.last_new_clears<=Textris.new_clears_display_duration:
            text[i+index*3+3]+=f"(+{Textris.new_clears})"
            text[i+index*3+4]+=f"(+{(40,100,300,1200)[Textris.new_clears-1]})"

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

def title_screen():

    Textris.presses_update()

    blink=False
    has_blinked=time.perf_counter()
    index=0
    title_has_moved=time.perf_counter()

    text=art.text2art(f"Textris {version}  by  YknotTYD   ","big")
    l=len(text.split("\n")[1])
    text="\n".join([line*2 for line in ("\n"*3+text).split("\n")])

    press_enter=(art.text2art("    Press Enter    ","small"),art.text2art("[Press Enter]","small"))

    while not Textris.click("enter"):

        Textris.presses_update()

        title="\n".join([line[index:index+64] for line in text.split("\n")])
        title=f"{title}\n\n\n{press_enter[blink]}"

        print(title)

        if time.perf_counter()-title_has_moved>=1/15:
            title_has_moved=time.perf_counter()
            index+=1
            index%=l

        if time.perf_counter()-has_blinked>=1:
            has_blinked=time.perf_counter()
            blink=not(blink)

    #audio.play_selection_sound()
    Textris.presses_update()

def keyboard_settings_loop():

    text="\n"+art.text2art("Keyboard   Controls","big")
    text+="""\n,-------------------------------------------------------------------------,
| [esc][ ][ ][ ][ ]  [ ][ ][ ][ ][ ]  [ ][ ][ ][ ]  [ ][__]  [ ][ ][ ][ ] |
|                                                                         |
|  [ ][ ][ ][r][ ][ ][ ][ ][ ][ ][ ][ ][ ][_]    [ ][ ][ ]  [ ][ ][ ][ ]  |
|  [_][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ← |   [ ][ ][ ]  [ ][ ][ ][ ] |
| [ ][_][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]|↑|   [↑]    [ ][ ][ ][ ]     |
| [__][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][__]    [←][↓][→]  [ ][ ][ ]||     |
|   [__][________________][__]              [__][ ]||                     |
`,-----------------------------------------------------------------------'

In-game:

    Left, Right, Down:
        Moves current piece.

    Up:
        Rotates current piece.

    Space:
        Hard-drops current piece.

    Shift:
        Switches held piece with current piece.

    Enter:
        Pauses/unpauses.

    Escape:
        Goes back to main menu."""

    in_menu="""In menus:

    Up, Down, Left, Right:
        Moves around.

    Enter:
        Selects.

    Escape:
        Goes back."""

    text=text.split("\n")

    for y,line in enumerate(in_menu.split("\n")):
        text[20+y]=f"{text[20+y]:<50}{line}"

    text="\n".join(text)

    while not Textris.click("esc"):

        Textris.presses_update()
        print(text)

    #audio.play_return_sound()
    Textris.presses_update()

def controller_settings_loop():

    text="\n"+art.text2art("Controller   Controls","big")
    text+="""\n\n      _=====_                               _=====_
     / _____ \\                             / _____ \\
   +.-'_____'-.---------------------------.-'_____'-.+
  /   |     |  '.                       .'  |  _  |   \\
 / ___| /|\ |___ \\                     / ___| /_\ |___ \\
/ |      |      | ;  __           _   ; | _         _ | ;
| | <---   ---> | | |__|         |_|  | ||_|       (_)| |
| |___   |   ___| ;SELECT       START ; |___       ___| ;
|\    | \|/ |    /  _     ___      _   \    | (X) |    /|
| \   |_____|  .','" "', |___|  ,'" "', '.  |_____|  .' |
|  '-.______.-' /       \\      /       \\  '-._____.-'   |
|               |       |------|       |                |
|              /\\       /      \\       /\\               |
|             /  '.___.'        '.___.'  \\              |
|            /                            \\             |
 \          /                              \\           /
  \________/                                \\_________/"""

    text+="\n\n\n\n"+art.text2art("[WIP]","small")

    while not Textris.click("esc"):

        Textris.presses_update()
        print(text)

    #audio.play_return_sound()
    Textris.presses_update()

def program_overview_loop():

    text="\n"+art.text2art("Program   Overview","big")
    text+="\n"*3+art.text2art(f"Total   line   number:   {lines_number:_}.".replace("_","   "),"small")
    text+=art.text2art(f"Total   character   number:   {char_number:_}.".replace("_","   "),"small")
    text+=art.text2art(f"Version:   {version}.","small")
    text+=art.text2art(f"Author:   YknotTYD.","small")

    while not Textris.click("esc"):
        Textris.presses_update()
        print(text)

    #audio.play_return_sound()
    Textris.presses_update()

def about_loops():

    text="\n"+art.text2art("About","big")
    text+="\n"*3
    text+=art.text2art("A   textual   Tetris   game   with","small")
    text+=art.text2art("cool   features   I   made   as","small")
    text+=art.text2art("a   spare   project.","small")

    while not Textris.click("esc"):

        Textris.presses_update()
        print(text)

    #audio.play_return_sound()
    Textris.presses_update()

def settings_loop():

    def controls_loop():

        Textris.presses_update()
        controls=("Keyboard   Controls","Controller   Controls")

        selection=0

        while not Textris.click("esc"):

            Textris.presses_update()
            text=""

            direction=Textris.click("down")-Textris.click("up")

            if direction:
                #audio.play_hover_sound()
                selection=min(max(selection+direction,0),len(controls)-1)

            for i,control in enumerate(controls):
                text+=art.text2art(("","-")[i==selection]+control,("small","big")[i==selection])

            print(text)

            if Textris.click("enter"):
                #audio.play_selection_sound()
                (keyboard_settings_loop,controller_settings_loop)[selection]()

        #audio.play_return_sound()
        Textris.presses_update()

    selection=0
    settings=("Controls","Program   Overview","About")

    while not Textris.click("esc"):

        text="\n"

        Textris.presses_update()
        direction=Textris.click("down")-Textris.click("up")

        if direction:
            #audio.play_hover_sound()
            selection=min(max(selection+direction,0),len(settings)-1)

        for i,setting in enumerate(settings):
            text+=art.text2art(("","-")[i==selection]+setting,("small","big")[i==selection])

        print(text)

        if Textris.click("enter"):
            #audio.play_selection_sound()
            (controls_loop,program_overview_loop,about_loops)[selection]()

    #audio.play_return_sound()

def credits_loop():

    height=36
    n=0
    went_down=time.perf_counter()

    text="""\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
Lead   Director
Yknot



Game   Designer
TheYummyDogo



Lead   Programmer
PAD



Art   Director
Me



Lead   Artist
Also   me



Sound   Designer
freesound.org



Gameplay   Programmer
YknotTYD



Playtesters
TYD



Special   Thanks
YknotTYD
TheYummyDogo
PAD
Me





Textris   by   me."""

    text="\n".join([art.text2art(line,"small") for line in text.split("\n")])

    while not Textris.click("esc"):

        if time.perf_counter()-went_down>=1/10:
            went_down=time.perf_counter()
            n=min(n+1,len(text.split("\n"))-height)

        print("\n".join(text.split("\n")[n:n+height]))

        Textris.presses_update()

    #audio.play_return_sound()
    Textris.presses_update()

def main_menu_loop():

    global selection

    Textris.presses_update()

    if direction:=(Textris.click("up")-Textris.click("down")):
        if direction:
            #audio.play_hover_sound()
            selection=max(min(selection-direction,4),0)

    level_selection=0
    settings=1
    creditsTYD=2
    title=3
    ewit=4

    text="\n"*2

    for b,string in zip((level_selection,settings,creditsTYD,title,ewit),
                        ("Level  Selection","Settings","Credits","Title  Screen","Exit")):
        text+=art.text2art(("","-")[b==selection]+string,("small","big")[b==selection])+"\n"*2

    text=text[:-2]

    print(text)


    def door():
        keyboard.press_and_release("alt+f4")

    if Textris.click("enter"):
        #audio.play_selection_sound()
        (level_selection_loop,settings_loop,credits_loop,title_screen,door)[selection]()

def level_selection_loop():

    selection=[0,0]
    grid=[[0,1,2,3,4],
          [5,6,7,8,9]]

    Textris.presses_update()

    while not (Textris.click("enter") or Textris.click("esc")):

        direction=(Textris.click("up")-Textris.click("down"),Textris.click("left")-Textris.click("right"))

        if any(direction):

            #audio.play_hover_sound()

            selection[0]=max(min(selection[0]-direction[1],4),0)
            selection[1]=max(min(selection[1]-direction[0],1),0)

        nums=[]
        for y,line in enumerate(grid):
            nums.append([])
            for x,num in enumerate(line):
                num=art.text2art(str(num),("small","big")[[x,y]==selection])
                nums[-1].append(num)

        text=list("\n"*22)
        for y,line in enumerate(nums):
            for x,num in enumerate(line):
                for index,numline in enumerate(num.split("\n")):
                    text[index+y*9]+=f"{numline:>9}"
            text+="\n"

        text="".join(text)
        text=text.split("\n")
        del text[8]
        del text[8]
        text="\n".join(text)

        text="\n".join([" "*9+line for line in text.split("\n")])
        text="\n".join([" "+line for line in art.text2art("Level Selection","small").split("\n")])+text

        print(text)

        Textris.presses_update()

    if Textris.click("enter"):

        #audio.play_selection_sound()
        Textris.gravity=1/(grid[selection[1]][selection[0]]*2+1)
        main_loop()

    if Textris.click("esc"):
        #audio.play_return_sound()
        pass

def main_loop():

    global paused

    while not keyboard.is_pressed("esc"):

        Textris.presses_update()

        if Textris.click("r"):
            Textris.grid=[[0 for i in range(Textris.width)] for i in range(Textris.height)]

        if Textris.click("enter"):
            #audio.play_pause_sound()
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

    #audio.play_return_sound()
    paused=True

def launch_no_wrapper():

    global selection

    Textris.init()
    ##audio.play_music()

    title_screen()

    selection=0
    while True:
        main_menu_loop()

def launch():
    curses.wrapper(launch_no_wrapper())
    curses.endwin()

if __name__=='__main__':
    launch()