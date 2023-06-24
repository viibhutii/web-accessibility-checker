
# Import libraries
from pip._vendor import requests
from bs4 import BeautifulSoup
import tkinter as tk
from urllib.parse import urlparse
#from nltk.corpus import stopwords

# Creates a UI window
window = tk.Tk()

# Sets the size and title of the window
window.geometry("800x500")
window.title("Web Accessibility Checker")

# Creates a label widget with the text "URL" and sets font and padding configurations, 
# packed to be displayed on UI
label = tk.Label(window, 
                 text="URL", 
                 font=('Arial', 18))
label.pack(padx=10, 
           pady=10)

# Creates an entry widget for the URL and sets width and packs it to display on UI
url_input = tk.StringVar() # Reading from a textbox in string format
url = tk.Entry(window, 
               width=80,
               font=('Arial', 14)
               )
url.pack()
# print("url1", url)

# Function to get article content 
def get_article_content():

    # Send a request to check for a response and then gather content from URL
    url_temp = url.get()
    url_temp.replace(u'\ufeff', '')
    response = requests.get(url_temp)
    response = response.text
    print("reponse 2",response)

    # Parse html response
    soup = BeautifulSoup(response, 'html.parser')
    # Complete article content
    content = soup.find('div', class_='content')
    # Aricle title
    header = content.find('h1', class_='article__title').text.strip()
    # Each section under an article (i.e., 1 subheader per section)
    sections = content.find_all('div', class_='step step-depth-1')

    return header, sections

# Function to display content 
def display_content():

    # Retrieves parsed header and sections of content from URL
    header, sections = get_article_content()

    # Clears previous content
    output_text.delete(1.0, tk.END) 

    # ARTICLE_TITLE 
    # Outputs title onto User Interface (UI). Checks for capitalization and naming convention 
    if not header.startswith("How to"):
        output_text.insert(tk.END, f"Title: {header}\n** Incorrect naming convention. Try starting with 'How to'.\n\n", "red_text")
    else:
        output_text.insert(tk.END, f"Title: {header}\n\n")

    # ARTICLE_SECTIONS
    # Breaks down article into numbered sections
    count = 0
    for section in sections:
        print(f"section {count}")
        count += 1
        
        # Finds and prints subheader under each section
        a = section.find('a')
        subheading = a.attrs['aria-label']
        subheader = subheading.replace("Anchor for ", '')
        print("     subheading: ", subheader)

        # Outputs the section number and subheader onto UI
        output_text.insert(tk.END, f"Section {count}\n\n")
        output_text.insert(tk.END, f"    Subheading: {subheader}\n\n")

        # ARTICLE_IMAGES & ALT_TEXT
        # Finds all images under section
        images = section.find_all('img')

        # Set initial condition as sections having no images
        has_image = False

        # Section has image, hence get alt_text
        for image in images:
            if image is not None:
                has_image = True
                alt = image.get('alt')
                
                # message for missing alt texts in red color
                if not alt:
                    output_text.insert(tk.END, "    Alt Text: Image does not have alt text\n", "red_text")
                # outputs alt text and message of capitalization error in first word in red color
                elif alt[0].islower():
                    output_text.insert(tk.END, f"    Alt Text: {alt}\n    ** First letter is not capitalized **", "red_text")
                # outputs alt text 
                else:
                    output_text.insert(tk.END, f"    Alt Text: {alt}\n")

        if not has_image:
            output_text.insert(tk.END, "    No image(s) found in this section\n", "blue_text") 

        # Gets and outputs alt text onto the UI for each image(s) under the section
        output_text.insert(tk.END, "\n")


# Creates a button widget, and sets text, font, command to execute when clicked, 
# padding, and packed to display on UI
button = tk.Button(window, 
                   text="OK", 
                   font=('Arial', 18), 
                   command=display_content)
button.pack(padx=20, pady=20)

# Creates a scroll bar
scrollbar = tk.Scrollbar(window)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Creates text widget to display output and packs it to display window with padding
output_text = tk.Text(window, 
                      height=400, 
                      width=200,
                      font=('Arial', 14),
                      yscrollcommand=scrollbar.set
                      )
output_text.pack(padx=16, 
                 pady=16)

# Configures the scroll bar to work with the text widget
scrollbar.config(command=output_text.yview)

# Sets foreground color as red for text tag named "red_text"
output_text.tag_config("red_text", 
                       foreground="red")
# Sets foreground color as blue for text tag named "blue_text"
output_text.tag_config("blue_text", 
                       foreground="blue")

# Starts the event to handle user interactions and keeps the window running
window.mainloop()



