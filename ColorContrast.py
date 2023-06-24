import tkinter # gui builder
from functools import partial # way to allow gui builder classes to call functions and pass them parameters (doesn't work the normal way for some reason)
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
# R,G, and B need to be the 8bit values of the Red, Green, and Blue values for the color you're trying to get the luminance for
def CalcLuminance(R,G,B):
    RsRGB = R/255
    GsRGB = G/255
    BsRGB = B/255
    #gets luminance for the Red value
    if RsRGB <= 0.03928:
        R = RsRGB/12.92
    else:
        R = ((RsRGB+0.055)/1.055)**2.4
    #gets luminance for the Green value
    if GsRGB <= 0.03928:
        G = GsRGB/12.92
    else:
        G = ((GsRGB+0.055)/1.055)**2.4
    #gets luminance for the Green value
    if BsRGB <= 0.03928:
        B = BsRGB/12.92
    else:
        B = ((BsRGB+0.055)/1.055)**2.4
    #gets the total luminance
    L = (0.2126 * R) + (0.7152 * G) + (0.0722 * B)
    return L

#the luminance value of the colors, takes in two color luminances
def CalcContrastRatio(Lum1,Lum2):
    if Lum1 > Lum2:
        L1 = Lum2
        L2 = Lum1
    else:
        L1 = Lum1
        L2 = Lum2
    #the larger luminance is the dividend  
    return (L1 + 0.05) / (L2 + 0.05)

#takes in the contrast Ratio
def WCAGSChecks(CR):
    #dictionary of all of the WCAGS checks
    CheckDict = {"AA-Level Large Text":"FAIL",
                 "AA-Level Small Text":"FAIL",
                 "AAA-Level Large Text":"FAIL",
                 "AAA-Level Small Text":"FAIL"}
    #the different levels for WCAGS checks, if they pass the check, the dictionary is changed to pass
    if CR < 1/3:
        CheckDict["AA-Level Large Text"] = "PASS"
    if CR < 1/4.5:
        CheckDict["AA-Level Small Text"] = "PASS"
    if CR < 1/4.5:
        CheckDict["AAA-Level Large Text"] = "PASS"
    if CR < 1/7:
        CheckDict["AAA-Level Small Text"] = "PASS"
    #returns the Dictionary of all of the Checks
    return CheckDict
# this function is for simplicity, makes the overall function calling much easier
def checkContrast(list1,list2):
    return WCAGSChecks(CalcContrastRatio(CalcLuminance(int(list1[0]),int(list1[1]),int(list1[2])),CalcLuminance(int(list2[0]),int(list2[1]),int(list2[2]))))

#some tests to verify that the code works
# print(WCAGSChecks(CalcContrastRatio(CalcLuminance(0,0,0),CalcLuminance(255,255,255))))
# print(WCAGSChecks(CalcContrastRatio(CalcLuminance(255,255,255),CalcLuminance(255,255,255))))
# print(WCAGSChecks(CalcContrastRatio(CalcLuminance(200,200,200),CalcLuminance(255,255,255))))
# print(WCAGSChecks(CalcContrastRatio(CalcLuminance(100,100,100),CalcLuminance(255,255,255))))
# print(WCAGSChecks(CalcContrastRatio(CalcLuminance(120,120,120),CalcLuminance(255,255,255))))

# old way of getting html, don't use ---
#HTMLStringArray = str(requests.get("https://snhu.screenstepslive.com/a/1599442-how-to-access-as-a-student").content).replace(" ","").split("\\n")

# size = len(HTMLStringArray)
# i = 0
# while i < size:
#     if HTMLStringArray[i] == "":
#         HTMLStringArray.pop(i)
#         i -= 1
#         size -= 1
#     i += 1
#print(HTMLStringArray)
#Don't use the above code ---

# #this is a text window I used to get used to tkinter
# class Window(tkinter.Tk):
#     def __init__(self):
#         super().__init__()

#         self.title("Color Contrast Checker")

#         self.button = tkinter.Button(text="close")
#         self.button.bind("<Button-1>",self.CloseWindow)
#         self.button.pack()
    
#     def CloseWindow(self,event):
#         self.destroy()

# window = Window()
# window.mainloop()

