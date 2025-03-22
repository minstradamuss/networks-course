import tkinter as tk
from tkinter import messagebox, simpledialog
from ftplib import FTP

class FTPClientGUI:
    def __init__(self, root):
        self.ftp = None
        self.root = root
        self.root.geometry("1000x1000")
        self.root.title("FTP Client")

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Server:").place(x=100, y=20)
        self.server_entry = tk.Entry(self.root)
        self.server_entry.insert(0, 'ftp.dlptest.com')
        self.server_entry.place(x=200, y=20)

        tk.Label(self.root, text="Port:").place(x=400, y=20)
        self.port_entry = tk.Entry(self.root)
        self.port_entry.insert(0, '21')
        self.port_entry.place(x=500, y=20)

        tk.Label(self.root, text="Username:").place(x=100, y=60)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.insert(0, 'dlpuser')
        self.username_entry.place(x=200, y=60)

        tk.Label(self.root, text="Password:").place(x=400, y=60)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.insert(0, 'rNrKYTX9g7z3RgJRmxWuGHbeu')
        self.password_entry.place(x=500, y=60)

        tk.Button(self.root, text="Connect", command=self.connect_to_ftp).place(x=300, y=100)
        tk.Button(self.root, text="List Files", command=self.list_files).place(x=400, y=100)

        tk.Label(self.root, text="Filename:").place(x=250, y=140)
        self.filename_entry = tk.Entry(self.root)
        self.filename_entry.place(x=350, y=140)

        tk.Button(self.root, text="Retrieve File", command=self.retrieve_file).place(x=200, y=180)
        tk.Button(self.root, text="Create File", command=self.create_file).place(x=300, y=180)
        tk.Button(self.root, text="Delete File", command=self.delete_file).place(x=400, y=180)
        tk.Button(self.root, text="Update File", command=self.update_file).place(x=500, y=180)

        self.log_text = tk.Text(self.root, height=40, width=75)
        self.log_text.place(x=200, y=220)

    def connect_to_ftp(self):
        server = self.server_entry.get()
        port = int(self.port_entry.get())
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            self.ftp = FTP()
            self.ftp.connect(server, port)
            self.ftp.login(username, password)
            self.log_text.insert(tk.END, "Connected to FTP server\n")
            self.list_files()
        except Exception as e:
            self.log_text.insert(tk.END, f"Error connecting: {str(e)}\n")
            messagebox.showerror("Connection Error", str(e))

    def list_files(self):
        if not self.ftp:
            self.log_text.insert(tk.END, "Not connected to FTP server.\n")
            return
        try:
            files = self.ftp.nlst()
            self.log_text.insert(tk.END, "\nLIST OF FILES:\n")
            for file in files:
                self.log_text.insert(tk.END, f"  - {file}\n")
            self.log_text.insert(tk.END, "END OF LIST\n\n")
        except Exception as e:
            self.log_text.insert(tk.END, f"Error listing files: {str(e)}\n")
            messagebox.showerror("Error", str(e))

    def retrieve_file(self):
        filename = self.filename_entry.get()
        try:
            lines = []
            self.ftp.retrlines("RETR " + filename, lines.append)
            self.log_text.insert(tk.END, '\nRETRIEVED FILE:\n')
            for line in lines:
                self.log_text.insert(tk.END, line + '\n')
            self.log_text.insert(tk.END, "END OF FILE\n\n")
        except Exception as e:
            self.log_text.insert(tk.END, f"Error retrieving file: {str(e)}\n")
            messagebox.showerror("Error", str(e))

    def create_file(self):
        if not self.ftp:
            self.log_text.insert(tk.END, "Not connected to FTP server.\n")
            return
        filename = self.filename_entry.get()
        file_content = simpledialog.askstring("Enter File Content", "Enter the content of the file:")
        
        try:
            with open(filename, "w") as file:
                file.write(file_content)
            with open(filename, "rb") as file:
                self.ftp.storbinary(f"STOR {filename}", file)

            self.log_text.insert(tk.END, f"File '{filename}' created and uploaded.\n")
        except Exception as e:
            self.log_text.insert(tk.END, f"Error creating file: {str(e)}\n")
            messagebox.showerror("Error", str(e))

    def update_file(self):
        if not self.ftp:
            self.log_text.insert(tk.END, "Not connected to FTP server.\n")
            return
        filename = self.filename_entry.get()
        
        try:
            with open(filename, "wb") as file:
                self.ftp.retrbinary(f"RETR {filename}", file.write)
            
            with open(filename, "r") as file:
                file_content = file.read()

            updated_content = simpledialog.askstring("Update File Content", "Update the content of the file:", initialvalue=file_content)
            
            with open(filename, "w") as file:
                file.write(updated_content)
            
            with open(filename, "rb") as file:
                self.ftp.storbinary(f"STOR {filename}", file)
            
            self.log_text.insert(tk.END, f"File '{filename}' updated.\n")
            
        except Exception as e:
            self.log_text.insert(tk.END, f"Error updating file: {str(e)}\n")
            messagebox.showerror("Error", str(e))

    def delete_file(self):
        if not self.ftp:
            self.log_text.insert(tk.END, "Not connected to FTP server.\n")
            return
        filename = self.filename_entry.get()
            
        try:
            self.ftp.delete(filename)
            self.log_text.insert(tk.END, f"File '{filename}' deleted.\n")
        except Exception as e:
            self.log_text.insert(tk.END, f"Error deleting file: {str(e)}\n")
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = FTPClientGUI(root)
    root.mainloop()
