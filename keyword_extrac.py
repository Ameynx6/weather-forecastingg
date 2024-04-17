import spacy
from spacy.matcher import Matcher
from spacy.tokens import Span

nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)

# Define the pattern for dates in MM/DD/YYYY format
date_pattern = [{"TEXT": {"REGEX": "\d{2}/\d{2}/\d{4}"}}]

# Add the pattern to the matcher
matcher.add("DATE", [date_pattern])

# Define the patterns for other date expressions
# Define the patterns for other date expressions
# Define the patterns for other date expressions
custom_patterns = [
    [{"LOWER": "next"}, {"LOWER": "day"}],
    [{"LOWER": "today"}],
    [{"LOWER": "tomorrow"}],
    [{"LOWER": {"IN": ["yesterday", "prior"]}}],
    [{"LOWER": {"IN": ["before", "prior", "ago"]}}, {"TEXT": {"REGEX": "\\d+"}}, {"LOWER": "days"}],
    [{"LOWER": "after"}, {"TEXT": {"REGEX": "\\d+"}}, {"LOWER": "days"}]
]



# Add the custom patterns to the matcher
matcher.add("CUSTOM_DATE", custom_patterns)

# Function to extract dates from text
def extract_dates(text):
    doc = nlp(text)
    matches = matcher(doc)
    dates = []
    for match_id, start, end in matches:
        span = doc[start:end]
        dates.append(span.text)
    return dates

# Test the function with different expressions
expressions = [
    "The meeting is scheduled for the next day.",
    "The meeting is scheduled for today.",
    "The meeting is scheduled for tomorrow.",
    "The meeting is scheduled for 2 days before.",
    "The meeting is scheduled for after 2 days."
]

for expression in expressions:
    dates = extract_dates(expression)
    print(f"For the expression '{expression}', extracted dates: {dates}")
