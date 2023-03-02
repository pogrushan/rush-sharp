#isolang: Rush# (Rush Sharp)
#isolang version: 1.0
#written in python 3.10.7
#written by -Rushan S Jawaid
# basically this is like a simple programming language that is used to control the turtle graphics

import os

#used to reference the 'icon.png' while in executable format
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

#used it while debugging to see the type of variable in bad egg for weird chars
debug = lambda i: print(str(type(i)) + " " + "'"+i+"'")
import tkinter

#make a window with 10 box labels
window = tkinter.Tk()
a = tkinter.Image("photo", file=resource_path("icon.png"))
window.iconphoto(True, a)
window.title("Rush# Counter")
window.geometry(f"480x200")

global labels_r1
labels_r1 = [tkinter.Label(window, text=str(str(i+1))) for i in range(40)]
#make a grid of 10x4 labels (40) to display the counter
for i in range(40):
    row = 0
    if i >= 10 and i < 20:
        row = 1
    elif i >= 20 and i < 30:
        row = 2
    elif i >= 30:
        row = 3
    labels_r1[i].grid(row=row, column=i%10)
    labels_r1[i].config(height=3, width=6)
    labels_r1[i].config(bg="grey")
    labels_r1[i].config(border=2, relief="groove")
labels_r1.insert(0, tkinter.Label(window, text=""))

#parser for the code
class Parser(object):
    def __init__(self, function_table):
        #replace all ; with \n and split the string into a list of lines so that each line is a line of 'code'
        self.function_table = function_table.replace(";","\n")
        self.function_table = self.function_table.split("\n")
        self.index, self.cur_line = 0, ""
        self.mem, self.out = [], []
        self.baddegg = []
        super(Parser, self).__init__()
    def nxt_line(self):
        #goto next line of code if there is one
        if self.index >= len(self.function_table):
            return False
        #place the next line of code into memory
        self.cur_line = self.function_table[self.index]
        self.index += 1
        return True
    def brk_at(self):   
        #basically split the code into 2 parts. Function name and rest all al arguments to the function
        self.mem = self.cur_line.split(" ")
        counter = 0
        for i in self.mem:
            if i.isspace():
                self.mem.pop(counter)
                #if its BAD CHAR then add it to the list of bad chars
                self.baddegg.append(i)
            else: 
                for badchar in self.baddegg:
                    if badchar == i:
                        self.mem.pop(counter)
                f_mem_t = self.mem.copy()
                self.mem = []
                for i in f_mem_t:
                    if i != '':
                        self.mem.append(i)
            counter += 1
    def parse(self):
        #in the final list 'out', transform the raw code into a list consisting of the function and a list of args
        f_mem = self.mem.copy()
        try:
            func_n = f_mem[0]
            f_mem.pop(0)
            self.out.append([func_n ,f_mem])
        except: 
            if len(f_mem) < 1: pass
            else: self.out.append(f_mem)

