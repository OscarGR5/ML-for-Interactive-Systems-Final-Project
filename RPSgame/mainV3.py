import tkinter as tk
import threading
import keyboard
import time  
from PIL import Image, ImageTk
from pythonosc import udp_client, dispatcher, osc_server

class RockPaperScissorsGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors")
        
        # Set window size and bg colour
        width = 950 
        height = 650
        x = (root.winfo_screenwidth())//2 - (width//2)
        y = (root.winfo_screenheight())//2 - (height//2) 
        self.root.geometry("{}x{}+{}+{}".format(width, height, x, y)) # Width x Height
        self.root.configure(bg="#3b5b7a")  
        
        # Disable resizing of the window
        root.resizable(False, False) 
        
        # Add title label
        self.title_label = tk.Label(root, text="Rock Paper Scissors", font=("Arial", 36, "bold"), fg="#ecf0f1", bg="#3b5b7a")
        self.title_label.pack(side=tk.TOP, pady=20)
        
        # Add instruction label
        self.instruction_label = tk.Label(root, text="Press ENTER for next round", font=("Arial", 20), fg="#ecf0f1", bg="#3b5b7a")
        self.instruction_label.pack(side=tk.TOP, pady=5)
        
        
        # Create labels for displaying images
        self.player_label = tk.Label(root, bg="#3b5b7a", bd=5, relief=tk.SOLID)
        self.player_label.pack(side=tk.LEFT, padx=50)
        self.computer_label = tk.Label(root, bg="#3b5b7a", bd=5, relief=tk.SOLID)
        self.computer_label.pack(side=tk.RIGHT, padx=50)
        
        # Load and resize images
        self.load_images()
                      
        # # OSC client setup
        # self.osc_client = udp_client.SimpleUDPClient("127.0.0.1", 57120)  
        
        # Start listening for OSC messages
        self.listen_osc()
        
        # Flag to control input processing
        self.allow_input = False
        
        # Start the game
        self.play()

    def load_images(self):
        # Load and resize images
        original_size = (350, 350)
        resized_size = (int(original_size[0]), int(original_size[1]))

        self.images = {
            "blank": ImageTk.PhotoImage(Image.new("RGB", (original_size[0], original_size[1]), "white")), 
            "rock": ImageTk.PhotoImage(Image.open("images/rock.png").resize(resized_size)),
            "paper": ImageTk.PhotoImage(Image.open("images/paper.png").resize(resized_size)),
            "scissors": ImageTk.PhotoImage(Image.open("images/scissors.png").resize(resized_size)),
            "rock2": ImageTk.PhotoImage(Image.open("images/rock2.png").resize(resized_size)),
            "paper2": ImageTk.PhotoImage(Image.open("images/paper2.png").resize(resized_size)),
            "scissors2": ImageTk.PhotoImage(Image.open("images/scissors2.png").resize(resized_size))
        }

    def listen_osc(self):
        # Create dispatcher for OSC
        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.map("/wek/outputs", self.handle_osc)
        
        # Start OSC server
        self.server = osc_server.ThreadingOSCUDPServer(("127.0.0.1", 12000), self.dispatcher)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.start()

    def handle_osc(self, msg, *args):
        # Process OSC input if allowed
        if self.allow_input and msg == "/wek/outputs":
            choice = int(args[0])
            self.update_game_state(choice)
            self.allow_input = False  # Disable input processing until ENTER is pressed
        
    def play(self):
        # Display initial images
        self.player_label.config(image=self.images["rock"])
        self.computer_label.config(image=self.images["rock2"])
        
        # Listen for ENTER key press to allow input processing
        keyboard.on_press_key("enter", self.allow_next_input)

    def allow_next_input(self, event):
        # Allow the next OSC input to come through when ENTER is pressed
        self.allow_input = True

    # Computer response + update images
    def update_game_state(self, player_choice):
        # Map player choice to corresponding image
        player_image = self.images[self.get_image_name(player_choice, "p")]
        
        # Display player choice
        self.player_label.config(image=player_image)
        
        # Select computer's choice    
        computer_choice = None
        if player_choice == 1:
            computer_choice = 2
        elif player_choice == 2:
            computer_choice = 3
        elif player_choice == 3:
            computer_choice = 1
                
        # Blank out the computer's image first
        self.computer_label.config(image=self.images["blank"])
        self.root.update()  # Force update to display the blank image
        
        # Slight delay before updating computer's choice
        time.sleep(0.1) 
        
        # Map computer's choice to corresponding image
        computer_image = self.images[self.get_image_name(computer_choice, "c")]

        # Display computer choice
        self.computer_label.config(image=computer_image) 
     

    # Update image   
    def get_image_name(self, choice, player):
        image_names = {
            "p": {1: "rock", 2: "paper", 3: "scissors"},
            "c": {1: "rock2", 2: "paper2", 3: "scissors2"}
        }
        default_choice = {"p": "rock", "c": "rock2"}

        return image_names.get(player, {}).get(choice, default_choice.get(player, "rock"))
      
if __name__ == "__main__":
    def on_closing(): # Used to kill all processes after closing tkinter window
        print("closing")
        # Stop the OSC server by calling its shutdown method
        game.server.shutdown()
        # Wait for the OSC server thread to finish
        game.server_thread.join()
        # Close the Tkinter window
        root.destroy()

    root = tk.Tk()
    root.title("Rock Paper Scissors")
    root.configure(bg="#3b5b7a")  # Background color
    game = RockPaperScissorsGame(root)
    root.protocol("WM_DELETE_WINDOW", on_closing) 
    root.mainloop()
