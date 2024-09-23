#Can Günyel 150200049
import subprocess as sp
import re
from datetime import datetime
import multiprocessing


def trace_website(website, repetitions):
    # Define the tracert command 
    command = f"tracert {website}"
    results = []

    
    for _ in range(repetitions):
        # Run the tracert command and capture the output
        result = sp.run(command, shell=True, cwd="C:\\Windows\\System32", capture_output=True)
        output_text = result.stdout.decode()
        
        # Parse the output to extract time values
        lines = output_text.split('\n')
        last_line = lines[-4]
        time_values = re.findall(r'(\d+) ms', last_line)
        results.append(time_values)

    return website, results


def trace_website_parallel(params):#to parallize the process
    website, repetitions = params
    website, time_values = trace_website(website, repetitions)
    return website, time_values

if __name__ == "__main__":
    # Get the current date and time
    time_date = datetime.now()
    time_date_str = time_date.strftime("%Y-%m-%d_%H-%M-%S")
    
    #Output file name
    output_file_path = f"output_{time_date_str}.txt"
    
    # List of websites
    websites = ["zalonda.de", "hepsiburada.com", "lanacion.com.ar", "vg.no", "property24.com", "google.com", "mail.ru", "tehrantimes.com", "im.qq.com", "flipkart.com"]
    
    # List of repetitions 
    repetitions = [4,7,10,14,17,20,24,27,30,34]
    #repetitions = [1,2]#small sample
    with open(output_file_path, "a") as output_file:
        with multiprocessing.Pool() as pool:
            # Generate a list of parameters for the trace_website_parallel function
            params = [(website, rep) for website in websites for rep in repetitions]
            
            #Multiprocessing the process with pool map
            results = pool.map(trace_website_parallel, params)

        for website, time_values in results:
            # Write results to the output file
            output_file.write(f"Results for {website} (Execution Counts):\n")
            for i, values in enumerate(time_values, start=1):
                output_file.write(f"Repetition {i}: {', '.join(values)}\n")
            output_file.write("\n")
