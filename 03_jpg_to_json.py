"""
This script processes image files from the '02_pdf_img/' directory and converts them into JSON files using an AI model.

Key Features:
- Reads `.jpg` files from the '02_pdf_img/' directory.
- Converts images to Base64 format for AI processing.
  Base 64 is simply a textual representation of an image.
- Sends the Base64-encoded images to an AI model for parsing using an OCR strategy.
- Saves the AI-generated JSON output to the '03_pdf_json/' directory.
- Skips processing for files that already exist in the output directory.

Dependencies:
- `openai` library: Install it using `pip install openai`.
- An API key for the OpenAI client, stored in a `.api_key` file.
- A prompt file (`03_newsletter extraction prompt.txt`) to guide the AI model.
"""

from pathlib import Path
import base64
from openai import OpenAI
import glob

# Load API key and initialize OpenAI client
with open(".api_key", "r") as f:
    api_key = f.read().strip()

client = OpenAI(api_key=api_key)

# Select AI model
model = ["gpt-4o-mini", "gpt-5-mini"][1]

# Load the prompt for AI processing
with open("03_newsletter extraction prompt.txt", "r") as f:
    prompt = f.read().strip()

# Initialize AI context for stateful responses
initial = client.responses.create(
    model=model,
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": prompt
                }
            ]
        }
    ]
)

context_id = initial.id

# Function to convert an image to Base64 format
def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# Function to send Base64 image to AI and get parsed JSON
def ai_parse(image_b64):
    response = client.responses.create(
        model=model,
        previous_response_id=context_id,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{image_b64}"
                    }
                ]
            }
        ]
    )

    return response.output_text

# Process images and save JSON output
for src in glob.glob('02_pdf_img/*'):
    print(src)  # Log the source file path

    src_out = Path('03_pdf_json') / (Path(src).stem + '.json')

    if src_out.exists():
        print(f"Skipping existing file: {src_out}")
    else:
        image_b64 = image_to_base64(src)
        
        text = ai_parse(image_b64)
        text = text.replace("```json", "").replace("```", "")
        
        with open(src_out, "a") as f:
            f.write(text)
