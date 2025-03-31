import os
import datetime
import json
import csv
import time

# Define severity levels and their keywords
SEVERITY_LEVELS = {
    "INFO": ["started", "connected", "logged in", "success"],
    "WARNING": ["failed", "failed attempt", "timeout", "deprecated", "high memory"],
    "ERROR": ["authentication failure", "disk error", "process crash"],
    "CRITICAL": ["root access", "brute-force", "security breach"]
}

# Defining function that clssifies log entry based on predefined severity keywords
def classify_log(log_line):
    """Classifies a log entry based on predefined severity keywords."""
    log_lower = log_line.lower()
    
    for severity, keywords in SEVERITY_LEVELS.items():
        if any(keyword in log_lower for keyword in keywords):
            return severity, log_line
    """Defaults to INFO"""
    return "INFO", log_line  # Default to INFO if no match is found

# Defining function that takes user input for the log file and the keyeords to search 

def read_logs(file_path, keywords,severity_filter=None ):
    """Reads the log file and filters lines containing specific keywords."""
    if not os.path.exists(file_path):
        print(f"\nError: Log file at {file_path} not found !\n")
        return
    
    print(f"\nSearching for:'{", ".join(keywords)}' in --> [{file_path}]...\n")

    filtered_logs=[]
    with open(file_path,"r") as file:
        for line in file:
            severity, classified_log = classify_log(line)
            if any(keyword.lower() in line.lower() for keyword in keywords) and (severity_filter is None or severity in severity_filter):
                filtered_logs.append(f"[{severity}] {classified_log.strip()}")

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
            writer.writerow(["Severity", "Log Entry"])
            for log in logs:
                parts = log.split("]",1)
                writer.writerow([parts[0][1:], parts[1] if len(parts) > 1 else ""])
        print(f"Logs Saved to {file_name}")
    
    else:
        print("\nInvalid Choice ! Logs will not be saved.") 

def monitor_logs(file_path, keywords, severity_filter=None):
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
                    severity, classified_log = classify_log(line)

                    if any(keyword.lower() in line.lower() for keyword in keywords) and (severity_filter is None or severity in severity_filter):
                        log_entry = f"[{severity}] {classified_log.strip()}"
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

        print("\n🔽 Choose Severity Level to Filter:")
        print("1. INFO")
        print("2. WARNING")
        print("3. ERROR")
        print("4. CRITICAL")
        print("5. ALL")

        severity_choice = input("\nEnter choice (1/2/3/4/5): ").strip()
        severity_map = {"1": ["INFO"], "2": ["WARNING"], "3": ["ERROR"], "4": ["CRITICAL"], "5": None}
        severity_filter = severity_map.get(severity_choice, None)

        if keywords:
            read_logs(log_file_path, keywords, severity_filter)
        else:
            print("\nNo keywords entered. Exiting...")
    
    elif mode =="2":
        log_file_path=input("\nEnter log file path to monitor (default: logs/sample.log): ").strip()
        if not log_file_path:
            log_file_path = "logs/sample.log"

        keywords = input("\nEnter keywords to watch (comma-separated, e.g., 'failed,error,denied'): ").strip().split(",")
        keywords = [word.strip() for word in keywords if word.strip()]

        print("\n🔽 Choose Severity Level to Filter:")
        print("1. INFO")
        print("2. WARNING")
        print("3. ERROR")
        print("4. CRITICAL")
        print("5. ALL")

        severity_choice = input("\nEnter choice (1/2/3/4/5): ").strip()
        severity_map = {"1": ["INFO"], "2": ["WARNING"], "3": ["ERROR"], "4": ["CRITICAL"], "5": None}
        severity_filter = severity_map.get(severity_choice, None)

        if keywords:
            monitor_logs(log_file_path, keywords, severity_filter)
        else:
            print("\nNo keywords provided. Exiting...")

    else:
        print("\nInvalid choice! Exiting...\n")
    
    print(f"\nX"+"xX"*40)
