# Asaniczka

The Asaniczka module provides quick functions to get up and running with a scraper.

## Available Functions:

1. `setup_logger()`: Set up a logger and return the logger instance.
2. `save_temp_file()`: Saves the given content to a temporary file in the specified temp folder.
3. `format_error()`: Removes newlines from the given error string.
4. `get_request()`: Makes a basic HTTP GET request to the given URL.
5. `create_dir()`: Creates a new directory.

## Available Classes:

1. `ProjectSetup`: A class that sets up project folders and provides access to their paths.

## Installation

To install Asaniczka, you can use pip:

pip install asaniczka

## Usage

```python
python import asaniczka

# Set up a logger
logger = asaniczka.setup_logger("/path/to/log/file.log")

# Save content to a temporary file
asaniczka.savetempfile(content, extension='txt', file_name=None)

# Format an error
formattederror = asaniczka.formaterror(error)

# Make a GET request
responsecontent = asaniczka.getrequest(url)

# Create a new directory
asaniczka.createdir(folderpath)

# Create project folders
project = asaniczka.ProjectSetup("MyProject")

```
