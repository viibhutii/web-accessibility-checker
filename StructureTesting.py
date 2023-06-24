import requests, tkinter

# this is the main window for tkinter
class mainWindow(tkinter.Tk):
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)

        # this establishes the title and size of the window
        self.title("Header Structure Checker")
        self.geometry("1000x500")

        # this establishes the hard-typed variables used in the window
        self.url = tkinter.StringVar()
        self.entrySection = tkinter.LabelFrame()
        self.resultSection = tkinter.LabelFrame()
        self.result = tkinter.Text(self.resultSection)

        self.refresh()

    # this refreshes all of the elements on the tkinter page
    def refresh(self):
        self.entrySection.grid_remove()
        self.resultSection.grid_remove()
        # the entry section, entry label, button, and entry box
        self.entrySection.grid(row=0,column=0)
        #label for entry
        tkinter.Label(self.entrySection,text="Enter the URL: ").grid(row=0,column=0)
        #actual textbox to enter the url
        tkinter.Entry(self.entrySection,textvariable=self.url).grid(row=0,column=1)
        #submit button
        tkinter.Button(self.entrySection,text="Submit",command=self.checkHeaders).grid(row=0,column=2)
        #this section contains the result
        self.resultSection.grid(row=1,column=0)
        #result label
        tkinter.Label(self.resultSection,text="Result:").grid(row=1,column=0)
        #result text box
        self.result.grid(row=2,column=0)

    def checkHeaders(self):
        #this empties the text box contianing the result of the test
        self.result.delete("1.0","end")
        #this grabs the url from the variable and then uses requests to get the page content
        url = self.url.get()
        content = str(requests.get(url).content).replace("\\n","")

        # empty array to hold the website tags
        contentArray = []
        #indexes for the following for loop's operation
        startIndex = 0
        endIndex = 0

        #this loop divideds the content of the page up into an array of all of the tags on the website
        for i in range(len(content)):
            if content[i] == "<":
                # depreciated, don't need the contents of a tag, just the tags
                # if i != endIndex+1:
                #     if content[endIndex+1:i].replace(" ","") != "":
                #         print(content[endIndex+1:i].strip(" "))
                startIndex = i
            elif content[i] == ">" and (content[startIndex:i+1].count("\"") % 2 == 0):
                endIndex = i
                contentArray.append(content[startIndex:endIndex+1])

        # this loop grabs every header in the webpage and puts it into "headerArray"
        headerArray = []
        for i in contentArray:
            if "<h" in i:
                if "<head" in i or "<html" in i:
                    continue
                headerArray.append(i)

        # some test cases
        #headerArray = ["<h2>","<h3>","<h4>","<h3>","<h5>","<h2>","<h4>"]

        # these are tags that change the text of the final result readout
        self.result.tag_config("Failed", foreground="red")
        self.result.tag_config("Passed", foreground="green")

        # this loop runs through every heading in the webpage, if it is out of order, 
        # if it is more than one step away from the previous header, it says it failed, otherwise it says it passed
        for i in range(len(headerArray)):
            if i == 0 or (int(headerArray[i][2:3]) <= int(headerArray[i-1][2:3]) or int(headerArray[i][2:3])-1 == int(headerArray[i-1][2:3])):
                self.result.insert(str(i+1)+ ".0",headerArray[i] + ": Heading Structure Good\n")
                self.result.tag_add("Passed", f"{str(i+1)}.0", f"{str(i+1)}.0 lineend")
            else:
                self.result.insert(f"{str(i+1)}.0",headerArray[i] + ": Skipped a Heading Level\n")
                self.result.tag_add("Failed", f"{str(i+1)}.0", f"{str(i+1)}.0 lineend")

        self.refresh()
        
mainWindow().mainloop()