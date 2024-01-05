"""Easy peasy lemon squeezy!🍋🤝🍸"""
import inspect
import pickle


def save_pkl(var) -> None:
    frame = inspect.currentframe()
    try:
        previous_frame = frame.f_back
        var_name = None
        for name, value in previous_frame.f_locals.items():
            if value is var:
                var_name = name
                break
        if var_name:
            file_name = f"{var_name}.pkl"
        else:
            file_name = "apple.pkl"     # TODO: make random fruits
            print("I couldn't find the variable name, but here's a fruit for you instead!")
        with open(file_name, 'wb') as file:
            pickle.dump(var, file)
        print(f"Variable '{file_name}' saved.")
    finally:
        del frame


def load_pkl(filename: str):
    try:
        with open(filename, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None