#this is the main window that tkinter will open for the Color Contrast checker
class ColorContrastCheckWindow(tkinter.Tk):
    def __init__(self):
        super().__init__()
        
        #this sets the title and window size
        self.title("Color Contrast Checker")
        self.geometry("600x400")

        #this is the function that takes the values out of the text boxes, empties the text fields for the text boxes, 
        # and then changes the output label to contain the results of the color contrast tests
        def Calculate():
            RGB1Val = self.RGB1.get().split(",")
            RGB2Val = self.RGB2.get().split(",")
            self.RGB1.set("")
            self.RGB2.set("")
            checkResults = str(WCAGSChecks(CalcContrastRatio(CalcLuminance(int(RGB1Val[0]),int(RGB1Val[1]),int(RGB1Val[2])),CalcLuminance(int(RGB2Val[0]),int(RGB2Val[1]),int(RGB2Val[2]))))).strip("}{").split(",")
            self.label4.config(text=str(checkResults[0] + "\n" + checkResults[1] + "\n" + checkResults[2] + "\n" + checkResults[3]))
        
        def urlContrast():
            url = self.url.get()
            print(url)
            #this instantiates a webdriver or just an automation "agent" for the web
            driver = webdriver.Chrome()

            #this send the webdriver to the desired url
            driver.get(url)

            #this has the code pause for 2 seconds, allowing the website to load
            time.sleep(2)

            # this line grabs the entire html document, and uses it to get a list of all of the child elements, which in this case would be the whole webpage
            elements = driver.find_element(By.TAG_NAME,"html").find_elements(By.XPATH,".//*")

            #Have the outline simply report the text and then the test reports for the text

            # # this loop runs through the above list and finds only the elements with text in them, and prints out their color
            # for i in elements:
            #     if i.text != '':
            #         print(f"{i.tag_name}: {i.value_of_css_property('color')} ",end="")
            #         # the below 3 lines are used to find the parent element that is visible, thus the background for the text previously found
            #         parent = i.find_element(By.XPATH,"..")
            #         while (not parent.is_displayed):
            #             parent = parent.find_element(By.XPATH,"..")
            #         print(f"Parent: {parent.tag_name}: {parent.value_of_css_property('color')}")

            #this loop does the same as above except runs it though the color contrast checker and puts the output in a text file
            file = open("ColorContrastOutput.txt","w")
            for i in elements:
                if i.text != '':
                    parent = i.find_element(By.XPATH,"..")
                    while (parent.value_of_css_property('background-color').strip('rgba()').replace(' ','').split(',')[3] == '0'):
                        parent = parent.find_element(By.XPATH,"..")
                    text = i.text.replace("\n","\n\t")
                    file.write(f"{i.tag_name}: Text Color: {i.value_of_css_property('color')} Background Color: {parent.value_of_css_property('background-color')}\n\t{text}\n{checkContrast(i.value_of_css_property('color').strip('rgba()').replace(' ','').split(','),parent.value_of_css_property('background-color').strip('rgba()').replace(' ','').split(','))}\n\n")
            file.close()

        # these are the labels and text boxes that make up the main body of the window
        self.label1 = tkinter.Label(self,text="First Color RGB Value: (000,000,000)")
        self.RGB1 = tkinter.StringVar()
        self.entry1 = tkinter.Entry(self,textvariable=self.RGB1)
        self.label2 = tkinter.Label(self,text="Second Color RGB Value: (000,000,000)")
        self.RGB2 = tkinter.StringVar()
        self.entry2 = tkinter.Entry(self,textvariable=self.RGB2)
        self.button = tkinter.Button(self,text="Calculate",command=Calculate)
        self.label3 = tkinter.Label(self,text="Result:")
        self.label4 = tkinter.Label(self,text="")

        # this section consists of the labels and entry boxes for the 
        self.label5 = tkinter.Label(self,text="URL to be checked: (this will open a new chrome tab, wait for the tab to close itself)")
        self.url = tkinter.StringVar()
        self.entry3 = tkinter.Entry(self,textvariable=self.url)
        self.button2 = tkinter.Button(self,text="Calculate",command=partial(urlContrast))
        self.label6 = tkinter.Label(self,text="Results will be in the \"ColorContrastOutput.txt\" file")
        
        # these lines set the position of the above elements, in a grid format
        self.label1.grid(row=0,column=0)
        self.entry1.grid(row=0,column=1)
        self.label2.grid(row=1,column=0)
        self.entry2.grid(row=1,column=1)
        self.button.grid(row=2,column=0)
        self.label3.grid(row=3,column=0)
        self.label4.grid(row=3,column=1)
        self.label5.grid(row=4,column=0)
        self.entry3.grid(row=4,column=1)
        self.button2.grid(row=5,column=0)
        self.label6.grid(row=6,column=0)

# this runs the window
ColorContrastCheckWindow().mainloop()

