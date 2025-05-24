import binascii
import random

PACKET_SIZE = 5


def crc16(data: bytes) -> int:
    return binascii.crc_hqx(data, 0xFFFF)


def encode_packet(data: bytes) -> bytes:
    crc = crc16(data)
    return data + crc.to_bytes(2, 'big')


def decode_packet(packet: bytes) -> tuple:
    data, crc_received = packet[:-2], int.from_bytes(packet[-2:], 'big')
    crc_calculated = crc16(data)
    return data, crc_received == crc_calculated, crc_received


def inject_error(data: bytes, bit_index: int) -> bytes:
    byte_index = bit_index // 8
    bit_offset = bit_index % 8
    corrupted = bytearray(data)
    corrupted[byte_index] ^= 1 << bit_offset
    return bytes(corrupted)


def run_crc_test(input_text):
    print("=== CRC Packet Test ===")
    packets = [input_text[i:i+PACKET_SIZE].encode() for i in range(0, len(input_text), PACKET_SIZE)]

    for i, data in enumerate(packets):
        encoded = encode_packet(data)
        original_crc = encoded[-2:]
        if i % 2 == 1:
            encoded = inject_error(encoded, random.randint(0, (PACKET_SIZE+2)*8 - 1))
        decoded_data, valid, received_crc = decode_packet(encoded)

        print(f"[{i}] Data: {data.decode(errors='ignore'):5} | Encoded: {encoded.hex()} | CRC: {received_crc:04X} | Status: {'OK' if valid else 'ERROR'}")


if __name__ == "__main__":
    text = input("Enter text to encode and test with CRC: ")
    run_crc_test(text)
