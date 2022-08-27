from tkinter import messagebox


def error_popup(title: str, msg: str) -> None:
    """Show popup window with error message

    Args:
        title (str): _description_
        msg (str): _description_
        window (Tk, optional): _description_. Defaults to None.
    """
    messagebox.showinfo(title=title, message=msg)
