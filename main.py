from GUI.GUI import GUI


def app():
    gui: GUI = GUI()
    gui.mainloop()  # type: ignore


if __name__ == "__main__":
    app()
