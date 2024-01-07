# RPA Library Documentation

## Folder Structure

The RPA Library follows a modular structure with three main folders: `email`, `file`, and `selector`. The current structure is as follows:

### 1. Email

- **Folder Name:** `email`
- **Virtual Environment:** `env_email`
- **Files:**
  - `globalemail.py`: Contains email-related functionalities.

### 2. File

- **Folder Name:** `file`
- **Virtual Environment:** `env_file`
- **Files:**
  - `global_files.py`: Includes file-related functionalities.

### 3. Selector

- **Folder Name:** `selector`
- **Virtual Environment:** `env_selector`
- **Files:**
  - `global.py`: Houses selector functionalities.

## Global Environment

- **Virtual Environment for the RPA Library:** `env_global_rpa_lib`

## Installation Instructions

To install dependencies for each module, use the respective virtual environments. For example, for the `email` module:

```bash
pip install -r email/requirements.txt
```

Repeat the same process for the file and selector modules.

## Global RPA Library

To install global dependencies for the entire RPA Library, you can use the provided `env_global_rpa_lib` virtual environment. Run the following command:

```bash
pip install -r env_global_rpa_lib/requirements.txt
```

## Usage

After installing the required dependencies, you can use the RPA Library modules in your Python script as follows:
```bash
pip install -r env_global_rpa_lib/requirements.txt
```

```python
from GlobalRPA_Lib import GlobalEmail, GlobalFiles, GlobalSelector
```