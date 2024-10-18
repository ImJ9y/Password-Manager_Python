import json
from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# global confirmWindow
#----------------------------- POP UP SCREEN --------------------------------------#
# def confirm():
#     global confirmWindow
#     confirmWindow = Tk()
#     confirmWindow.title("Confirm")
#     confirm_label = Label(confirmWindow, text="Do you want to add this?")
#     confirm_label.pack()
#     B1 = Button(confirmWindow, text="Yes", command=save)
#     B1.pack()
#     B2 = Button(confirmWindow, text="No", command=confirmWindow.destroy)
#     B2.pack()
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    random_letters = [random.choice(letters) for _ in range(nr_letters)]
    random_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    random_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = random_letters + random_symbols + random_numbers

    random.shuffle(password_list)

    password = "".join(password_list)
        # for char in password_list:
        #     password += char

    password_input.insert(0, password)
    pyperclip.copy(password)
    print(f"Your password is: {password}")

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    # global confirmWindow
    # confirmWindow.withdraw()
    website = website_input.get()
    email = email_or_username_input.get()
    password = password_input.get()

    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website_input.get()) == 0 or len(email_or_username_input.get()) == 0 or len(password_input.get()) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        confirm = messagebox.askokcancel(title= website,
                                         message=f"These are the details entered:\n Email: {email}\nPassowrd: {password}\n Is it Okay to save?")
        if confirm:
            try:
                with open("data.json", "r") as file:
                    # Read old data
                    data = json.load(file)
            except FileNotFoundError:
                with open("data.json", "w") as file:
                    # create a new data
                    json.dump(new_data, file, indent=4)
            else:
                # Updating old data
                data.update(new_data)

                with open("data.json", "w") as file:
                    # Saving updated data
                    json.dump(data, file, indent=4)
            finally:
                website_input.delete(0, END)
                password_input.delete(0, END)

        else:
            website_input.delete(0, END)
            password_input.delete(0,END)

# ---------------------------- Search Engine ------------------------------- #
def search_website():
    website = website_input.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]['email']
            password = data[website]['password']
            messagebox.showinfo(title=website, message=f"Email: {email}\n Password: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image = logo_image)
canvas.grid(column = 1, row = 0) #grid and pack can't use together
# X.grid(row=2, column =0, columnspan = 2) #Expand the label

#WebSite Label
website_label=Label(text = "Website:")
website_label.grid(column = 0, row=1)
#Email/Username Label
email_or_username_label=Label(text = "Email/Uesrname:")
email_or_username_label.grid(column = 0, row=2)
#Password Label
password_label=Label(text = "Password:")
password_label.grid(column = 0, row=3)

#WebSite Input
website_input = Entry(width=35)
website_input.grid(column= 1, row = 1, columnspan = 2)
#Email/Username Input
email_or_username_input = Entry(width=35)
email_or_username_input.grid(column= 1, row = 2, columnspan = 2)
email_or_username_input.insert(0, "dummy@gmail.com")
#Password Input
password_input = Entry(width=35)
password_input.grid(column=1, row=3, columnspan = 2)


#Search Button
search_button = Button(text= "Search", width= 10, command = search_website)
search_button.grid(column = 2, row = 1, columnspan = 2)

#Generate Password Button
generate_password_button = Button(text= "Generate Password", width=10, command=generate_password)
generate_password_button.grid(column = 2, row = 3, columnspan = 2)

#Add Button
add_button = Button(text= "Add", width= 33, command = save)
add_button.grid(column = 1, row = 4, columnspan = 2)

window.mainloop()
