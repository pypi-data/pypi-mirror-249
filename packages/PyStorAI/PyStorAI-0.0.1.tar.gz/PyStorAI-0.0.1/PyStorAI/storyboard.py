import datetime

def get_current_datetime():
    current_datetime = datetime.datetime.now()
    return current_datetime

if __name__ == "__main__":
    current_datetime = get_current_datetime()
    print(f"Current Date and Time: {current_datetime}")
