import tkinter as tk

# class for calculator
class Calculator:
    def __init__(self):
        # Encapsulation: Storing private state variables
        self._expression = ""
    
    def add_to_expression(self, value):
        self._expression += str(value)
    
    def clear_expression(self):
        self._expression = ""
    
    def evaluate_expression(self):
        try:
            result = str(eval(self._expression)) 
        except Exception as e:
            result = "Error"
        self._expression = result
        return result

# Multiple inheritance, inheriting from both Calculator and tk.Tk
class CalculatorApp(Calculator, tk.Tk):
    def __init__(self):
        Calculator.__init__(self)
        tk.Tk.__init__(self)
        self.title("Calculator")
        self.geometry("370x400")
        self.create_widgets()
    
    # Overriding Tkinter methods
    def create_widgets(self):
        self.entry = tk.Entry(self, font=("Arial", 24), borderwidth=2, relief="solid")
        self.entry.grid(row=0, column=0, columnspan=4)

        buttons = [
            '7', '8', '9', '/', 
            '4', '5', '6', '*', 
            '1', '2', '3', '-', 
            '0', '.', '=', '+'
        ]
        
        row_val = 1
        col_val = 0

        for button in buttons:
            action = lambda x=button: self.on_button_click(x)
            b = tk.Button(self, text=button, font=("Arial", 18), command=action)
            b.grid(row=row_val, column=col_val, sticky="nsew")
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1
        
        clear_button = tk.Button(self, text="Clear", font=("Arial", 18), command=self.clear_expression_action)
        clear_button.grid(row=row_val, column=0, columnspan=4, sticky="nsew")
    
    def on_button_click(self, char):
        if char == "=":
            self.display_result()
        else:
            self.add_to_expression(char)
            self.update_entry()

    def display_result(self):
        result = self.evaluate_expression()
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, result)

    def update_entry(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, self._expression)
    
    # Decorator to demonstrate functionality extension
    @staticmethod
    def display(func):
        def wrapper(*args, **kwargs):
            print("Displaying the result on the screen")
            return func(*args, **kwargs)
        return wrapper

    @display
    def clear_expression_action(self):
        self.clear_expression()
        self.update_entry()

if __name__ == "__main__":
    app = CalculatorApp()

    # Polymorphism - Tkinter methods will be dynamically resolved
    app.mainloop()
