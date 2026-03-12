import struct
from .huffman import HuffmanCompression

class CompressionMethod:
    HUFFMAN = 0
    DEFLATE = 1

class BitWriter:
    def __init__(self):
        self.buffer = bytearray()
        self.current_byte = 0
        self.bits_filled = 0
 
    def write_bits(self, value, bit_count):
        for i in range(bit_count - 1, -1, -1):
            bit = (value >> i) & 1
            self.current_byte = (self.current_byte << 1) | bit
            self.bits_filled += 1
            if self.bits_filled == 8:
                self.buffer.append(self.current_byte)
                self.current_byte = 0
                self.bits_filled = 0

    def get_bytes(self):
        if self.bits_filled > 0:
            self.current_byte <<= (8 - self.bits_filled)
            self.buffer.append(self.current_byte)
        return bytes(self.buffer)

class BitReader:
    def __init__(self, data):
        self.data = data
        self.byte_index = 0
        self.bit_index = 0

    def read_bit(self):
        if self.byte_index >= len(self.data):
            raise EOFError("No more bits")
        bit = (self.data[self.byte_index] >> (7 - self.bit_index)) & 1
        self.bit_index += 1
        if self.bit_index == 8:
            self.bit_index = 0
            self.byte_index += 1
        return bit

    def read_bits(self, count):
        value = 0
        for _ in range(count):
            value = (value << 1) | self.read_bit()
        return value

class LZ77:
    def __init__(self, window_size=4096, lookahead_buffer_size=64):
        self.window_size = window_size
        self.lookahead_buffer_size = lookahead_buffer_size

    def compress(self, data):
        i = 0
        writer = BitWriter()
        data_len = len(data)
        window = memoryview(data)

        while i < data_len:
            best_match_distance = -1
            best_match_length = -1

            end_of_buffer = min(i + self.lookahead_buffer_size, data_len)
            substring = window[i:end_of_buffer].tobytes()

            start_index = max(0, i - self.window_size)
            search_buffer = window[start_index:i].tobytes()

            for length in range(3, len(substring) + 1):
                candidate = substring[:length]
                pos = search_buffer.rfind(candidate)
                if pos != -1:
                    best_match_distance = i - (start_index + pos)
                    best_match_length = length
                else:
                    break

            if best_match_length >= 3:
                writer.write_bits(1, 1)
                writer.write_bits(best_match_length, 8)
                writer.write_bits(best_match_distance, 12)
                i += best_match_length
            else:
                writer.write_bits(0, 1)
                writer.write_bits(data[i], 8)
                i += 1

        writer.write_bits(1, 1)
        writer.write_bits(0, 8)
        writer.write_bits(0, 12)
        return writer.get_bytes()

    def decompress(self, compressed):
        reader = BitReader(compressed)
        result = bytearray()
        try:
            while True:
                is_backref = reader.read_bit()
                if is_backref:
                    length = reader.read_bits(8)
                    distance = reader.read_bits(12)
                    if length == 0 and distance == 0:
                        break
                    for _ in range(length):
                        result.append(result[-distance])
                else:
                    literal = reader.read_bits(8)
                    result.append(literal)
        except EOFError:
            pass
        return bytes(result)

class DeflateCompression:
    @staticmethod
    def compress(data, level=9):
        if not data:
            return None

        lz77 = LZ77()
        compressed_lz77 = lz77.compress(data)

        huffman = HuffmanCompression()
        compressed_huff = huffman.compress(compressed_lz77)

        return struct.pack('B', CompressionMethod.DEFLATE) + compressed_huff

    @staticmethod
    def decompress(compressed_data):
        if not compressed_data:
            return None

        method = struct.unpack('B', compressed_data[:1])[0]
        if method != CompressionMethod.DEFLATE:
            raise ValueError("Invalid compression method")

        compressed_huff = compressed_data[1:]
        huffman = HuffmanCompression()
        decompressed_lz77 = huffman.decompress(compressed_huff)

        lz77 = LZ77()
        return lz77.decompress(decompressed_lz77)

class CompressFactory:
    @staticmethod
    def compress(data, method=CompressionMethod.DEFLATE, level=9):
        if method == CompressionMethod.HUFFMAN:
            huffman = HuffmanCompression()
            return struct.pack('B', CompressionMethod.HUFFMAN) + huffman.compress(data)
        elif method == CompressionMethod.DEFLATE:
            return DeflateCompression.compress(data, level)
        else:
            raise ValueError(f"Unsupported compression method: {method}")

    @staticmethod
    def decompress(compressed_data):
        if not compressed_data:
            return None
        method = struct.unpack('B', compressed_data[:1])[0]
        if method == CompressionMethod.HUFFMAN:
            huffman = HuffmanCompression()
            return huffman.decompress(compressed_data[1:])
        elif method == CompressionMethod.DEFLATE:
            return DeflateCompression.decompress(compressed_data)
        else:
            raise ValueError(f"Unsupported compression method: {method}")