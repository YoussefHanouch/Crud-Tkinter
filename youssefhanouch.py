from pymongo import MongoClient
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk

client = MongoClient('mongodb://localhost:27017/')
db=client['efm']
collection = db['PR']

root = tk.Tk()
root.title("gérer les prouduit")
root.geometry("1000x400")


def add_item():
    item = {
        "id": entry_id.get(),
        "name": entry_name.get(),
        "price": entry_price.get(),
        "quantity": entry_quantity.get()
    }
   
    collection.insert_one(item)
    refresh_table()
    messagebox.showinfo("Success", "Item added successfully!")
   
def update_item():
    selected_item = tree.focus()
    if selected_item:
        item_id = str(tree.item(selected_item)['values'][0])
        item = {
        "id": entry_id.get(),
        "name": entry_name.get(),
        "price": entry_price.get(),
        "quantity": entry_quantity.get()
        }
        collection.update_one({"id": item_id}, {"$set":item})
        messagebox.showinfo("Success", "Item updated successfully!")
        refresh_table()
    else:
        messagebox.showerror("Error", "No item selected")

# Function to delete an item
def delete_item():
    selected_item = tree.focus()
    if selected_item:
        item_id = str(tree.item(selected_item)['values'][0])
        collection.delete_one({"id": item_id})
        refresh_table()
        messagebox.showinfo("Success", "Item deleted successfully!")
    else:
        messagebox.showerror("Error", "No item selected")

# show item
def show_item():
    selected_item = tree.focus()
    if selected_item:
        item_id = str(tree.item(selected_item)['values'][0])
        vr = collection.find_one({"id": item_id})

        entry_id.delete(0, END)
        entry_name.delete(0, END)
        entry_price.delete(0, END)
        entry_quantity.delete(0, END)

        entry_id.insert(0, vr["id"])
        entry_name.insert(1, vr["name"])
        entry_price.insert(2, vr["price"])
        entry_quantity.insert(3, vr["quantity"])
        
# Function to refresh the table
def refresh_table():
    for item in tree.get_children():
        tree.delete(item)

    items = collection.find()
    for item in items:
        tree.insert(parent='', index='end', iid=item["_id"], text="", values=(item["id"], item["name"], item["price"], item["quantity"]))

menu_barre = tk.Menu(root)

# Création du menu "Fichier"
menu_barre = tk.Menu(menu_barre, tearoff=0)
menu_barre.add_command(label="Quitter", command=root.quit)

root.config(menu=menu_barre)
# Form Elements
title=Label(root,text='formulaire Pour ajouter  Produit',font="calibre 20 bold")
title.grid(row=0,column=2, pady=10, columnspan=4)
label_id = Label(root, text="ID:")
label_name = Label(root, text="Name:")
label_price = Label(root, text="Price:")
label_quantity = Label(root, text="Quantity:")

entry_id = Entry(root)
entry_name = Entry(root)
entry_price = Entry(root)
entry_quantity = Entry(root)

button_add = Button(root, text="ajouter", command=add_item,width=12,font=("Arial",10),bg="green",fg="white")
button_update = Button(root, text="Mis a jour", command=update_item,width=12,font=("Arial",10),bg="blue",fg="white")
button_delete = Button(root, text="supprimmer", command=delete_item,width=12,font=("Arial",10),bg="red",fg="white")
button_show = Button(root, text="afficher", command=show_item,width=12,font=("Arial",10),bg="#7000ff",fg="white")

label_id.grid(row=5, column=0, padx=5, pady=5)
label_name.grid(row=6, column=0, padx=5, pady=5)
label_price.grid(row=7, column=0, padx=5, pady=5)
label_quantity.grid(row=8, column=0, padx=5, pady=5)

entry_id.grid(row=5, column=1, padx=5, pady=5)
entry_name.grid(row=6, column=1, padx=5, pady=5)
entry_price.grid(row=7, column=1, padx=5, pady=5)
entry_quantity.grid(row=8, column=1, padx=5, pady=5)

button_add.grid(row=9, column=0, columnspan=2, padx=5, pady=5)
button_update.grid(row=10, column=0, columnspan=2, padx=5, pady=5)
button_delete.grid(row=11,column=0, columnspan=2, padx=5, pady=5)
button_show.grid(row=12,column=0, columnspan=2, padx=5, pady=5)

tree = ttk.Treeview(root)
tree['columns'] = ("ID", "Name", "Price", "Quantity")
tree.column("#0", width=0, stretch=NO)
tree.column("ID", anchor=W, width=100)
tree.column("Name", anchor=W, width=200)
tree.column("Price", anchor=W, width=150)
tree.column("Quantity", anchor=W, width=150)
tree.heading("ID", text="ID", anchor=W)
tree.heading("Name", text="Name", anchor=W)
tree.heading("Price", text="Price", anchor=W)
tree.heading("Quantity", text="Quantity", anchor=W)
tree.grid(row=5, column=2 , rowspan=7, padx=10, pady=10)

refresh_table()

root.mainloop()
