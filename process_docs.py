import json
import re
import os
import glob

def process_markdown_files():
    """
    Reads all markdown files in the docs/ directory, splits them into chunks based on headings,
    and saves the structured data to a JSON file.
    """
    # Use Python's glob to find all markdown files
    # The path should be relative to where the script is run
    base_path = 'docs'
    file_paths = glob.glob(os.path.join(base_path, '**', '*.md'), recursive=True)

    if not file_paths:
        print("No markdown files found in the docs/ directory.")
        return

    all_chunks = []
    # Regex to find markdown headings (H1, H2, H3)
    heading_pattern = re.compile(r"^(#{1,3})\s(.+)", re.MULTILINE)

    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.strip():
                continue

            # Find all headings
            headings = list(heading_pattern.finditer(content))
            
            if not headings:
                # If no headings, treat the whole file as one chunk
                all_chunks.append({
                    "source": file_path.replace('\\', '/'),
                    "heading": os.path.basename(file_path),
                    "content": content.strip()
                })
                continue

            # Split content by headings
            # First chunk is the content before the first heading
            first_heading_start = headings[0].start()
            if first_heading_start > 0:
                 all_chunks.append({
                    "source": file_path.replace('\\', '/'),
                    "heading": os.path.basename(file_path), # Use filename as heading for intro content
                    "content": content[:first_heading_start].strip()
                })

            for i, match in enumerate(headings):
                start_pos = match.end()
                end_pos = headings[i + 1].start() if i + 1 < len(headings) else len(content)
                
                heading_text = match.group(2).strip()
                chunk_content = content[start_pos:end_pos].strip()

                if chunk_content:
                    all_chunks.append({
                        "source": file_path.replace('\\', '/'),
                        "heading": heading_text,
                        "content": chunk_content
                    })

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

    # Write the output to a JSON file
    output_filename = 'processed_docs.json'
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print(f"Successfully processed {len(file_paths)} files and created {len(all_chunks)} chunks.")
    print(f"Output saved to {output_filename}")

if __name__ == "__main__":
    process_markdown_files()