import os

# Defining function that takes user input for the log file and the keyeords to search 

def read_logs(file_path, keywords):
    """Reads the log file and filters lines containing specific keywords."""
    if not os.path.exists(file_path):
        print(f"\n Error: Log file at {file_path} not found !\n")
        return
    
    print(f"\nSearching for:'{", ".join(keywords)}' in --> [{file_path}]...\n")
    with open(file_path,"r") as file:
        filtered_logs = [line.strip() for line in file if any(keyword.lower() in line.lower() for keyword in keywords)]

        if filtered_logs:
            print(f"\nMatch Found : "+"-"*40)
            for log in filtered_logs:
             print(log)
        else:
            print("\nNo Match Found !\n")

# running the log analyzer 
if __name__ == "__main__":
    #User input for the log file path
    log_file_path=input("\nEnter the path of the log file to be analyzed. DEFAULT (logs/sample.log)").strip()
    if not log_file_path:
        log_file_path="logs/sample.log"

    #User input for keyword search    
    keywords=input("\nEnter the keywords to search. Comma seperated e.g. (failed, denied, warning):\n").strip().split(",")
    keywords = [word.strip() for word in keywords if word.strip()] 

    if not keywords:
        print("\nNo Keywords entered to search. Exiting ...\n")

    else:
        read_logs(log_file_path,keywords)
        print(f"\nX"+"xX"*40)
