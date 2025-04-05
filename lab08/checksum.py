def calculate_checksum(data: bytes, k: int = 16) -> int:
    if k % 8 != 0:
        raise ValueError("The block size k must be a multiple of 8.")
    
    block_size = k // 8
    sum = 0

    if len(data) % block_size != 0:
        data += bytes(block_size - (len(data) % block_size))

    for i in range(0, len(data), block_size):
        value = int.from_bytes(data[i:i + block_size], byteorder='big')
        sum += value
        sum = (sum & 0xFFFF) + (sum >> 16)

    return ~sum & 0xFFFF


def verify_checksum(data: bytes, checksum: int, k: int = 16) -> bool:

    if k % 8 != 0:
        raise ValueError("The block size k must be a multiple of 8.")
    
    block_size = k // 8
    sum = checksum

    if len(data) % block_size != 0:
        data += bytes(block_size - (len(data) % block_size))

    for i in range(0, len(data), block_size):
        value = int.from_bytes(data[i:i + block_size], byteorder='big')
        sum += value
        sum = (sum & 0xFFFF) + (sum >> 16)

    return (sum & 0xFFFF) == 0xFFFF


def run_tests():
    print("Running tests...\n")

    # Test 1: Valid data, 16-bit blocks
    data = bytes([0x12, 0x34, 0x56, 0x78])
    checksum = calculate_checksum(data)
    print("Test 1 - Checksum:", checksum)
    assert verify_checksum(data, checksum)

    # Test 2: Corrupted checksum
    wrong_checksum = (checksum + 90) & 0xFFFF
    print("Test 2 - Wrong checksum:", wrong_checksum)
    assert not verify_checksum(data, wrong_checksum)

    # Test 3: Corrupted data
    broken_data = bytes([0x13, 0x34, 0x56, 0x78])
    print("Test 3 - Corrupted data")
    assert not verify_checksum(broken_data, checksum)

    # Test 4: 32-bit blocks, valid
    checksum_32 = calculate_checksum(data, k=32)
    print("Test 4 - 32-bit checksum:", checksum_32)
    assert verify_checksum(data, checksum_32, k=32)

    # Test 5: Corrupted checksum, 32-bit blocks
    wrong_checksum_32 = (checksum_32 + 1) & 0xFFFF
    print("Test 5 - Wrong 32-bit checksum:", wrong_checksum_32)
    assert not verify_checksum(data, wrong_checksum_32, k=32)

    # Test 6: Corrupted data, 32-bit blocks
    broken_data_32 = bytes([0x12, 0x35, 0x56, 0x78])
    print("Test 6 - Corrupted 32-bit data")
    assert not verify_checksum(broken_data_32, checksum_32, k=32)

    # Test 7: Odd-length data with padding
    data_odd = bytes([0x01, 0x02, 0x03])
    checksum_odd = calculate_checksum(data_odd)
    print("Test 7 - Odd-length data checksum:", checksum_odd)
    assert verify_checksum(data_odd, checksum_odd)

    # Test 8: Empty data
    data_empty = bytes()
    checksum_empty = calculate_checksum(data_empty)
    print("Test 8 - Empty data checksum:", checksum_empty)
    assert verify_checksum(data_empty, checksum_empty)

    # Test 9: All-zero data
    data_zero = bytes([0x00] * 10)
    checksum_zero = calculate_checksum(data_zero)
    print("Test 9 - All-zero data checksum:", checksum_zero)
    assert verify_checksum(data_zero, checksum_zero)

    # Test 10: All-one data (0xFF)
    data_ones = bytes([0xFF] * 10)
    checksum_ones = calculate_checksum(data_ones)
    print("Test 10 - All-ones data checksum:", checksum_ones)
    assert verify_checksum(data_ones, checksum_ones)

    # Test 11: Large data (e.g., 1000 bytes)
    data_large = bytes([i % 256 for i in range(1000)])
    checksum_large = calculate_checksum(data_large)
    print("Test 11 - Large data checksum:", checksum_large)
    assert verify_checksum(data_large, checksum_large)

    # Test 12: One byte only
    data_single = bytes([0xAB])
    checksum_single = calculate_checksum(data_single)
    print("Test 12 - Single byte checksum:", checksum_single)
    assert verify_checksum(data_single, checksum_single)

    print("\nAll 12 tests passed!")


if __name__ == "__main__":
    run_tests()
