# The raw input string provided
raw_input = """
impassable_mountains = LIST { 13531 13523 13517 13516 13515 10772 10778 13560 13561 13562 13563 13564 13541 13542 13544 13545 13867 13874 13885 14097 14101 14102 14104 10417 10418 10419 11680 11683 13054 13078 13244 13427 13344 13801 }
"""

def sort_bracket_content(text):
    # Find the start and end of the bracketed content
    start_index = text.find('{')
    end_index = text.rfind('}')

    if start_index == -1 or end_index == -1:
        return "Error: Could not find brackets { } in the text."

    # Extract the content inside the brackets
    inner_content = text[start_index + 1:end_index]

    # Convert strings to integers for proper numerical sorting
    # This also handles arbitrary whitespace (newlines, tabs, spaces)
    try:
        numbers = [int(x) for x in inner_content.split()]
    except ValueError:
        return "Error: The list contains non-integer values."

    # Sort the numbers
    numbers.sort()

    # Join them back into a string
    sorted_content = " ".join(map(str, numbers))

    # Reconstruct the final string
    # We keep the "impassable_mountains = LIST { " part and the closing " }"
    result = f"impassable_mountains = LIST {{ {sorted_content} }}"
    
    return result

if __name__ == "__main__":
    # Process the string
    sorted_string = sort_bracket_content(raw_input)
    
    # Print to console
    print("Sorted List:")
    print(sorted_string)
    
    # Save to file
    with open("sorted_mountains.txt", "w") as f:
        f.write(sorted_string)
    print("\nResult has also been saved to 'sorted_mountains.txt'")