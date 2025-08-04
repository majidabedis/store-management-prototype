class Menu:
    def __init__(self, title, options=None):
        self.title = title
        self.options = options if options else {}

    def add_option(self, key, label, action, submenu=None):
        self.options[key] = (label, action, submenu)

    def display(self):
        print(f"\n=== {self.title} ===")
        for key, (label, _, _) in self.options.items():
            print(f"{key}. {label}")

    def execute(self):
        while True:
            self.display()
            choice = input("لطفاً گزینه مورد نظر را انتخاب کنید: ")
            if choice in self.options:
                label, action, submenu = self.options[choice]
                if action:
                    action()
                if submenu:
                    submenu.execute()
            else:
                print("انتخاب نامعتبر!")
