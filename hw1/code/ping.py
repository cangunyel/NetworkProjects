import subprocess as sp
import re
from datetime import datetime
from multiprocessing import Pool

def ping_website(website, ping_count):
    command = f"ping -n {ping_count} {website}"
    result = sp.run(command, shell=True, cwd="C:\\Windows\\System32", capture_output=True)
    output_text = result.stdout.decode()
    time_values = re.findall(r"time=(\d+)ms", output_text)
    return website, time_values

if __name__ == "__main__":
    time_date = datetime.now()
    time_date_str = time_date.strftime("%Y-%m-%d_%H-%M-%S")
    output_file_path = f"output_{time_date_str}.txt"
    websites = ["zalonda.de", "hepsiburada.com", "lanacion.com.ar", "vg.no", "property24.com", "google.com", "mail.ru", "tehrantimes.com", "im.qq.com", "flipkart.com"]

    with open(output_file_path, "a") as output_file:
        with Pool() as pool:
            results = []
            for website in websites:
                for x in range(10):
                    ping_count = (x + 1) * 10
                    results.append(pool.apply_async(ping_website, (website, ping_count)))

            for result in results:
                website, time_values = result.get()
                output_file.write(f"Results for {website} (Ping Count {len(time_values)}):\n")
                if time_values:
                    output_file.write(",".join(time_values) + "\n")
                output_file.write("\n")
