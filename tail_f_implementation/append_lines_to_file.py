LOG_FILE_PATH = "your_log_file.log"
with open(LOG_FILE_PATH, mode="a+") as f:
    for i in range(1):
        f.write(f"This is - {i}th Line\n")
