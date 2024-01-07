import os
import openai
import re
import json
from itertools import combinations
from rich.progress import track

# Get the API key from the environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

# Check if the API key is not set
if not openai.api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set")

def distance(s1, s2):
    return len(set(s1) ^ set(s2))

def parse_raw_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    tests = []
    current_test = None

    # Wrap your iterable with track to show progress
    for line in track(lines, description="Parsing test steps..."):
        line = line.strip()
        test_id_match = re.search(r'✓ (.*)', line)
        test_step_match = re.search(r'(cy:.*)', line)
        if test_id_match:
            if current_test:
                tests.append(current_test)
            current_test = {'testId': test_id_match.group(1), 'testSteps': []}
        elif test_step_match and current_test:
            current_test['testSteps'].append(test_step_match.group(1))

    if current_test:
        tests.append(current_test)

    return tests

def summarize_steps(steps):
    # Define key actions or events that you want to extract
    key_actions = ['click', 'type', 'new url', 'assert']

    # Extract steps that contain key actions
    summarized_steps = [step for step in steps if any(action in step for action in key_actions)]

    # If less than 10 steps are included, add more steps until there are 10
    if len(summarized_steps) < 10:
        summarized_steps += steps[len(summarized_steps):10]

    return ' '.join(summarized_steps)



def can_merge(test1, test2, similarity_percentage):
    # Use the summarize_steps function to summarize the tests
    test1_summary = summarize_steps(test1)
    test2_summary = summarize_steps(test2)

    if similarity_percentage > 80:
        prompt = f"Can these two test cases be merged? If yes, suggest how.\n\nTest 1: {test1_summary}\nTest 2: {test2_summary}"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1000,
        )
        merge_suggestion = response.choices[0].text.strip(); # Extract the suggestion from the response
        print(merge_suggestion) 
        # Only generate a new test case if the OpenAI API suggests that the tests can be merged
        if "yes" in merge_suggestion.lower():
            # Directly split the merge_suggestion string by commas
            suggested_steps = merge_suggestion.split(', ')
            # Format the steps
            formatted_suggestion = '\n'.join(f"- {step.strip('')}" for step in suggested_steps)
            return formatted_suggestion
        else:
            return merge_suggestion
    else:
        return "No merge suggested due to low similarity"
    

# Parse all files first
raw_file_path = 'cypress-log.txt'
tests = parse_raw_file(raw_file_path)

# Convert each test to a tuple of (testId, testSteps) if testSteps has 5 or more steps
tests = [(test['testId'], test['testSteps']) for test in tests if len(test['testSteps']) >= 5]

# Save the parsed tests to a JSON file for debugging
with open('debug.json', 'w') as f:
    json.dump(tests, f, indent=4)

report = []
for i, ((test1_name, test1_steps), (test2_name, test2_steps)) in enumerate(combinations(tests, 2)):
    similarity = 1 - distance(test1_steps, test2_steps) / max(len(test1_steps), len(test2_steps))
    # Check if raw_similarity is less than 0 before calculating the percentage
    similarity_percentage = max(0, round(similarity * 100, 2))
    merge_suggestion = can_merge(test1_steps, test2_steps, similarity_percentage)
    print(merge_suggestion)
    comparison = {
        'Test 1': {
            'Name': test1_name,
            'Steps': test1_steps
        },
        'Test 2': {
            'Name': test2_name,
            'Steps': test2_steps
        },
        'Similarity': similarity_percentage,
        'Merge Suggestion': merge_suggestion
    }
    report.append(comparison)


report_json = json.dumps(report, indent=4)

# Generate an HTML file
with open('report.html', 'w') as f:
    f.write(f"""
<!DOCTYPE html>
<html>
<head>
    <title>Report</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
        <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f0f0;
        }}
        .container {{
            background-color: #fff;
            margin: 2em auto;
            padding: 2em;
            border-radius: 0.5em;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        h1 {{
            color: #333;
        }}
        h5 {{
            color: #666;
        }}
        pre {{
            background-color: #f9f9f9;
            padding: 1em;
            border-radius: 0.5em;
        }}
        .same-step {{
            color: green;
        }}
        .test-case {{
            margin-bottom: 1em;
            margin-left: 1em;
        }}
        .box {{
            width: auto;
            height: auto;
            /* Add other CSS properties as needed */
        }}
    </style>
</head>
<body>
    <div class="container box">
        <h1 class="my-4">Report</h1>
        <script>
        const mydata = {report_json};
        for(let i = 0; i < mydata.length; i++) {{
            let test1Title = mydata[i]["Test 1"]["Name"];
            let test1Steps = mydata[i]["Test 1"]["Steps"];
            let test2Title = mydata[i]["Test 2"]["Name"];
            let test2Steps = mydata[i]["Test 2"]["Steps"];
            let similarity = mydata[i]["Similarity"];
            let mergeSuggestion = mydata[i]["Merge Suggestion"]; 
        if (similarity >= 80) {{
            document.write("<div class='card my-4'><div class='card-body'>");
            document.write("<div class='row'><div class='col-sm-6'>");
            document.write("<h5 class='test-case'>" + test1Title + "</h5><pre>");
            for(let j = 0; j < test1Steps.length; j++) {{
                if(test2Steps.includes(test1Steps[j])) {{
                    document.write("<span class='same-step'>" + test1Steps[j] + "</span><br>");
                }} else {{
                    document.write(test1Steps[j] + "<br>");
                }}
            }}
            document.write("</pre></div><div class='col-sm-6'>");
            document.write("<h5 class='test-case'>" + test2Title + "</h5><pre>");
            for(let j = 0; j < test2Steps.length; j++) {{
                if(test1Steps.includes(test2Steps[j])) {{
                    document.write("<span class='same-step' style='color: green;'>" + test2Steps[j] + "</span><br>");
                }} else {{
                    document.write(test2Steps[j] + "<br>");
                }}
            }}
            document.write("</pre></div></div>");
            document.write("<p><strong>Similarity:</strong> " + similarity + "%</p>");
            if (mergeSuggestion) {{
                let suggestionParts = mergeSuggestion.split('. The modified version is as follows:\\n');
                let suggestionText = suggestionParts[0];
                let mergedTestCase = suggestionParts[1];
                document.write("<p><strong>Merge Suggestion:</strong> " + suggestionText + "</p>");
                if (mergedTestCase) {{
                    let steps = mergedTestCase.split(', ');
                    document.write("<ul>");
                    for(let j = 0; j < steps.length; j++) {{
                        document.write("<li> " + steps[j] + "</li>");
                    }}
                    document.write("</ul>");
                }}
            }}
            document.write("</div></div>");
        }}
        }}
        </script>
    </div>
</body>
</html>
    """)