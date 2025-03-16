import json
import argparse

def convert_to_chat_format(input_file, output_file, system_message="You are a rap lyric generator."):
    """
    Convert a JSONL file from prompt/completion format to messages format for OpenAI chat fine-tuning.
    
    Args:
        input_file (str): Path to the input JSONL file
        output_file (str): Path to save the output JSONL file
        system_message (str): The system message to include in each example
    """
    converted_data = []
    
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                # Parse the JSON line
                item = json.loads(line.strip())
                
                # Check if the line is already in the new format
                if "messages" in item:
                    converted_data.append(item)
                    continue
                
                # Check if the line has prompt and completion fields
                if "prompt" in item and "completion" in item:
                    # Create new format
                    new_item = {
                        "messages": [
                            {"role": "system", "content": system_message},
                            {"role": "user", "content": item["prompt"].strip()},
                            {"role": "assistant", "content": item["completion"].strip()}
                        ]
                    }
                    
                    # Remove the leading space from the assistant's message if present
                    # OpenAI's old format had a leading space in completion
                    if new_item["messages"][2]["content"].startswith(" "):
                        new_item["messages"][2]["content"] = new_item["messages"][2]["content"][1:]
                    
                    # Remove "END" token if present
                    if new_item["messages"][2]["content"].endswith(" END"):
                        new_item["messages"][2]["content"] = new_item["messages"][2]["content"][:-4]
                    
                    converted_data.append(new_item)
                else:
                    print(f"Warning: Skipping line with missing fields: {line.strip()}")
                    
            except json.JSONDecodeError:
                print(f"Warning: Could not parse JSON in line: {line.strip()}")
    
    # Write the converted data to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in converted_data:
            f.write(json.dumps(item) + '\n')
    
    print(f"Conversion complete! Converted {len(converted_data)} examples to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert JSONL from prompt/completion to messages format")
    parser.add_argument("input_file", help="Path to the input JSONL file")
    parser.add_argument("output_file", help="Path to save the output JSONL file")
    parser.add_argument("--system", default="You are a rap lyric generator.", 
                        help="System message to include in each example")
    
    args = parser.parse_args()
    convert_to_chat_format(args.input_file, args.output_file, args.system)