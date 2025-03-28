import os
import datetime
import json
import csv
import time

# Defining function that takes user input for the log file and the keyeords to search 

def read_logs(file_path, keywords):
    """Reads the log file and filters lines containing specific keywords."""
    if not os.path.exists(file_path):
        print(f"\nError: Log file at {file_path} not found !\n")
        return
    
    print(f"\nSearching for:'{", ".join(keywords)}' in --> [{file_path}]...\n")

    filtered_logs=[]
    with open(file_path,"r") as file:
        for line in file:
            if any(keyword.lower() in line.lower() for keyword in keywords):
                filtered_logs.append(line.strip())

    if filtered_logs:
        print(f"\nMatch Found : "+"-"*40)
        for log in filtered_logs:
         print(log)

        # Giving user the option to chose a format for export
        export_logs(file_path,keywords,filtered_logs)   

    else:
        print("\nNo Match Found !\n")

def export_logs(file_path,keywords,logs):
    """ We will save the recordings in a log file, these can be collectively stored in a Output_logs Directory"""
    output_dir="Output_logs"
    os.makedirs(output_dir, exist_ok=True)
    # Timestamps
    timestamp=datetime.datetime.now().strftime("%d %b %Y_%H%M%S")
    file_base=f"{output_dir}/Filtered_Logs_{timestamp}"

    print(f"\n💾 Choose export format: ")
    print("1. TXT")
    print("2. JSON")
    print("3. CSV")

    choice = input("\nEnter your choice(1/2/3): ").strip()

    if choice== "1":
        file_name=f"{file_base}.txt"
        # Writing output to file 
        with open(file_name,"w") as file:
            file.write(f"Logs filtered. SOURCE: {file_path} \n")
            file.write(f"Filter KEYWORDS: [{",".join(keywords)}] \n") 
            file.write("-" * 20 + "\n")
            file.write("-" * 20 + "\n")
            file.write("\n".join(logs))
        print(f"\nFiltered logs saved to: {file_name}")

    elif choice == "2":
        file_name=f"{file_base}.json"
        with open(file_name,"w") as file:
            json.dump(logs, file, indent=4)
        print(f"Logs saved to {file_name}")
    
    elif choice=="3":
        file_name=f"{file_base}.csv"
        with open(file_name, "w", newline="") as file:
            writer=csv.writer(file)
            writer.writerow(["Logs"])
            for log in logs:
                writer.writerow([log])
        print(f"Logs Saved to {file_name}")
    
    else:
        print("\nInvalid Choice ! Logs will not be saved.") 

def monitor_logs(file_path, keywords):
    """ Monitors a log file in real time for new logs containing specific keywords and saves results"""

    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found!\n")
        return
    
    print(f"\nMonitoring '{file_path}' for keywords: {', '.join(keywords)} (Press Ctrl+C to stop)...\n")
    matched_logs=[]

    try: 
        with open(file_path, "r") as file:
            file.seek(0, os.SEEK_END) # --> Moves to the end of the file

            while True:
                line = file.readline()
                if line:
                    if any(keyword.lower() in line.lower() for keyword in keywords):
                        log_entry = line.strip()
                        print(f"{log_entry}")
                        matched_logs.append(log_entry)
                    else: 
                        time.sleep(1) #Wait for new lines to appear
    
    except KeyboardInterrupt:
        print("Monitoring Stopped.")

        if(matched_logs):
            print("\n Saving logs ...")
            export_logs(file_path,keywords,matched_logs) 

        else:
            print("No logs were matched. Nothing to save.")            

# running the log analyzer 
if __name__ == "__main__":

    print("\nLog Analyzer - Choose an Option:")
    print("1. Analyze an exisiting log file")
    print("2. Monitor logs in real-time")

    mode = input("\nEnter your choice(1/2): ").strip()

    if mode == "1":
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
    
    elif mode =="2":
        log_file_path=input("\n Enter log file path to monitor (default: logs/sample.log): ").strip()
        if not log_file_path:
            log_file_path = "logs/sample.log"

        keywords = input("\nEnter keywords to watch (comma-separated, e.g., 'failed,error,denied'): ").strip().split(",")
        keywords = [word.strip() for word in keywords if word.strip()]

        if not keywords:
            print("\nNo keywords provided. Exiting...\n")
        else:
            monitor_logs(log_file_path, keywords)

    else:
        print("\nInvalid choice! Exiting...\n")
    
    print(f"\nX"+"xX"*40)
