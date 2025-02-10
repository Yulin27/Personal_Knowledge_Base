def parse_title_kw_summary(text:str):
    """
    Parse the title, keywords and summary from the text.
    :param text: The text to parse.
    """
    # Split the text into lines
    lines = text.split("\n")
    
    # Initialize the title, keywords and summary
    title = None
    keywords = None
    summary = None
    
    # Loop through the lines
    for line in lines:
        # Check if the line contains the title
        if "Title:" in line:
            title = line.replace("Title:", "").strip()
        # Check if the line contains the keywords
        if "Key Words:" in line:
            keywords = line.replace("Key Words:", "").strip()
            keywords = keywords.split(",")
        # Check if the line contains the summary
        if "Summary:" in line:
            summary = line.replace("Summary:", "").strip()

    # Verify that all the fields are present
    if title is None or keywords is None or summary is None:
        raise ValueError("title, keywords or summary not found in the text.")

    result = {"title": title, "keywords": keywords, "summary": summary}
    return result

