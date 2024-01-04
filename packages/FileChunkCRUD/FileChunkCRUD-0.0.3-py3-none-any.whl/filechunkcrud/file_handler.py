class FileHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_chunks(self, chunk_size=1024):
        """Read large file in chunks with given size."""
        with open(self.file_path, 'r') as file:
            for chunk in iter(lambda: file.read(chunk_size), ''):
                yield chunk

    def create_file(self, content_generator):
        """Create a new file with the given content."""
        with open(self.file_path, 'w') as file:
            for content_chunk in content_generator:
                file.write(content_chunk)

    def update_file(self, content_generator):
        """Update an existing file with the given content."""
        with open(self.file_path, 'a') as file:
            for content_chunk in content_generator:
                file.write(content_chunk)

    def delete_file(self):
        """Delete the file."""
        import os
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
