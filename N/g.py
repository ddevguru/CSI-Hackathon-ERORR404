import tkinter as tk
from tkinter import messagebox
import random

quiz_data = [
    {
        "question": "What does HTML stand for?",
        "options": ["Hyper Text Markup Language", "Hyperlinks and Text Markup Language", "Home Tool Markup Language", "Hyper Tool Markup Language"],
        "answer": "Hyper Text Markup Language"
    },
    {
        "question": "What is the purpose of CSS?",
        "options": ["To define the structure of web pages", "To style the web pages", "To create animations", "To store data"],
        "answer": "To style the web pages"
    },
    {
        "question": "Which SQL command is used to retrieve data from a database?",
        "options": ["INSERT", "UPDATE", "SELECT", "DELETE"],
        "answer": "SELECT"
    },
    {
        "question": "Which tag is used to create a hyperlink in HTML?",
        "options": ["<link>", "<a>", "<href>", "<anchor>"],
        "answer": "<a>"
    },
    {
        "question": "How do you comment out code in CSS?",
        "options": ["// Comment", "# Comment", "/* Comment */", "<!-- Comment -->"],
        "answer": "/* Comment */"
    },
    {
        "question": "What SQL keyword is used to sort the result-set?",
        "options": ["ORDER BY", "SORT", "ALIGN", "GROUP BY"],
        "answer": "ORDER BY"
    },
    {
        "question": "True or False: CSS is used to structure web pages.",
        "options": ["True", "False"],
        "answer": "False"
    },
    {
        "question": "Which CSS property is used to change the background color?",
        "options": ["background-color", "color", "bgcolor", "background"],
        "answer": "background-color"
    },
    {
        "question": "In HTML, which tag is used to define an unordered list?",
        "options": ["<ol>", "<ul>", "<li>", "<list>"],
        "answer": "<ul>"
    },
    {
        "question": "What does SQL stand for?",
        "options": ["Structured Query Language", "Stylized Query Language", "Simplified Query Language", "Sequential Query Language"],
        "answer": "Structured Query Language"
    },
    {
        "question": "Which attribute is used to provide a unique identifier for an HTML element?",
        "options": ["class", "id", "name", "key"],
        "answer": "id"
    },
    {
        "question": "Which of the following CSS properties controls the text size?",
        "options": ["font-style", "text-size", "font-size", "text-style"],
        "answer": "font-size"
    },
    {
        "question": "Which HTML tag is used to define a table row?",
        "options": ["<th>", "<tr>", "<td>", "<table>"],
        "answer": "<tr>"
    },
    {
        "question": "Which SQL clause is used to filter records?",
        "options": ["WHERE", "FROM", "ORDER BY", "FILTER"],
        "answer": "WHERE"
    },
    {
        "question": "How do you make text bold in HTML?",
        "options": ["<strong>", "<bold>", "<b>", "<em>"],
        "answer": "<b>"
    },
    {
        "question": "Which CSS property is used to control the spacing between elements?",
        "options": ["margin", "padding", "spacing", "border"],
        "answer": "margin"
    },
    {
        "question": "Which SQL statement is used to insert new data in a database?",
        "options": ["INSERT INTO", "ADD", "INSERT NEW", "ADD DATA"],
        "answer": "INSERT INTO"
    },
    {
        "question": "Which CSS property is used to align text to the center?",
        "options": ["align", "text-align", "center-text", "text-style"],
        "answer": "text-align"
    },
    {
        "question": "Which HTML attribute is used to specify the path to an image?",
        "options": ["src", "href", "path", "alt"],
        "answer": "src"
    },
    {
        "question": "What is the correct syntax to link an external CSS file in HTML?",
        "options": ["<link href='style.css'>", "<stylesheet>style.css</stylesheet>", "<css src='style.css'>", "<link rel='stylesheet' href='style.css'>"],
        "answer": "<link rel='stylesheet' href='style.css'>"
    },
    {
        "question": "Which SQL function is used to return the number of rows in a table?",
        "options": ["COUNT()", "SUM()", "TOTAL()", "MAX()"],
        "answer": "COUNT()"
    },
    {
        "question": "Which HTML tag is used to display a horizontal line?",
        "options": ["<hr>", "<line>", "<br>", "<divider>"],
        "answer": "<hr>"
    },
    {
        "question": "Which SQL statement is used to delete data from a table?",
        "options": ["REMOVE", "DELETE", "DROP", "CUT"],
        "answer": "DELETE"
    },
    {
        "question": "How do you select elements with the class name 'container' in CSS?",
        "options": ["#container", ".container", "container", "*container"],
        "answer": ".container"
    },
    {
        "question": "Which SQL statement is used to update data in a table?",
        "options": ["MODIFY", "UPDATE", "CHANGE", "SET"],
        "answer": "UPDATE"
    }
]
random.shuffle(quiz_data)

score = 0
current_question = 0

def load_next_question():
    global current_question
    if current_question < len(quiz_data):
        question_label.config(text=quiz_data[current_question]["question"])
        for i, option in enumerate(quiz_data[current_question]["options"]):
            option_buttons[i].config(text=option)
    else:
        messagebox.showinfo("Quiz Completed", f"Your final score is: {score}/{len(quiz_data)}")
        root.quit()

def check_answer(selected_option):
    global score, current_question
    correct_answer = quiz_data[current_question]["answer"]
    
    if selected_option == correct_answer:
        score += 1
        feedback_label.config(text="Correct!", fg="green")
    else:
        feedback_label.config(text=f"Wrong! Correct answer: {correct_answer}", fg="red")
    
    current_question += 1
    root.after(1000, load_next_question)

root = tk.Tk()
root.title("HTML, CSS, SQL Quiz Game")
root.geometry("400x300")

question_label = tk.Label(root, text="", font=("Arial", 14), wraplength=350)
question_label.pack(pady=20)

option_buttons = []
for i in range(4):
    btn = tk.Button(root, text="", font=("Arial", 12), width=40, command=lambda i=i: check_answer(option_buttons[i].cget("text")))
    btn.pack(pady=5)
    option_buttons.append(btn)

feedback_label = tk.Label(root, text="", font=("Arial", 12))
feedback_label.pack(pady=20)

load_next_question()

root.mainloop()
