from tkinter import *
import time
from tkinter.ttk import Combobox


def main():
    global keys, wind, stack, start, i, entry_text, call, num, correct, tim, second, frame
    wind = Tk()
    wind.geometry("1200x600")
    wind.title("Typing Speed Calulator")
    wind.config(bg="light green")
    frame = Frame(wind, bg="light green")
    speed_func(frame)
    accuracy_func(frame)
    time_func(frame)
    second = 60
    correct = 0
    keys = "qwertyuiopasdfghjklzxcvbnm()',.234567890"
    keys += keys.upper()
    story_text = story(frame)
    start = True
    i = 0
    stack = []
    entry_text = ""
    for j in keys:
        story_text.bind(f"<{j}>", TEXT)
    story_text.bind("<space>", TEXT)
    story_text.bind("<BackSpace>", backspace)
    story_text.tag_add("0", 1.0)
    story_text.tag_config("0", underline=True)
    tim = 60
    call = False
    num = 0
    story_text.bind("<Button-1>", cursor_call)
    frame.place(x=20, y=40)

    wind.mainloop()
    return frame


def story(frame):
    with open("story1.txt") as file:
        global story1, story_text
        story1 = file.read()
        story_text = Text(
            frame, width=105, height=17, font=("Courier", "14"), wrap=WORD
        )
        story_text.grid(row=2, columnspan=3, pady=30)
        story_text.insert("1.0", story1)
        story_text.config(state="disabled")
        return story_text


def begin():
    global before
    if start:
        before = time.time()
        timer()


def timer():
    global tim, root
    tim -= 1
    min = "{:02}".format(tim // 60)
    sec = "{:02}".format(tim % 60)
    label.config(text=f"{min}:{sec}")
    if tim != 0:
        label.after(1000, timer)
    else:
        for j in keys:
            story_text.unbind(sequence=f"<{j}>")
        story_text.unbind(sequence="<BackSpace>")
        story_text.unbind(sequence="<space>")
        story_text.tag_config(str(i), underline=False)
        new_window()


def new_window():
    result = Tk()
    result.title("Result")
    result.geometry("1000x500")
    frame_result = Frame(result, width=160)
    Label(frame_result, text="Result", font=("bold", 60), fg="lime", bg="orange").grid(
        padx=200, pady=60, columnspan=3
    )
    speed_func(frame_result)
    speed_box.grid_configure(column=0, row=1)
    speed_display.config(
        text=f"{int(accurate * len(entry_text.split())/((second/60)))} AWPM"
    )
    accuracy_func(frame_result)
    accuracy_box.grid_configure(column=2, row=1)
    accuracy_display.config(text=accu_percent)

    def destry():
        wind.destroy()
        result.destroy()

    Button(frame_result, text="Exit", command=destry).grid(columnspan=3, row=2, pady=15)
    frame_result.place(x=100, y=20)
    result.mainloop()


def TEXT(event):
    global i, story_text, entry_text, correct
    story_text.tag_add(str(i), f"1.0+{i}c")
    story_text.tag_add(str(i + 1), f"1.0+{i+1}c")
    key = event.char
    stack.append(key)
    entry_text = "".join(stack)
    if key == story1[i]:
        correct += 1
        story_text.tag_config(
            str(i), background="light green", underline=True, underlinefg="green"
        )
    else:
        story_text.tag_config(
            str(i), background="pink", underline=True, underlinefg="red"
        )
    story_text.tag_config(str(i + 1), underline=True)
    accuracy(correct)
    i += 1

    if len(stack) == 1:
        begin()
        choice.config(state="disable")

    elif len(stack) > 1:
        global start
        start = False
    speed_test()


def cursor_call(label):
    global call
    call = True
    cursor()


def cursor():
    global num
    if tim != 0:
        story_text.unbind(sequence="<Button-1>")
        if num % 2 == 0:
            story_text.tag_config(str(i), underline=True, underlinefg="Black")
        else:
            story_text.tag_config(str(i), underlinefg="Grey")
        num += 1
        story_text.after(500, cursor)
    else:
        story_text.tag_config(str(i), underline=False)


def accuracy(correct):
    global accurate, accu_percent
    accurate = correct / len(stack)
    accu_percent = f"{int(accurate*100)}%"
    accuracy_display.config(text=accu_percent)


def backspace(entry):
    global correct, i, entry_text, tim
    if i > 0:
        i -= 1
        if correct > 0:
            if stack[-1] == story1[len(stack) - 1]:
                correct -= 1
                
        stack.pop()
        entry_text = "".join(stack)
        speed_test()
        story_text.tag_config(str(i), background="white", underlinefg="Black")
        story_text.tag_config(str(i + 1), underline=False)


def Selected_time(entry):
    global second, tim
    minutes = choice.get()
    if minutes == "1 minute":
        label.config(text="01:00")
        tim = second = 60

    elif minutes == "2 minutes":
        label.config(text="02:00")
        tim = second = 120
    elif minutes == "30 seconds":
        label.config(text="00:30")
        tim = second = 30


def speed_test():
    global speed
    speed = int(accurate * len(entry_text.split()) / ((second - tim) / 60))
    speed_display.config(text=f"{speed} AWPM")


def speed_func(window):
    global speed_display, speed_box
    speed_box = Frame(window, borderwidth=1, relief="raised")
    Label(
        speed_box,
        text="Speed",
        font=("bold", 18),
        fg="green",
        borderwidth=1,
        relief="raised",
        padx=100,
        pady=6,
    ).grid()
    speed_display = Label(speed_box, text="0 AWPM", pady=15)
    speed_display.grid(row=1)
    speed_box.grid(column=0, row=0)


def accuracy_func(window):
    global accuracy_display, accuracy_box
    accuracy_box = Frame(window, borderwidth=1, relief="raised")
    Label(
        accuracy_box,
        text="Accuracy",
        font=("bold", 18),
        fg="green",
        borderwidth=1,
        relief="raised",
        padx=100,
        pady=6,
    ).grid()
    accuracy_display = Label(accuracy_box, text="0%", pady=15)
    accuracy_display.grid(row=1)
    accuracy_box.grid(column=1, row=0)


def time_func(window):
    global label, choice
    time_box = Frame(window, borderwidth=1, relief="raised")
    Label(
        time_box,
        text="Time",
        font=("bold", 18),
        fg="green",
        borderwidth=1,
        relief="raised",
        padx=100,
        pady=6,
    ).grid(columnspan=2)
    label = Label(time_box, text="01:00", font=("arial", 14), fg="red", pady=15)
    label.grid(row=1, column=1)
    choice = Combobox(
        time_box,
        values=["30 seconds", "1 minute", "2 minutes"],
        state="readonly",
        width=10,
    )
    choice.current(1)
    choice.bind("<<ComboboxSelected>>", Selected_time)
    choice.grid(row=1, column=0, padx=5)
    time_box.grid(column=2, row=0)

    


if __name__ == "__main__":
    main()
