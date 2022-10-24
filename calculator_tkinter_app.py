#****this is a calculator app using python tkinter. followed tutorial youtube channel Programiz****

#!/usr/bin/env python3

#import virtualenv

#print(dir(virtualenv))

import tkinter as tk


#constant
LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGIT_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

OFF_WHITE = "#F8FAFF"
WHITE = "#FFFFFF"
LIGHT_BLUE = "#CCEDFF"
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"


class Calculator:
    def __init__(self):
        self.window = tk.Tk() #create the window of the calc using the tk class of the Tkinter module
        self.window.geometry("375x667") #specify the width and height of the window
        self.window.resizable(0,0) #disable resizing for the window
        self.window.title("Calculator") #gave the app name 

        #display current expressions and total expressions
        self.total_expression = ""
        self.current_expression = ""
        #create frame for display and buttons
        self.display_frame = self.create_display_frame()
        
        self.total_label, self.label = self.create_display_labels()
       
        #buttons with their positiob
        self.digits = {
            7:(1,1), 8:(1,2), 9:(1,3),
            4:(2,1), 5:(2,2), 6:(2,3),
            1:(3,1), 2:(3,2), 3:(3,3),
            0:(4,2), '.':(4,1)
        }

        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"} #create a dictionary/list if want to loop
        self.buttons_frame = self.create_buttons_frame()

        #make the buttons span the entire buttons frame/app
        self.buttons_frame.rowconfigure(0,weight=1)

        
        for x in range(1,5):
            self.buttons_frame.rowconfigure(x,weight=1)
            self.buttons_frame.columnconfigure(x,weight=1)


        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()

    #make it so we can enter the digits/operators through keyboard
    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate()) #this code means that pressing enter key on the keyboard is the same as clicking the equal button on the app
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))

        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equal_button()
        self.create_square_button()
        self.create_sqrt_button()

    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=LIGHT_GRAY, 
                                fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE) #padx padding in horizontal
        total_label.pack(expand=True, fill="both")

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=LIGHT_GRAY, 
                                fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE) #padx makes it horizontal
        label.pack(expand=True, fill="both")

        return total_label, label
        
    
    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both") #allow frame to expand and fill empty spaces
        return frame

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()


    def create_digit_buttons(self):
        for digit,grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DIGIT_FONT_STYLE, 
                                borderwidth=0, command=lambda x=digit: self.add_to_expression(x)) #borderwidth set to 0 supposed to remove border of the buttons & command is used to add functionality to the button
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator): #when we click the operator button it will be appended to the digit we input
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()


    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=lambda x=operator: self.append_operator(x))
            #then place these operator buttons to the buttons frame grid
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i+=1

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_total_label()
        self.update_label()


    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="C", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.clear)
            #then place these operator buttons to the buttons frame grid
        button.grid(row=0, column=1, sticky=tk.NSEW)
    
    def square(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()

    def create_square_button(self):
        button = tk.Button(self.buttons_frame, text="x\u00b2", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.square)
            #then place these operator buttons to the buttons frame grid
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def sqrt(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()

    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame, text="\u221ax", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.sqrt)
            #then place these operator buttons to the buttons frame grid
        button.grid(row=0, column=3, sticky=tk.NSEW)

    #eval function evaluates and returns the value of a valid python expression 
    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            self.current_expression = str(eval(self.total_expression)) 
            self.total_expression = ""
        except Exception as e:   #if division by 0 will throw exception error
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_equal_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.evaluate)
            #then place these operator buttons to the buttons frame grid
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)
        
    
    def create_buttons_frame(self):
        frame = tk.Frame(self.window) #the background color for buttons frame has been set to black by default. 
        frame.pack(expand=True, fill="both")
        return frame

    def update_total_label(self):
        expression = self.total_expression   #replace multiply and division symbol * and / to x and 
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)
    
    def update_label(self):
        self.label.config(text=self.current_expression[:11]) #truncate the result so its not overflow using slicing

    #start calculator app
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calc = Calculator()
    calc.run() 


    #create an .exe file of the calculator app so that it can run the app at any window without any python setup (stand alone executable)
    #use pyinstaller. first install pip3 install pyinstaller
    #then to convert calculator.py to calculator.exe ==> pyinstaller --onefile -w (name of our py file), onefile means create a single file only, and w means that python should not bring up the terminal when we call the file
    #go the project folder and inside dist folder, the exec has been created. when open that file, the calculator app will be open

    
