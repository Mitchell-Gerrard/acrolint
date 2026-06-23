import re

def file_text_extract(file_path):
    """
    Extracts the text content from a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The text content of the file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return ""
def regex_extract(pattern, text):
    """
    Extracts all matches of a regex pattern from the given text.

    Args:
        pattern (str): The regex pattern to search for.
        text (str): The text to search within.
    
    Returns:
        list: A list of all matches found.
    """
    try:
        return re.findall(pattern, text)
    except re.error as e:
        print(f"Regex error: {e}")
        return []
def collect_acronyms(text):
    """
    Collects all acronyms from the specified file.

    Args:
        file_path (str): The path to the file.
    
    Returns:
        list: A list of all acronyms found.
    """
    
    # Simple regex to find acronyms (uppercase letters)
    return regex_extract(r'\b[A-Z]{2,}\b', text)
def find_acronym_definitions(files):
    """
    Finds acronym definitions in the given text.

    Args:
        text (str): The text to search within.
    
    Returns:
        list: A list of all acronym definitions found.
    """
    results = []
    for file in files:
        text = file_text_extract(file)
        patterns = [
        r'([A-Z][A-Za-z\s\-&]+)\s*\(([A-Z]{2,10})\)',
        r'\b([A-Z]{2,10})\s*\(([A-Z][A-Za-z\s\-&]+)\)']
        for pattern in patterns:
            results.extend(regex_extract(pattern, text))
    return results


def find_undefined_acronyms(files, defined_acronyms):
    all_acronyms = []
    for file in files:
        text = file_text_extract(file)
        all_acronyms.extend(collect_acronyms(text))
    all_unique_acronyms = set(all_acronyms)
    defined_acronyms_short = [acronym[0] for acronym in defined_acronyms]

    return [acronym for acronym in all_unique_acronyms if acronym not in defined_acronyms_short]
def index_to_line(text, index):
    return text[:index].count("\n") + 1
def firstusage(files, pattern):
    result = []
    for file in files:
        print(file)
        text = file_text_extract(file)

        for match in re.finditer(pattern, text):
            result.append(
                index_to_line(text, match.start())
                )
                
        if match:
            break  # Stop searching after the first match in the current file
    return result[0], file
def output_file(file_path, orgonised_data):
    if file_path.endswith(".json"):
        import json
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(orgonised_data, f, indent=4)
def acrolint(file_paths):
    """
    Main function to process the given file paths and find acronyms and their definitions.

    Args:
        file_paths (list): A list of file paths to process.
    Returns:
        dict: A dictionary containing acronyms, their definitions, and first usage information.
    """
    orgonised_data = {}
    acronyms = find_acronym_definitions(file_paths)
    undefined_acronyms = find_undefined_acronyms(file_paths, acronyms)

    for acronym in undefined_acronyms:
        first_usage = firstusage(file_paths, r'\b' + re.escape(acronym) + r'\b')
        orgonised_data[acronym] = {
            "definition": None,
            "first_usage": first_usage,
            "defined": False
        }

    for acronym in acronyms:
        first_usage = firstusage(file_paths, r'\b' + re.escape(acronym[0]) + r'\b')
        orgonised_data[acronym[0]] = {
            "definition": acronym[1],
            "first_usage": first_usage,
            "defined": True
        }
    return orgonised_data

def main():
    # Example usage
    file_paths = ["tests/test_files/main.tex"]  # Replace with your file paths
    acronyms = find_acronym_definitions(file_paths)
    undefined_acronyms = find_undefined_acronyms(file_paths, acronyms)
    orgonised_data = {}
    for acronym in undefined_acronyms:
        first_usage = firstusage(file_paths, r'\b' + re.escape(acronym) + r'\b')
        orgonised_data[acronym] = {
            "definition": None,
            "first_usage": first_usage,
            "defined": False
        }
    for acronym in acronyms:
        first_usage = firstusage(file_paths, r'\b' + re.escape(acronym[0]) + r'\b')
        orgonised_data[acronym[0]] = {
            "definition": acronym[1],
            "first_usage": first_usage,
            "defined": True
        }
    output_file("tests/test_files/output.json", orgonised_data)
