from GUI.GUI import GUI


class Main(GUI):
    def __init__(self):
        super().__init__()
        self.gui: GUI = GUI()

    def loop(self):
        self.gui.mainloop()  # type: ignore


if __name__ == "__main__":
    app = Main()
    app.loop()
