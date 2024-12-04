import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3
import matplotlib.pyplot as plt
from auth import check_credentials 
from pro1 import get_news, get_dynamic_values

root =tk.Tk()
root.title("FIRE_NEWS_")
root.geometry("950x550+50+50")
img = Image.open("firepic.ico")
root.iconphoto(True, ImageTk.PhotoImage(img))
root.configure(bg="#f0f8ff") 

#functions
def clear_data():
    entr_name.delete(0,tk.END)
    entr_password.delete(0,tk.END)

def store_db():
    try:
        con = sqlite3.connect("Login.db")
        c = con.cursor()
        # Insert into database
        c.execute("INSERT INTO login VALUES(:name_temp, :password_temp)", 
                  { 
                      "name_temp": entr_name.get(),
                      "password_temp": entr_password.get()
                  })
        con.commit()
        print("Data inserted successfully.")
    except sqlite3.Error as e:
        print(f"Error occurred: {e}")
    finally:
        con.close()


def show_db():
    con=sqlite3.connect("Login.db")
#create cursor
    c=con.cursor()
    c.execute("SELECT * FROM login")
    returner=c.fetchall()
    print(returner)

    con.commit()

#close the program
    con.close()


#no of times login
click_count = 0
def no_clicker():
    global click_count
    click_count += 1
    #store_db()
    clear_data()


def check_credentials_and_redirect():
    name = entr_name.get()
    password = entr_password.get()

    if check_credentials(name, password):  # Check credentials using auth.py
        update_message("Logged in successfully!", "green")
        root.after(5000, lambda: update_message("", "black"))  # Clear message after 5 seconds
        open_dashboard(name)  # Open the dashboard with the user's name
    else:
        update_message("Invalid credentials!", "red")
        root.after(5000, lambda: update_message("", "black"))  # Clear message after 5 seconds