#this part runs the code 
class Intepretter(object):
    def __init__(self, function_table):
        #define input code and setup turtle
        self.function_table = function_table
        self.index, self.cur_line = 0, ""
        self.runtime = ""
        self.total_counter = 0
        import turtle
        self.pn = turtle.Turtle()
        super(Intepretter, self).__init__()
    def nxt_line(self):
        #same as the parser; goto next line of code if there is one and place it in memory
        if self.index >= len(self.function_table):
            return False
        self.cur_line = self.function_table[self.index]
        self.index += 1
        return True
    def run_line(self):
        #this part runs the code. 
        def inner(func, *args):
            #total counter shows lines of code whereas the root counter defined at top shows true lines/written lines 
            self.total_counter += 1
            try:
                labels_r1[self.total_counter+1].config(bg="green")
            except: 
                #if the line of code is more than 40 then make the background of all labels red
                for i in labels_r1:
                    i.config(bg="red")
            # basically this just shows the function and its args in the console
            self.runtime = str(func).ljust(14, " ") + " " + str(args)
            import time, turtle
            chk_args = False
            if len(args) > 0:
                chk_args = True
            #--------------------------------------------------
            if func == "set_base":
                #set the base to be decimal(10), binary(2), octal(8), hexadecimal(16) etc
                self.base = int(args[0])
            elif func == "n_screen":
                #setup screen with user defined size and initial position
                self.screen = turtle.Screen()
                img = tkinter.PhotoImage("photo", file=resource_path("icon.png"))
                #turtle._Screen._root.iconphoto(True, img)
                splsh_img = tkinter.PhotoImage(file=resource_path("icon.png"),master=turtle._Screen._root)
                self.screen.setup(int(args[0],self.base), int(args[1],self.base), startx=int(args[2],self.base), starty=int(args[3],self.base))
                self.screen.title("Rush# Graphics Window")
            elif func == "set_title":
                #set the title of the screen
                self.screen.title(args[0].replace('"', '').replace("'", ""))
            elif func == "reg_shape":
                #to set the shape, we first must register the shape in the screen
                self.screen.register_shape(args[0].replace('"', '').replace("'", ""))
            elif func == "n_turtle":
                #now we can create a turtle
                self.pn = turtle.Turtle()
            elif func == "set_shape":
                #set the shape of the turtle (must come after reg_shape and n_turtle)
                self.pn.shape(args[0].replace('"', '').replace("'", ""))
            elif func == "pd":
                #move with pen down
                self.pn.pendown() 
            elif func == "fd":
                #move forward
                self.pn.forward(int(args[0],self.base))
            elif func == "bk":
                #move backward
                self.pn.backward(int(args[0],self.base))
            elif func == "rt":
                #turn right
                self.pn.right(int(args[0],self.base))
            elif func == "lt":
                #turn left
                self.pn.right(int(args[0],self.base))
            elif func == "wait":
                #wait for a certain amount of time (seconds)
                time.sleep(int(args[0],self.base))
            elif func == "millis":  
                #wait for a certain amount of time (milliseconds)
                time.sleep(int(args[0],self.base)/1000)
            elif func == "pu":
                #move with pen up  
                self.pn.penup()
            elif func == "set_pos":
                #set the position of the turtle
                self.pn.setpos(int(args[0],self.base), int(args[1],self.base))
            elif func == "size":
                #set the size of the turtle
                self.pn.turtlesize(int(args[0],self.base), int(args[1],self.base))
            elif func == "set_color":
                #set the color of the turtle
                self.pn.color(args[0].replace('"', '').replace("'", ""))
            elif func == "set_heading":
                #set the heading of the turtle in degrees
                self.pn.setheading(int(args[0],self.base))
            elif func == "set_heading_by":
                #increase or decrease the heading of the turtle by a certain amount of degrees
                self.pn.setheading(self.pn.heading() + int(args[0],self.base))
            elif func == "repeat":
                #repeat lines in [ ... ]
                self.i_runtime = self.runtime
                #so that the output in console reds s repeat ..n [ ... ]
                for i in range(int(args[0],self.base)):
                    str_ = ""
                    for kll in args[1:len(args)]:
                        #to remove the [ and ] from the args and make it a string
                        str_ += kll
                        str_ += " "
                    str_ = str_[:-1]
                    #split lines by comma into separate lines of code to be ran
                    lines = str_.split(",")
                    for ik in lines:
                        #run each line of code 
                        inner(ik.split(" ")[0], *ik.split(" ")[1:])
                        #send repeated lines of code running to the console
                        print("     Rpt"  + "  " + str(str(i)).zfill(4) + "  " + str(intepretter.runtime))
                    self.runtime = self.i_runtime
            #--------------------------------------------------
            else:
                #check if it is a comment
                if "//^" in func:
                    pass
                else:
                    #its not so the function is not found; raise error
                    print("Error: Function not found")
                    print("Function: " + func)
        func = self.cur_line[0]
        args = self.cur_line[1]
        for i in args:
            #remove the [ and ] from the args
            if i == "[" or i == "]":
                args.pop(args.index(i))
        #run the function which if-runs the code
        inner(func, *args)

import sys
#read the code
with open(sys.argv[1], "r") as f:
    in_run = f.read()
    f.close()

#parse the code
parsed = Parser(in_run)
run_ = True
while run_:
    ret = parsed.nxt_line()
    if not ret:
        #there is no next line so break and set out toe the parsed code
        out = parsed.out
        break
    else:
        #there is a next line; goto it and parse it
        parsed.brk_at()
        parsed.parse()

interpret_ = True
intepretter = Intepretter(out)
while interpret_:
    ret = intepretter.nxt_line()
    #it never light up so forced it to
    labels_r1[1].config(bg="green")
    if ret == False:
        #there is no next line so end the intepretter
        break 
    else:
        #there is a next line;intepret it
        intepretter.run_line()
        #debug to the console about current line ofcode that was executed
        print(str(ret)  + "  " + str(intepretter.index).zfill(4) + "  " + str(intepretter.runtime))

#admire ze output
import time
time.sleep(5)



#Finished on 02-02-2023
#isolang: Rush# (Rush Sharp)
#isolang version: 1.0
#written by -Rushan S Jawaid