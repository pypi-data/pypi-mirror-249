import unittest
import os
from filechunkcrud import FileHandler

class TestFileHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Creating a temporary file for testing
        cls.test_file_path = "test_file.txt"
        with open(cls.test_file_path, "w") as file:
            file.write("Hello, World!\nThis is a test file.")

    @classmethod
    def tearDownClass(cls):
        # Removing the temporary file after testing
        if os.path.exists(cls.test_file_path):
            os.remove(cls.test_file_path)

    def test_read_chunks(self):
        file_handler = FileHandler(self.test_file_path)
        content = ""
        for chunk in file_handler.read_chunks(chunk_size=5):
            content += chunk
        self.assertEqual(content, "Hello, World!\nThis is a test file.")

    def test_create_large_file(self):
        # Testing creation of a large file using generator
        large_file_path = "large_test_file.txt"
        file_handler = FileHandler(large_file_path)

        def large_content_generator(size):
            for i in range(size):
                yield f"Line {i}\n"

        file_handler.create_file(large_content_generator(1_000_000))  # For example, 1_000_000 lines

        with open(large_file_path, "r") as file:
            lines = file.readlines()
        self.assertEqual(len(lines), 1_000_000)
        os.remove(large_file_path)  # Removing the large file after the test

    def test_update_file(self):
        # Testing update file with additional content
        file_handler = FileHandler(self.test_file_path)
        file_handler.update_file("\nAdditional content")
        with open(self.test_file_path, "r") as file:
            content = file.read()
        self.assertIn("Additional content", content)

    def test_delete_file(self):
        # Testing file deletion
        temp_file_path = "temp_file.txt"
        with open(temp_file_path, "w") as file:
            file.write("Temporary file.")
        file_handler = FileHandler(temp_file_path)
        file_handler.delete_file()
        self.assertFalse(os.path.exists(temp_file_path))

if __name__ == '__main__':
    unittest.main()
