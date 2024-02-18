import tkinter as tk

window = tk.Tk()
window.title("Virtual Assistant")

fromMessage = tk.Frame(master=window)
fromMessage.grid(row=0, column=0, columnspan=2, sticky="nsew")

scrollbar = tk.Scrollbar(master=fromMessage)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

messages = tk.Listbox(master=fromMessage, yscrollcommand=scrollbar.set)
messages.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

fromEntry = tk.Frame(master=window)
fromEntry.grid(row=1, column=0, padx=10, sticky="ew")

textInput = tk.Entry(master=fromEntry)
textInput.pack(fill=tk.BOTH, expand=True)

sendButton = tk.Button(master=window, text="send")
sendButton.grid(row=1, column=1, pady=10, sticky="ew")

window.rowconfigure(0, minsize=500, weight=1)
window.rowconfigure(1, minsize=50, weight=0)
window.columnconfigure(0, minsize=500, weight=1)
window.columnconfigure(1, minsize=250, weight=0)

window.mainloop()
