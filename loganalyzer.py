import os

# Define the log file path 
log_file_path = "logs/sample.log";

# Define keywords to look up in the log analysis 
keywords = ["Failed", "Warning", "Error", "Denied"];

def read_logs(file_path):
    
    if not os.path.exists(file_path):
        print(f"Log file: {file_path} not found !")
        return
    
    with open(file_path,"r") as file:
        for line in file:
            if any( keyword in line for  keyword in keywords):
                print(line.strip())

# running the log analyzer 
if __name__ == "__main__":
    read_logs(log_file_path)