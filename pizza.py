import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
root = tk.Tk()

class PizzaMakerGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title(70 * " " + "Procedural Object-Oriented Pizza Company (P00P inc.)")
        self.master.geometry("800x600")

        tk.Label(self.master, height=2).pack()  #adding padding

        # Create left input area
        input_frame = tk.Frame(self.master, width=400, height=600)

        input_frame.pack(side="left", fill="both", expand=True)  # fill and expand added
        input_frame.grid_propagate(False)  # prevent auto resizing
        ttk.Separator(input_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=20, pady=1)
        # Create right output area
        output_frame = tk.Frame(self.master, width=600, height=600)
        output_frame.pack(side="right", fill="both", expand=True)
        output_frame.grid_propagate(False)
        self.pizza_canvas = tk.Canvas(output_frame, bg="white")
        self.current_size = (300, 300)
        self.sauce_layers = {}
        self.cheese_layers = {}
        self.seasoning_layer = {}
        self.toppings_layers = {}
        self.cheese_image = None
        self.cheese_layer = None
        self.cheese_var = tk.StringVar(value="Normal")
        self.size_var = tk.StringVar(value="New York Thin Crust")  # modified default value

        self.create_size_RBTN(input_frame)
        ttk.Separator(input_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=20, pady=1)
        self.crust_var = tk.StringVar(value="crust_nyc")
        self.create_crust_RBTN(input_frame)
        # Set default pizza crust

        ttk.Separator(input_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=20, pady=1)
        # Create sauce options

        self.sauce_var = tk.StringVar(value="Marinara")  # Set initial value to first option
        self.create_sauce_options(input_frame)

        ttk.Separator(input_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=20, pady=1)

        self.create_cheese_toppings(input_frame)
        ttk.Separator(input_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=20, pady=1)
        self.toppings_checkboxes = {}
        self.create_toppings_chkbx(input_frame)
        # Create the season checkbox
        self.seasoning_var = tk.BooleanVar()
        ttk.Separator(input_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=20, pady=1)
        self.create_seasoning_chkbx(input_frame)

        ttk.Separator(input_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=20, pady=1)
        # Create the "Build Pizza" button

        build_btn = tk.Button(input_frame, text="Build Pizza", width=30, command=self.button_pressed())  # set width to 20
        build_btn.pack(side="top", padx=20, pady=1)

        ttk.Separator(input_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=20, pady=1)

        self.pizza_canvas.pack(side="left", padx=20, pady=20)
        self.pizza_canvas.config(width=350, height=350)

        self.crust_image = Image.open(f"images/{self.crust_var.get()}.png").resize((350, 350))
        self.crust_tkimage = ImageTk.PhotoImage(self.crust_image)
        # Create the season checkbox

        self.pizza_canvas.create_image(2, 2, image=self.crust_tkimage, anchor="nw")
        self.pizza_canvas.image = self.crust_tkimage

    def set_pizza_size(self):

        size = self.size_var.get()
        if size == "Small":
            self.current_size = (300, 300)
        elif size == "Medium":
            self.current_size = (350, 350)
        elif size == "Large":
            self.current_size = (450, 450)

        self.pizza_canvas.config(width=self.current_size[0], height=self.current_size[1])
        # self.update_sauce_image()
        self.cheese_update()

        # Resize the crust image based on the pizza size
        self.crust_image = Image.open(f"images/{self.crust_var.get()}.png").resize(self.current_size)
        self.crust_tkimage = ImageTk.PhotoImage(self.crust_image)

        # Update the canvas size and crust image

        self.pizza_canvas.config(width=self.current_size[0], height=self.current_size[1])
        self.pizza_canvas.create_image(0, 0, image=self.crust_tkimage, anchor="nw")
        self.pizza_canvas.image = self.crust_tkimage

    # Define a function to update the sauce image on the pizza canvas
    def update_sauce_image(self):
        # Get the selected sauce from the sauce_var variable
        selected_sauce = self.sauce_var.get()

        # Remove all existing sauce layers from the canvas
        if "sauce" in self.sauce_layers:
            self.pizza_canvas.delete(self.sauce_layers["sauce"]["layer"])
            del self.sauce_layers["sauce"]

        # Remove all existing sauce layers from the canvas
        for layer in self.sauce_layers.values():
            self.pizza_canvas.delete(layer["layer"])

        # Remove all existing toppings layers from the canvas
        for layer in self.toppings_layers.values():
            self.pizza_canvas.delete(layer["layer"])
        # Remove all existing cheese layers from canvas
        for layer in self.cheese_layers.values():
            self.pizza_canvas.delete(layer["layer"])

        # Display the new sauce layer on the canvas
        selected_sauce_image = f"images/sauce_{selected_sauce}.png"
        sauce_image = Image.open(selected_sauce_image).resize((self.current_size[0], self.current_size[1]))
        sauce_tkimage = ImageTk.PhotoImage(sauce_image)
        self.sauce_layers[selected_sauce] = {"image": sauce_image,"tkimage":sauce_tkimage,
                                             "layer":self.pizza_canvas.create_image(0,0, image = sauce_tkimage, anchor = "nw")}


        #Redraw the toppings layers on the canvas
        for layer in self.toppings_layers.values():
            layer["layer"] = self.pizza_canvas.create_image(0, 0, image=layer["tkimage"], anchor="nw")
        # Move the sauce layer above the crust image
        self.pizza_canvas.tag_raise("sauce")
        self.pizza_canvas.tag_lower("crust")  # Move the crust image to the bottom
        # Update the toppings image

    def set_pizza_crust(self):

        crust_type = self.crust_var.get().lower().replace(' ', '_')
        self.crust_image = Image.open(f"images/{crust_type}.png").resize((self.current_size[0], self.current_size[1]))
        self.crust_tkimage = ImageTk.PhotoImage(self.crust_image)
        self.pizza_canvas.config(width=self.current_size[0], height=self.current_size[1])
        self.pizza_canvas.create_image(0, 0, anchor="nw", image=self.crust_tkimage)
        self.cheese_update()
        self.pizza_canvas.image = self.crust_tkimage
        self.pizza_canvas.tag_lower("crust")

    # Update the cheese image to match the new size
        if self.cheese_image:
            self.cheese_image = self.cheese_image.resize((self.current_size[0], self.current_size[1]))
            cheese_tkimage = ImageTk.PhotoImage(self.cheese_image)
            self.pizza_canvas.itemconfigure(self.cheese_layer, image=cheese_tkimage)
            self.pizza_canvas.tag_raise(self.cheese_layer)

    # Create a function to handle cheese selection

    def cheese_select(self, event):
        # Get the selected cheese option
        selection = event.widget.curselection()
        if selection:
            selected_cheese = event.widget.get(selection[0])
            self.cheese_var.set(selected_cheese)
        self.cheese_update()

        # Update the cheese layer when the cheese_var changes

    def cheese_update(self): #updates after user selects

        # Get the selected cheese from the cheese_var variable
        selected_cheese = self.cheese_var.get()

        # Remove all existing cheese layers from the canvas
        for layer in self.cheese_layers.values():
            self.pizza_canvas.delete(layer["layer"])

        # Display the new cheese layer on the canvas
        selected_cheese_image = f"images/cheese_{selected_cheese}.png"
        self.cheese_image = Image.open(selected_cheese_image).resize((self.current_size[0], self.current_size[1]))
        cheese_tkimage = ImageTk.PhotoImage(
            Image.open(selected_cheese_image).resize((self.current_size[0], self.current_size[1])))
        self.cheese_layer = self.pizza_canvas.create_image(0, 0, anchor="nw", image=cheese_tkimage, tags=("cheese",))
        self.cheese_layers[selected_cheese] = {"image": cheese_tkimage, "layer": self.cheese_layer}

        # Move the cheese layer above the crust image
        self.pizza_canvas.tag_raise("cheese")
        self.pizza_canvas.tag_lower("crust")

        #Move the crust image to the bottom

    def update_toppings_image(self):

        # Remove all existing toppings layers from the canvas
        for layer in self.toppings_layers.values():
            self.pizza_canvas.delete(layer["layer"])

        # Get the selected toppings from the toppings_checkboxes list
        selected_toppings = [topping for topping, var in self.toppings_checkboxes.items() if var.get()]

        # Display the new toppings layers on the canvas
        for i, topping in enumerate(selected_toppings):
            toppings_image = Image.open(f"images/topping_{topping}.png").resize(
                (self.current_size[0], self.current_size[1]))
            toppings_tkimage = ImageTk.PhotoImage(toppings_image)
            toppings_layer = self.pizza_canvas.create_image(0, 0, anchor="nw", image=toppings_tkimage,
                                                            tags=(f"topping_{i}",))
            self.toppings_layers[topping] = {"image": toppings_tkimage, "layer": toppings_layer}

        # Move the toppings layers above the sauce and crust images
        self.pizza_canvas.tag_raise("topping")
        self.pizza_canvas.tag_lower("crust")

    # Define a function to update the seasoning image on the pizza canvas
    def update_seasoning_image(self):

        # Get the value of the seasoning checkbox
        is_seasoning = self.seasoning_var.get()

        # Remove any existing seasoning layer from the canvas
        if "seasoning" in self.seasoning_layer:
            self.pizza_canvas.delete(self.seasoning_layer["seasoning"]["layer"])
            del self.seasoning_layer["seasoning"]

        # If the seasoning checkbox is checked, add a new seasoning layer to the canvas
        if is_seasoning:
            # Load the selected seasoning image
            seasoning_image = Image.open(os.path.join("images", "seasoning.png")).resize(self.current_size)
            seasoning_tkimage = ImageTk.PhotoImage(seasoning_image)

            # Create a new seasoning layer on the canvas
            self.seasoning_layer["seasoning"] = {
                "image": seasoning_tkimage,
                "layer": self.pizza_canvas.create_image(0, 0, anchor="nw", image=seasoning_tkimage, tags=("seasoning",))
            }
            # Move the seasoning layer above the crust image
            self.pizza_canvas.tag_raise("seasoning")
            self.pizza_canvas.tag_lower("crust")  # Move the crust image to the bottom

            # Update the toppings image

            self.update_toppings_image()
    def button_pressed(self):
        self.set_pizza_size()
        self.set_pizza_crust()
        self.update_sauce_image()
        self.cheese_update()
        self.update_toppings_image()
        self.update_seasoning_image()
    def create_toppings_chkbx(self,in_frame):
        # Create the checkboxes
        for var in self.toppings_checkboxes.values():
            var.trace("w", lambda *args, **kwargs: self.update_toppings_image())
        toppings_frame = tk.Frame(in_frame)
        toppings_frame.pack(side="top", anchor="w", padx=20, pady=1)
        tk.Label(toppings_frame, text=3 * "     " + "Choose YourToppings:").grid(row=0, column=0, sticky="w")
        row = 1
        column = 0
        for i, topping in enumerate(
                ["Mushroom", "Pepperoni", "Jalapeno", "Chicken", "Tomato", "Onion", "Ham", "Olive", "Pepper"]):
            var = tk.BooleanVar()
            self.toppings_checkboxes[topping] = var
            chk = tk.Checkbutton(toppings_frame, text=topping.title(), variable=var, command=self.update_toppings_image)
            chk.grid(row=row, column=column, sticky="w")
            column += 1
            if column == 2:
                row += 1
                column = 0
    def create_cheese_toppings(self,in_frame):
        # Create cheese options
        None1 = []
        cheese_options = {"None": None1, "Normal": "cheese_normal", "Extra": "cheese_extra"}

        # Create a frame for the cheese options

        cheese_frame = tk.Frame(in_frame)
        cheese_frame.pack(side="top", anchor="w", padx=20, pady=5)
        tk.Label(cheese_frame, text="Cheese:").pack(side="left")

        # Create a listbox for cheese options
        cheese_listbox = tk.Listbox(cheese_frame, selectmode="single", height=3)
        cheese_listbox.pack(side="left")

        # Bind the listbox to the cheese_select function
        cheese_listbox.bind("<<ListboxSelect>>", self.cheese_select)

        # Add cheese options to the listbox
        for cheese_name, cheese_file in cheese_options.items():
            cheese_listbox.insert(tk.END, cheese_name)

    def create_seasoning_chkbx(self,in_frame):
        seasoning_frame = tk.Frame(in_frame)
        seasoning_frame.pack(side="top", anchor="w", padx=100, pady=1)
        tk.Label(seasoning_frame, text="Seasoning:").pack(side="left")
        tk.Checkbutton(seasoning_frame, variable=self.seasoning_var, command=self.update_seasoning_image).pack(side="left")

    def create_sauce_options(self,in_frame):
        sauce_options = {"Marinara": "sauce_marinara", "Alfredo": "sauce_alfredo", "Barbeque": "sauce_barbeque",
                         "Chipotle": "sauce_chipotle"}
        sauce_frame = tk.Frame(in_frame)
        sauce_frame.pack(side="top", anchor="w", padx=20, pady=20)
        tk.Label(sauce_frame, text="Sauce:").pack(side="left")
        sauce_menu = tk.OptionMenu(sauce_frame, self.sauce_var, *sauce_options.keys(),
                                   command=lambda x: self.update_sauce_image())
        sauce_menu.pack(side="left")
    def create_crust_RBTN(self,in_frame):
        crust_frame = tk.Frame(in_frame)
        crust_frame.pack(side="top", anchor="w", padx=20, pady=20)  # anchor, padx, and pady added
        tk.Label(crust_frame, text="Choose your Crust:").pack(side="top")
        crust_thin = ttk.Radiobutton(crust_frame, text="New York Thin Crust", variable=self.crust_var,
                                     value="crust_nyc", command=self.set_pizza_crust)
        crust_thin.pack(side="left")
        crust_thick = ttk.Radiobutton(crust_frame, text="Chicago Style Deep Dish", variable=self.crust_var,
                                      value="crust_chicago", command=self.set_pizza_crust)
        # Create the pizza display

        crust_thick.pack(side="left")
    def create_size_RBTN(self,in_frame):
        # Define a variable to store the currently selected pizza size
        size_frame = tk.Frame(in_frame)
        size_frame.pack(side="top", anchor="w", padx=20, pady=20)
        tk.Label(size_frame, text="Size:").pack(side="top")

        size_small = tk.Radiobutton(size_frame, text="Small", variable=self.size_var, value="Small",
                                         command=self.set_pizza_size)
        size_small.pack(side="left")
        size_medium = tk.Radiobutton(size_frame, text="Medium", variable=self.size_var, value="Medium",
                                          command=self.set_pizza_size)
        size_medium.pack(side="left")
        size_large = tk.Radiobutton(size_frame, text="Large", variable=self.size_var, value="Large",
                                         command=self.set_pizza_size)
        size_large.pack(side="left")
        # self.crust_var = tk.StringVar(value="crust_nyc")  # changed default value to "crust_nyc"
        self.size_var.set("Small")


app = PizzaMakerGUI(master=root)
app.mainloop()


