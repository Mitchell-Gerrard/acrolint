import re
STOP_WORDS = {
    "a", "an", "the", "of", "in", "at", "to", "for", "and"
}

def clean_definition(definition, acronym):
    """ Cleans the definition by removing leading junk words and taking the last N words based on acronym length.
    
    Args: 
        definition (str): The definition string to clean.
        acronym (str): The acronym associated with the definition.
    Returns:
        str: The cleaned definition.
    
    """
    if acronym.endswith("s") and len(acronym) > 2:
        acronym = acronym[:-1]
    definition = definition.replace("-", " ")
    words = definition.strip().split()
    print(f"Cleaning definition: '{definition}' for acronym: '{acronym}'")
    # remove leading junk words
    words = [w for w in words if w.lower() not in STOP_WORDS]

    # heuristic: take last N words based on acronym length
    n = max(2, len(acronym))
    words = words[-(n):]
    print(f"Cleaned definition: '{' '.join(words)}'")
    return " ".join(words)
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
    return regex_extract(r'\b(?:[A-Z]{2,}|[0-9]+[A-Z]+|[A-Z]+[0-9]+)\b', text)
def find_acronym_definitions(files):
    """
    Finds acronym definitions in the given text.

    Args:
        text (str): The text to search within.
    
    Returns:
        list: A list of all acronym definitions found.
    """
    results = []
    ACRONYM_PATTERN = r"[A-Z]{2,15}s?"
    DEFINITION_PATTERN = r"[A-Za-z][A-Za-z0-9\s\-&,/]*"

    for file in files:
        text = file_text_extract(file)

        # Definition (ABC)
        for definition, acronym in re.findall(
            rf"({DEFINITION_PATTERN})\s*\(({ACRONYM_PATTERN})\)",
            text,
        ):
            definition = clean_definition(definition, acronym)
            results.append((acronym, definition))

        # ABC (Definition)
        for acronym, definition in re.findall(
            rf"\b({ACRONYM_PATTERN})\s*\(({DEFINITION_PATTERN})\)",
            text,
        ):
            definition = clean_definition(definition, acronym)
            results.append((acronym, definition))

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
    for file in files:
        text = file_text_extract(file)

        for match in re.finditer(pattern, text):
            return index_to_line(text, match.start()), file

    return None, None
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
