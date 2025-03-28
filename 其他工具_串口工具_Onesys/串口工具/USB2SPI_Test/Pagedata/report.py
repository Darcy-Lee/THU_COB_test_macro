import os

class ErrorInfo:
    def __init__(self, line_num, column_num, char):
        self.line_num = line_num
        self.column_num = column_num
        self.char = char

    def __str__(self):
        return f"Line: {self.line_num}, Column: {self.column_num}, Char: {self.char}"


class FileChecker:
    def __init__(self, allowed_chars):
        self.allowed_chars = allowed_chars
        self.error_counts = {}

    def check_file(self, file_path):
        errors = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, start=1):
                    # Split the line into bytes
                    bytes_in_line = line.strip().split(' ')
                    for column_num, byte in enumerate(bytes_in_line, start=1):
                        if byte not in self.allowed_chars:
                            errors.append(ErrorInfo(line_num, column_num, byte))
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")

        if errors:
            self.error_counts[file_path] = errors

    def write_errors_to_file(self, output_file):
        with open(output_file, 'w') as out_file:
            for file_path, errors in self.error_counts.items():
                for error in errors:
                    out_file.write(f"File: {file_path}, {error}\n")
                out_file.write(f"{file_path} has {len(errors)} error(s)\n")

    def check_specific_files(self, files_to_check):
        for file in files_to_check:
            if os.path.isfile(file):
                self.check_file(file)
            else:
                print(f"File not found: {file}")


if __name__ == "__main__":
    allowed_chars = {'00', 'FF', '  '}  # Update the allowed chars list as needed
    checker = FileChecker(allowed_chars)
    files_to_check = [f"RRAMpage_SUBIP{i}.txt" for i in range(8)]  # List of specific files to check
    checker.check_specific_files(files_to_check)
    checker.write_errors_to_file('ErrorReport.txt')
    # os.rename('ErrorReport.txt1', 'ErrorReport.txt')
