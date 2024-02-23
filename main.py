import tkinter as tk
from tkinter import ttk
import json
from difflib import get_close_matches

JSON_FILE = 'json_file'


def load_knowledge_base(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        if data:
            return data
        else:
            return None


def save_knowledge_base(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


def find_best_match(user_question, questions):
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None


def get_answer_for_question(question, knowledge_base):
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]


# App GUI
window = tk.Tk()
style = ttk.Style()
font_style = ("Helvetica", 10)
window.title("Virtual Assistant")
window.configure(bg="#f0f0f0")

fromMessage = tk.Frame(master=window)
fromMessage.grid(row=0, column=0, columnspan=2, sticky="nsew")

scrollbar = tk.Scrollbar(master=fromMessage)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

messages = tk.Listbox(master=fromMessage, yscrollcommand=scrollbar.set)
messages.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
messages.configure(bg="#CCE5FF", fg="#000000", font=font_style)

fromEntry = tk.Frame(master=window)
fromEntry.grid(row=1, column=0, padx=10, sticky="ew")

textInput = tk.Entry(master=fromEntry)
textInput.pack(fill=tk.BOTH, expand=True)
textInput.configure(font=font_style)
textInput.insert(0, "Write your message here")


def send_message(event=None):
    knowledge = load_knowledge_base(JSON_FILE)

    text = textInput.get()
    if text.lower() == 'quit':
        window.destroy()
    else:
        messages.insert(tk.END, f"You: {text}", )
        best_match = find_best_match(text, [q["question"] for q in knowledge["questions"]])

        if best_match:
            answer = get_answer_for_question(best_match, knowledge)
            messages.configure(bg="#CCE5FF", fg="#000000", font=font_style)
            messages.insert(tk.END, f"Bot: {answer}")
        # Learn a bot new answers
        elif text.lower().startswith('learn: '):
            qia = text[7:]
            new_question, new_answer = qia.split("-", 1)
            knowledge["questions"].append({"question": new_question.strip(), "answer": new_answer.strip()})
            save_knowledge_base(JSON_FILE, knowledge)
            messages.insert(tk.END, f"Bot: Thank you for teaching me a new answer,"
                                    f" you can change it with 'Change: Question-New answer'")

        # Change answer that already exist
        elif text.lower().startswith('change: '):
            qia = text[8:]
            question, new_answer = qia.split("-", 1)
            for q in knowledge["questions"]:
                if q["question"] == question:
                    found_question = q
                    found_question["answer"] = new_answer.strip()
                    save_knowledge_base(JSON_FILE, knowledge)
                    messages.insert(tk.END, f"Bot: The answer has been changed")
            if not any(q["question"] == question for q in knowledge["questions"]):
                messages.insert(tk.END, f"Bot: I Can't change that answer, answer doesn't exist")

        else:
            messages.insert(tk.END, f"Bot: I don't know answer, please teach me with 'Learn: Question-Answer'")
        textInput.delete(0, tk.END)


sendButton = (tk.Button(master=window, text="Send", command=send_message))
textInput.bind("<Return>", send_message)
sendButton.grid(row=1, column=1, pady=10, sticky="ew")
sendButton.configure(bg="#CCE5FF", fg="#000000", font=font_style)

window.rowconfigure(0, minsize=500, weight=1)
window.rowconfigure(1, minsize=50, weight=0)
window.columnconfigure(0, minsize=500, weight=1)
window.columnconfigure(1, minsize=250, weight=0)

window.mainloop()