def open_dashboard(username):
    """Opens the dashboard window upon successful login."""
    # Create a new Toplevel window for the dashboard
    dashboard_window = tk.Toplevel(root)
    dashboard_window.title("FIRE_NEWS_MAIN")
    dashboard_window.geometry("950x550+50+50")
    dashboard_window.configure(bg="#f0f0f5")  # Light gray background
    clear_data()
    # Add a welcome message
    label = tk.Label(
        dashboard_window,
        text=f"Welcome {username}",
        font=("Arial", 24, "bold"),
        fg="#2e86c1",
        bg="#f0f0f5",
    )
    label.pack(pady=10)

    # Frames for sections
    frame1 = tk.Frame(dashboard_window, bd=3, relief="groove", bg="#ffffff")
    frame1.place(x=15, y=100, width=900, height=60)

    frame2 = tk.Frame(dashboard_window, bd=3, relief="groove", bg="#ffffff")
    frame2.place(x=15, y=180, width=900, height=60)

    frame3 = tk.Frame(dashboard_window, bd=3, relief="groove", bg="#ffffff")
    frame3.place(x=15, y=260, width=900, height=60)

    result_frame = tk.Frame(dashboard_window, bd=3, relief="sunken", bg="#ffffff")
    result_frame.place(x=15, y=340, width=900, height=180)

    btn_logout = tk.Button(
        dashboard_window,
        text="Logout",
        font=("Arial", 12, "bold"),
        bg="#ff4d4d",
        fg="white",
        activebackground="#cc0000",
        activeforeground="white",
        cursor="hand2",
        command=lambda: (dashboard_window.destroy(), root.deiconify()),  # Close dashboard and show main window
    )
    btn_logout.place(x=820, y=10, width=100, height=40)

    # Frame 1 - Filter Popularity
    tk.Label(
        frame1,
        text="Filter Popularity:",
        font=("Arial", 12, "bold"),
        bg="#ffffff",
        fg="#333333",
    ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

    combo_popularity = ttk.Combobox(
        frame1, state="readonly", width=20, font=("Arial", 10)
    )
    combo_popularity["values"] = ("everything", "top-headlines")
    combo_popularity.current(0)
    combo_popularity.grid(row=0, column=1, padx=10, pady=10)

    # Frame 2 - Filter Sources
    tk.Label(
        frame2,
        text="Filter Sources By:",
        font=("Arial", 12, "bold"),
        bg="#ffffff",
        fg="#333333",
    ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

    combo_filter = ttk.Combobox(frame2, state="readonly", width=20, font=("Arial", 10))
    combo_filter["values"] = ("language", "country", "category")
    combo_filter.current(0)
    combo_filter.grid(row=0, column=1, padx=10, pady=10)

    combo_filter.bind("<<ComboboxSelected>>", lambda _: update_dynamic_options())

    # Frame 3 - Dynamic Filter Options and Fetch Button
    tk.Label(
        frame3,
        text="Dynamic Filter:",
        font=("Arial", 12, "bold"),
        bg="#ffffff",
        fg="#333333",
    ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

    combo_dynamic = ttk.Combobox(frame3, state="readonly", width=30, font=("Arial", 10))
    combo_dynamic.grid(row=0, column=1, padx=10, pady=10)

    def update_dynamic_options():
        """Update options in the dynamic combobox based on the filter."""
        selected_filter = combo_filter.get()
        combo_dynamic["values"] = get_dynamic_values(selected_filter)
        combo_dynamic.current(0)

    update_dynamic_options()

    btn_fetch = tk.Button(
        frame3,
        text="Fetch News",
        font=("Arial", 12, "bold"),
        bg="#2e86c1",
        fg="white",
        activebackground="#1a5276",
        activeforeground="white",
        command=lambda: save_and_fetch(),
    )
    btn_fetch.grid(row=0, column=2, padx=20, pady=10)

    # Result Textbox
    tk.Label(
        result_frame,
        text="News Results:",
        font=("Arial", 12, "bold"),
        bg="#ffffff",
        fg="#333333",
    ).pack(anchor="w", padx=10, pady=5)

    result_text = tk.Text(
        result_frame,
        wrap="word",
        height=8,
        width=105,
        font=("Arial", 10),
        bg="#f8f9fa",
        fg="#333333",
        bd=2,
        relief="solid",
    )
    result_text.pack(padx=10, pady=5)

    def save_and_fetch():
        """Save selections and fetch news."""
        selected_popularity = combo_popularity.get()
        selected_filter = combo_filter.get()
        filter_value = combo_dynamic.get()
        articles = get_news(selected_popularity, selected_filter, filter_value)

        result_text.delete(1.0, tk.END)  # Clear previous results
        if articles:
            for article in articles:
                result_text.insert(
                    tk.END, article["title"] + "\n" + "-" * 80 + "\n\n"
                )
        else:
            result_text.insert(tk.END, "Failed to fetch news.\n")


def update_message(message, color):
    """Update the message label with the provided text and color."""
    lab6=tk.Label(scnd_frame,text=message, fg=color,font=(12))
    lab6.grid(row=5,column=3)


#matplotlib graphs
def grapher():
    plt.hist(click_count)
    plt.show()
# Welcome Label
labl = tk.Label(
    root,
    text="Welcome to News Fire",
    font=("Broadway", 36, "bold"),
    bg="white",
    fg="grey",
    cursor="hand2",
    bd=3,
    relief="raised",
)
labl.pack(side="top", pady=10)

# Frame for the tagline
frst_frame = tk.Frame(root, bg="#f8f9fa", bd=2, relief="ridge")
frst_frame.place(x=140, y=80, width=681, height=60)

# Tagline Label
lab2 = tk.Label(
    frst_frame,
    text=""" "Stay Updated Wherever You Are" """,
    font=("Broadway", 26, "italic"),
    fg="darkblue",
    bg="lightblue",
)
lab2.grid(row=0, column=0, padx=10, pady=5)

# Frame for the login form
scnd_frame = tk.Frame(root, bg="#ffffff", bd=3, relief="sunken")
scnd_frame.place(x=16, y=150, width=920, height=310)

# Login Form Header
lab3 = tk.Label(
    scnd_frame,
    text="Login to Your Account",
    font=("Calibri", 18, "bold"),
    fg="black",
    bg="lightgrey",
)
lab3.grid(row=0, column=1, columnspan=2, pady=20)

# Labels for Name and Password
lab4 = tk.Label(
    scnd_frame, text="Name: ", font=("Calibri", 14, "bold"), fg="black", bg="lightblue"
)
lab4.grid(row=1, column=0, padx=10, pady=10, sticky="w")

lab5 = tk.Label(
    scnd_frame,
    text="Password: ",
    font=("Calibri", 14, "bold"),
    fg="black",
    bg="lightblue",
)
lab5.grid(row=2, column=0, padx=10, pady=10, sticky="w")

# Variables for Entry Fields
name_var = tk.StringVar()
email_var = tk.StringVar()

# Entry Fields
entr_name = tk.Entry(scnd_frame, textvariable=name_var, width=30, bd=3, font=("Arial", 12))
entr_name.grid(row=1, column=1, padx=10, pady=10)

entr_password = tk.Entry(scnd_frame, textvariable=email_var, show="*", width=30, bd=3, font=("Arial", 12))
entr_password.grid(row=2, column=1, padx=10, pady=10)

# Buttons Styling
def on_enter(e):
    e.widget.config(bg="#1e90ff")  # Hover color


def on_leave(e):
    e.widget.config(bg="#4CAF50")  # Default color


# Log In Button
btn = tk.Button(
    scnd_frame,
    text="Log In",
    command=check_credentials_and_redirect,
    font=("Arial", 14, "bold"),
    bg="#4CAF50",
    fg="white",
    relief="solid",
    cursor="hand2",
    width=12,
)
btn.grid(row=3, column=1, pady=20)
btn.bind("<Enter>", on_enter)
btn.bind("<Leave>", on_leave)

# Additional Buttons
btn1 = tk.Button(
    root,
    text="Show Records",
    font=("Arial", 12, "bold"),
    bg="#ff8c00",
    fg="white",
    relief="solid",
    cursor="hand2",
    command=show_db,
)
btn1.place(x=15, y=480, width=180, height=40)

btn2 = tk.Button(
    root,
    text="Visitors",
    font=("Arial", 12, "bold"),
    bg="#ff8c00",
    fg="white",
    relief="solid",
    cursor="hand2",
    command=grapher,
)
btn2.place(x=210, y=480, width=180, height=40)

# Footer
lab6 = tk.Label(
    root,
    text="FIRE_NEWS - Stay Informed, Stay Ahead",
    font=("Helvetica", 13, "italic"),
    fg="darkblue",
    bg="#f0f8ff",
)
lab6.place(x=600,y=520)
#connecting the database
con=sqlite3.connect("Login.db")
#create cursor
c=con.cursor()
#create table
# c.execute("""
# CREATE TABLE login (
#           name text,
#           password text NOT NULL
# )
# """)
#commit the changes
con.commit()

#close the program
con.close()

root.mainloop()