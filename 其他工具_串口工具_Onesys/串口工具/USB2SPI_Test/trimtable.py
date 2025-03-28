# trimtable.py

class TrimTable:
    def __init__(self, input_data=None, input_type='hex'):
        self.bit_length = 144
        self.data_int = 0  # Store the integer representation
        self.data_hex = ''  # Store the hexadecimal representation
        self.data_bin = ''  # Store the binary string with '0b' prefix
        self.data_bin_str = ''  # Store the binary string without '0b' prefix
        if input_data is not None:
            if input_type == 'hex':
                self.from_hex(input_data)
            elif input_type == 'int':
                self.from_int(input_data)
            elif input_type == 'bin':
                self.from_bin(input_data)
            elif input_type == 'bin_str':
                self.from_bin_str(input_data)
            else:
                raise ValueError("Invalid input_type specified")
            self._update_all()

    def _update_all(self):
        """Update all representations based on the current integer value."""
        self.data_hex = f'{self.data_int:0{self.bit_length // 4}X}'
        self.data_bin = f'{self.data_int:0{self.bit_length}b}'
        self.data_bin_str = self.data_bin.lstrip('0')

    def from_int(self, integer):
        if integer >= 2 ** self.bit_length:
            raise ValueError(f"Integer too large for {self.bit_length} bits")
        self.data_int = integer
        self._update_all()

    def from_hex(self, hex_str):
        self.data_int = int(hex_str, 16)
        self._update_all()

    def from_bin(self, bin_str):
        self.data_int = int(bin_str, 2)
        self._update_all()

    def from_bin_str(self, bin_str_no_prefix):
        self.data_int = int(bin_str_no_prefix, 2)
        self._update_all()

    def to_int(self):
        return self.data_int

    def to_hex(self):
        return self.data_hex

    def to_bin(self):
        return self.data_bin

    def to_bin_str(self):
        return self.data_bin_str

    def set_bit(self, position, value):
        if position < 0 or position >= self.bit_length:
            raise ValueError("Bit position out of range")
        if value not in [0, 1]:
            raise ValueError("Bit value must be 0 or 1")
        if value == 1:
            self.data_int |= (1 << position)
        else:
            self.data_int &= ~(1 << position)
        self._update_all()

    def set_IBIAS(self, IBIAS_str='100'):
        bit_positions = [31,30,29]

        if len(IBIAS_str) != len(bit_positions):
            raise ValueError(f"IBIAS_str 的长度必须为 {len(bit_positions)}")

        for idx, num in enumerate(bit_positions):
            self.set_bit(num, int(IBIAS_str[idx]))

    def set_IBLC(self, IBLC_str='1010'):
        bit_positions = [71, 70, 69, 68]

        if len(IBLC_str) != len(bit_positions):
            raise ValueError(f"IBLC_str 的长度必须为 {len(bit_positions)}")

        for idx, num in enumerate(bit_positions):
            self.set_bit(num, int(IBLC_str[idx]))

    def set_HRVFY(self, HRVFY_str='110010'):
        HRVFY_str = HRVFY_str[1:]
        bit_positions = [86, 85, 84, 83, 82]

        if len(HRVFY_str) != len(bit_positions):
            raise ValueError(f"HRVFY_str 的长度必须为 {len(bit_positions)+1}")

        for idx, num in enumerate(bit_positions):
            self.set_bit(num, int(HRVFY_str[idx]))

    def set_RDREF(self,RDREF_str='101010'):
        bit_positions = [81, 80, 95, 94, 93, 92]

        # 确保 RDREF_str 的长度与 bit_positions 相同
        if len(RDREF_str) != len(bit_positions):
            raise ValueError(f"RDREF_str 的长度必须为 {len(bit_positions)}")

        for idx, num in enumerate(bit_positions):
            self.set_bit(num, int(RDREF_str[idx]))

    def set_LRVFY(self, LRVFY_str='100010'):

        bit_positions = [91, 90, 89, 88, 103, 102]

        if len(LRVFY_str) != len(bit_positions):
            raise ValueError(f"LRVFY_str 的长度必须为 {len(bit_positions)}")

        for idx, num in enumerate(bit_positions):
            self.set_bit(num, int(LRVFY_str[idx]))

    def set_FORMVFY(self, FORMVFY_str='100010'):

        bit_positions = [101, 100, 99, 98, 97, 96]

        if len(FORMVFY_str) != len(bit_positions):
            raise ValueError(f"FORMVFY_str 的长度必须为 {len(bit_positions)}")

        for idx, num in enumerate(bit_positions):
            self.set_bit(num, int(FORMVFY_str[idx]))

    def get_bit(self, position):
        if position < 0 or position >= self.bit_length:
            raise ValueError("Bit position out of range")
        return (self.data_int >> position) & 1

    def hex_display(self):
        """Returns the hex representation with underscores every two characters."""
        return '_'.join(self.data_hex[i:i + 2] for i in range(0, len(self.data_hex), 2))

# Example usage:
if __name__ == '__main__':
    hex_string = 'AA8804FDFDA2A84A6F7FC0F7551C9C208410'
    table = TrimTable(hex_string, 'hex')

    print("Integer:", table.to_int())
    print("Hex:", table.to_hex())
    print("Hex Display:", table.hex_display())
    print("Binary:", table.to_bin())
    print("Binary (no prefix):", table.to_bin_str())

    table.set_bit(0, 1)
    print("After setting bit 0 to 1:")
    print("Integer:", table.to_int())
    print("Hex:", table.to_hex())
    print("Hex Display:", table.hex_display())
    print("Binary:", table.to_bin())
    print("Binary (no prefix):", table.to_bin_str())

    print("Bit at position 0:", table.get_bit(0))
