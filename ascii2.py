import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


class ASCIIArtEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("ASCII Art Editor")
        self.create_main_frame()
        self.create_options_frame()
        self.create_text_frame()

    def create_main_frame(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)
        self.canvas = tk.Canvas(self.main_frame, width=400, height=400, bg="white")
        self.canvas.pack(side=tk.LEFT)
        self.image_path = tk.StringVar()
        path_entry = tk.Entry(self.main_frame, textvariable=self.image_path, width=50)
        path_entry.pack(side=tk.LEFT, padx=10)
        browse_button = tk.Button(self.main_frame, text="Browse", command=self.browse_image)
        browse_button.pack(side=tk.LEFT)
        generate_button = tk.Button(self.main_frame, text="Generate", command=self.generate_ascii)
        generate_button.pack(side=tk.LEFT, padx=10)
        save_button = tk.Button(self.main_frame, text="Save Text", command=self.save_text)
        save_button.pack(side=tk.LEFT)

    def create_options_frame(self):
        self.options_frame = tk.Frame(self.main_frame)
        self.options_frame.pack(side=tk.LEFT, padx=10, pady=10)
        self.char_width = tk.IntVar(value=80)
        self.char_height = tk.IntVar(value=40)
        self.font_size = tk.IntVar(value=10)
        self.grayscale_method = tk.StringVar(value="Average")
        self.character_set = tk.StringVar(value="+_)(*&^%$#@!) ")
        width_label = tk.Label(self.options_frame, text="Character Width:")
        width_label.grid(row=0, column=0, sticky=tk.W)
        width_entry = tk.Entry(self.options_frame, textvariable=self.char_width)
        width_entry.grid(row=0, column=1)
        height_label = tk.Label(self.options_frame, text="Character Height:")
        height_label.grid(row=1, column=0, sticky=tk.W)
        height_entry = tk.Entry(self.options_frame, textvariable=self.char_height)
        height_entry.grid(row=1, column=1)
        font_label = tk.Label(self.options_frame, text="Font Size:")
        font_label.grid(row=2, column=0, sticky=tk.W)
        font_entry = tk.Entry(self.options_frame, textvariable=self.font_size)
        font_entry.grid(row=2, column=1)
        grayscale_label = tk.Label(self.options_frame, text="Grayscale Method: ")
        grayscale_label.grid(row=3, column=0, sticky=tk.W)
        grayscale_options = ["Average", "Red", "Green", "Blue"]
        grayscale_menu = tk.OptionMenu(self.options_frame, self.grayscale_method, *grayscale_options)
        grayscale_menu.grid(row=3, column=1)
        charset_label = tk.Label(self.options_frame, text="Character Set: ")
        charset_label.grid(row=4, column=0, sticky=tk.W)
        charset_entry = tk.Entry(self.options_frame, textvariable=self.character_set)
        charset_entry.grid(row=4, column=1)

    def create_text_frame(self):
        self.text_frame = tk.Frame(self.root)
        self.text_frame.pack(fill=tk.BOTH, expand=True)
        text_scrollbar = tk.Scrollbar(self.text_frame)
        text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text = tk.Text(self.text_frame, wrap=tk.NONE, yscrollcommand=text_scrollbar.set)
        self.text.pack(fill=tk.BOTH, expand=True)
        text_scrollbar.config(command=self.text.yview)

    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.image_path.set(file_path)
            self.load_image(file_path)

    def load_image(self, image_path):
        # Load the selected image and display it on the canvas
        image = Image.open(image_path)
        image.thumbnail((400, 400))
        photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
        self.canvas.image = photo

    def generate_ascii(self):
        image_path = self.image_path.get()
        char_width = self.char_width.get()
        char_height = self.char_height.get()
        font_size = self.font_size.get()
        grayscale_method = self.grayscale_method.get()
        character_set = self.character_set.get()

        if image_path:
            self.convert_image_to_ascii(image_path, char_width, char_height, font_size, grayscale_method, character_set)

    def convert_image_to_ascii(self, image_path, char_width, char_height, font_size, grayscale_method, character_set):
        try:
            # Open the image and convert it to grayscale
            image = Image.open(image_path)
            grayscale_image = image.convert("L")
            
            # Resize the grayscale image to match the specified character width and height
            resized_image = grayscale_image.resize((char_width, char_height))
            
            ascii_text = ""
            for y in range(char_height):
                for x in range(char_width):
                    # Extract a crop region from the resized image based on font size
                    left = x * font_size
                    top = y * font_size
                    right = left + font_size
                    bottom = top + font_size
                    crop = resized_image.crop((left, top, right, bottom))
                    
                    # Calculate the average pixel value based on the selected grayscale method
                    if grayscale_method == "Average":
                        avg_pixel = int(sum(crop.getdata()) / len(crop.getdata()))
                    elif grayscale_method == "Red":
                        avg_pixel = int(sum(c[0] for c in crop.getdata()) / len(crop.getdata()))
                    elif grayscale_method == "Green":
                        avg_pixel = int(sum(c[1] for c in crop.getdata()) / len(crop.getdata()))
                    elif grayscale_method == "Blue":
                        avg_pixel = int(sum(c[2] for c in crop.getdata()) / len(crop.getdata()))
                    
                    # Map the average pixel value to a character from the selected character set
                    char_index = int(avg_pixel / 256 * len(character_set))
                    ascii_char = character_set[char_index]
                    ascii_text += ascii_char
                ascii_text += "\n"
            self.display_ascii_text(ascii_text)
        except Exception as e:
            self.display_message(f"Error during conversion: {str(e)}")

    def display_ascii_text(self, ascii_text):
        # Clear the text area and display the ASCII art
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, ascii_text)

    def save_text(self):
        ascii_text = self.text.get("1.0", tk.END)
        if not ascii_text:
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(ascii_text)
            except Exception as e:
                self.display_message(f"Failed to save text: {str(e)}")

    def display_message(self, message):
        print(message)


root = tk.Tk()
ASCIIArtEditor(root)
root.mainloop()
