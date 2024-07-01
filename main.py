import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
from tkinter.filedialog import asksaveasfile
import qrcode
import cv2 as cv
import pyzbar.pyzbar as pyzbar
from PIL import Image

app_title = "QR Code Generator and Scanner in Python"
win = tk.Tk()
win.title(app_title)
width = 480
height = 180
screenwidth = win.winfo_screenwidth()
screenheight = win.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
win.geometry(alignstr)
win.resizable(width=False, height=False)
qr_default_fg_color = "black"
qr_default_bg_color = "white"

def save_and_display():
    files = [('PNG Image', '*.png')]
    file_path = asksaveasfile(filetypes=files, defaultextension=files).name
    if file_path:
        generate_qr(file_path)
        img = cv.imread(file_path)
        cv.imshow('QR Code', img)
        cv.waitKey(0)
        cv.destroyAllWindows()

def choose_fg_color():
    global qr_default_fg_color
    color_code = colorchooser.askcolor(title="Choose QR Foreground Color")
    if color_code[1] is not None:
        qr_default_fg_color = color_code[1]

def choose_bg_color():
    global qr_default_bg_color
    color_code = colorchooser.askcolor(title="Choose QR Background Color")
    if color_code[1] is not None:
        qr_default_bg_color = color_code[1]

def generate_qr(file_path):
    input_URL = LineEditURL.get()
    if input_URL != '':
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=15,
            border=4,
        )
        qr.add_data(input_URL)
        qr.make(fit=True)
        img = qr.make_image(fill_color=qr_default_fg_color, back_color=qr_default_bg_color)
        img.save(file_path)
        messagebox.showinfo(app_title, "QR Code generated successfully")
    else:
        messagebox.showerror(app_title, "Please enter URL / Link / Web Address to generate QR Code")

def read_qr_from_webcam():
    cap = cv.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        decoded_objects = pyzbar.decode(frame)
        for obj in decoded_objects:
            data = obj.data.decode('utf-8')
            print("Data:", data)
            messagebox.showinfo("QR Code Data", data)

        cv.imshow('QR Code Scanner', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

def read_file_qr():
    filename = tk.filedialog.askopenfilename(title="Select QR Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if filename:
        try:
            img = Image.open(filename)
            decoded_objects = pyzbar.decode(img)
            if decoded_objects:
                for obj in decoded_objects:
                    data = obj.data.decode("utf-8", errors="ignore")  # Decode with error handling
                    print("Data:", data)
                    messagebox.showinfo("QR Code Data", data)
            else:
                messagebox.showinfo(app_title, "No QR code found in the image.")
        except FileNotFoundError:
            messagebox.showerror(app_title, "File not found. Please check the path and try again.")
        except Exception as e:
            messagebox.showerror(app_title, f"An error occurred: {e}")

LineEditURL = ttk.Entry(win)
LineEditURL.place(x=30, y=30, width=345, height=25)

BtnGenerate = ttk.Button(win, text="Generate", command=save_and_display)
BtnGenerate.place(x=380, y=29, width=70, height=27)

BtnBackgroundColor = ttk.Button(win, text="Choose QR Background Color", command=choose_bg_color)
BtnBackgroundColor.place(x=29, y=60, width=210, height=30)

BtnForegroundColor = ttk.Button(win, text="Choose QR Foreground Color", command=choose_fg_color)
BtnForegroundColor.place(x=240, y=60, width=210, height=30)

BtnScanQRWebcam = ttk.Button(win, text="Scan QR Code from Webcam", command=read_qr_from_webcam)
BtnScanQRWebcam.place(x=29, y=90, width=210, height=30)

BtnScanQRFile = ttk.Button(win, text="Scan QR Code from File", command=read_file_qr)
BtnScanQRFile.place(x=240, y=90, width=210, height=30)

win.mainloop()
