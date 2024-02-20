import tkinter as tk
import json
from difflib import get_close_matches

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
textInput.insert(0, "Writte your message here")

def send_message(event=None):
    knowledge = load_knowledge_base('knowledge_base.json')
    while True:
        text = textInput.get()
        if text.lower() == 'quit':
            break
        else:
            messages.insert(tk.END, f"You: {text}")
        best_match = find_best_match(text, [q["question"] for q in knowledge["questions"]])

        if best_match:
            answer = get_answer_for_question(best_match, knowledge)
            messages.insert(tk.END, f"Bot: {answer}")

        elif text.lower().startswith('learn: '):
            qia = text[7:]
            new_question, new_answer = qia.split("-", 1)
            knowledge["questions"].append({"question": new_question.strip(), "answer": new_answer.strip()})
            save_knowledge_base('knowledge_base.json', knowledge)
            messages.insert(tk.END, f"Bot: Thank you for learning me")
        elif text.lower().startswith('change: '):
            qia = text[8:]
            question, new_answer = qia.split("-", 1)
            for q in knowledge["questions"]:
                if q["question"] == question:
                    found_question = q
                    found_question["answer"] = new_answer.strip()
                    save_knowledge_base('knowledge_base.json', knowledge)
                    messages.insert(tk.END, f"Bot: Answer is changed")
            if question not in knowledge["questions"]:
                messages.insert(tk.END, f"Bot: Cant change that answer")




        elif text.lower() == "quit":
            break
        else:
            messages.insert(tk.END, f"Bot: I don't know answer, please teach me with 'Learn: question-answer'")
        textInput.delete(0, tk.END)

        break

sendButton = (tk.Button(master=window, text="send", command=send_message))
textInput.bind("<Return>", send_message)
sendButton.grid(row=1, column=1, pady=10, sticky="ew")

window.rowconfigure(0, minsize=500, weight=1)
window.rowconfigure(1, minsize=50, weight=0)
window.columnconfigure(0, minsize=500, weight=1)
window.columnconfigure(1, minsize=250, weight=0)

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


window.mainloop()
