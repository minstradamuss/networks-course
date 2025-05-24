import tkinter as tk
from tkinter import messagebox
import binascii

PACKET_SIZE = 5


def crc16(data: bytes) -> int:
    return binascii.crc_hqx(data, 0xFFFF)


def encode_packet(data: bytes) -> bytes:
    crc = crc16(data)
    return data + crc.to_bytes(2, 'big')


def decode_packet(packet: bytes) -> tuple:
    data, crc_received = packet[:-2], int.from_bytes(packet[-2:], 'big')
    crc_calculated = crc16(data)
    return data, crc_received == crc_calculated


def inject_error(data: bytes, bit_index: int) -> bytes:
    byte_index = bit_index // 8
    bit_offset = bit_index % 8
    corrupted = bytearray(data)
    corrupted[byte_index] ^= 1 << bit_offset
    return bytes(corrupted)


def check_crc(input_text):
    results.delete(1.0, tk.END)
    text = input_text.get()
    packets = [text[i:i+PACKET_SIZE].encode() for i in range(0, len(text), PACKET_SIZE)]

    for i, data in enumerate(packets):
        encoded = encode_packet(data)
        if i % 2 == 1:
            encoded = inject_error(encoded, 3)
        decoded_data, valid = decode_packet(encoded)
        results.insert(tk.END, f"[{i}] Data: {data.decode(errors='ignore')}, Encoded: {encoded.hex()}, Status: {'OK' if valid else 'ERROR'}\n")


root = tk.Tk()
root.title("CRC Packet Checker")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

label = tk.Label(frame, text="Enter text:")
label.pack()

input_text = tk.Entry(frame, width=50)
input_text.pack()

check_btn = tk.Button(frame, text="Check CRC", command=lambda: check_crc(input_text))
check_btn.pack(pady=5)

results = tk.Text(frame, width=80, height=20)
results.pack()

root.mainloop()
