from tkinter import *
from PIL import Image, ImageTk
import tkinter
import filter
import plotter
import scrapping


def win_2(text, selected1, selected2):
    def back():
        win2.destroy()
        win_1()
    win2 = Tk()
    win2.geometry("1920x1080")

    # Label(text="Loading", font=('Aerial 30')).pack()


    try:
        if selected1 == '1':
            final_path = scrapping.scrape_amazon(selected_option=selected1, url=text, direct_url=True)
            df_cloud = filter.word_cloud_filter(final_path, url=True, text=text)
        else:
            final_path = scrapping.scrape_amazon(user_input=text, selected_option=selected2)
            df_cloud = filter.word_cloud_filter(final_path, url=False, text=text)

        path_plot1 = plotter.normal_cloud(df_cloud)
        if selected2 == "3" and selected1 == '1':
            df_sentiment = filter.cloud_sentiment_filter(final_path, url=True, text=text)
            path_plot2 = plotter.sentiment_cloud(df_sentiment)
        if selected2 == "3" and selected1 == '2':
            df_sentiment = filter.cloud_sentiment_filter(final_path, url=False, text=text)
            path_plot2 = plotter.sentiment_cloud(df_sentiment)
    except:
        back_btn = Button(win2, text="Back", command=back)
        back_btn.pack(anchor=N)

        win2.mainloop()
        pass

    ##

    if selected2 == '3':
        frame = Frame(win2, width=200, height=200)
        frame.pack()
        frame.place(anchor='e', relx=0.5, rely=0.5)

        # Create a photoimage object of the image in the path
        image1 = Image.open(path_plot1)
        width, height = image1.size
        image1 = image1.crop((width / 5, height / 10, width * 5 / 6, height * 9 / 10))
        test = ImageTk.PhotoImage(image1)

        label1 = tkinter.Label(frame, image=test)
        label1.image = test
        label1.pack()

        frame1 = Frame(win2, width=200, height=200)
        frame1.pack()
        frame1.place(anchor='w', relx=0.5, rely=0.5)

        image2 = Image.open(path_plot2)
        width, height = image2.size
        image2 = image2.crop((width / 5, height / 10, width * 5 / 6, height * 9 / 10))
        test = ImageTk.PhotoImage(image2)

        label2 = tkinter.Label(frame1, image=test)
        label2.image = test
        label2.pack()
    if selected2 == '4':
        frame = Frame(win2, width=400, height=400)
        frame.pack()
        frame.place(anchor='e', relx=0.5, rely=0.5)

        # Create a photoimage object of the image in the path
        image1 = Image.open(path_plot1)
        width, height = image1.size
        image1 = image1.crop((width / 5, height / 10, width * 5 / 6, height * 9 / 10))
        test = ImageTk.PhotoImage(image1)

        label1 = tkinter.Label(frame, image=test)
        label1.image = test
        label1.pack()
    ###

    back_btn = Button(win2, text="Back",command =back)
    back_btn.pack(anchor=N)

    win2.mainloop()


def win_1():
    def submit_get():
        selected1 = str(radio1.get())
        selected2 = str(radio2.get())
        text = entry.get()
        if selected1 in '12' and selected2 in '34' and text != '':
            print(text)
            win.destroy()
            win_2(text, selected1, selected2)
    # Create an instance of tkinter frame or window
    win = Tk()

    # Set the size of the window
    win.geometry("1920x1080")

    radio1 = IntVar()
    radio2 = IntVar()
    # Label(text="Product review analysis", font=('Aerial 11')).pack()
    Label(text="Product review analysis", font=('Aerial 30')).pack()
    Label(text="\nEnter Product/URL to search\n", font=('Aerial 30')).pack()

    # Define radiobutton for each options
    r1 = Radiobutton(win, text="URL", variable=radio1, value=1)
    r1.pack(anchor=N)
    r1.place(x=650, y=300)

    r2 = Radiobutton(win, text="Name", variable=radio1, value=2)
    r2.pack(anchor=N)
    r2.place(x=800, y=300)

    r3 = Radiobutton(win, text="With Sentiment", variable=radio2, value=3)
    r3.pack(anchor=N)
    r3.place(x=650, y=400)

    r4 = Radiobutton(win, text="Without Sentiment", variable=radio2, value=4)
    r4.pack(anchor=N)
    r4.place(x=800, y=400)

    entry = Entry(win, width=40)
    entry.focus_set()
    entry.pack()

    submit_btn = Button(win, text="Submit", command=submit_get)
    submit_btn.pack(anchor=N)
    submit_btn.place(x=750, y=500)

    # Define a label widget
    label = Label(win)
    label.pack()

    win.mainloop()


win_1()