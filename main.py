import concurrent.futures
import socket
import tkinter as tk
from tkinter import ttk

class NetworkServiceChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Service Checker")

        # Create a ttk Style
        self.style = ttk.Style()

        # Configure the style for the Frame (entire GUI)
        self.style.configure("TFrame", background='#CCCCCC')  # grey

        # Configure the style for the Label
        self.style.configure("TLabel", font=("Arial", 12), padding=5, background='#CCCCCC')

        # Configure the style for the Entry
        self.style.configure("TEntry", font=("Arial", 12), padding=5)

        # Configure the style for the Button
        self.style.configure("TButton", font=("Arial", 12), padding=10, background='#4CAF50', foreground='white')

        # Configure the style for the Text
        self.style.configure("TText", font=("Arial", 12), padding=5)

        self.frame = ttk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)  # Make the frame fill the entire window

        self.target_host_label = ttk.Label(self.frame, text="Enter the target host or IP address:")
        self.target_host_entry = ttk.Entry(self.frame)

        self.check_button = ttk.Button(self.frame, text="Check Services", command=self.check_services)

        self.result_label = ttk.Label(self.frame, text="Results:")
        self.result_text = tk.Text(self.frame, height=10, width=50, state=tk.DISABLED)

        self.target_host_label.pack(pady=5)
        self.target_host_entry.pack(pady=5)
        self.check_button.pack(pady=10)
        self.result_label.pack()
        self.result_text.pack(pady=5)

    # ADD
    def check_service(self, host, port):
        try:
            # Use synchronous socket library
            with socket.create_connection((host, port), timeout=5):
                return True
        except (socket.timeout, ConnectionRefusedError):
            return False
        except Exception as e:
            return str(e)

    def check_services_async(self, target_host, services):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(lambda p: (p[0], p[1], self.check_service(target_host, p[1])), services.items()))

        return results

    def display_results(self, results):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)

        for service, port, result in results:
            status = "Open" if result else "Closed"
            self.result_text.insert(tk.END, f"{service} (Port {port}): {status}\n")

        self.result_text.config(state=tk.DISABLED)

    def check_services(self):
        target_host = self.target_host_entry.get()
        global services_to_check
        services_to_check = {
            "HTTP": 80,
            "HTTPS": 443,
            "FTP": 21,
            "SSH": 22,
            "Telnet": 23,
            "SMTP": 25,
            "DNS": 53,
            "HTTP Proxy": 8080,
            "Minecraft": 25565,
        }

        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.config(state=tk.DISABLED)

        results = self.check_services_async(target_host, services_to_check)
        self.display_results(results)

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkServiceChecker(root)
    root.mainloop()
