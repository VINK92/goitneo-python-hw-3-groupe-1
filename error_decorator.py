def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter a valid username."
        except ValueError:
            return "Invalid input format. Please provide both username and phone number."
        except IndexError:
            return "Invalid input format. Please provide both username and phone number."
    return inner
