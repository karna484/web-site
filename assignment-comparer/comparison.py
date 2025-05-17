import difflib
from collections import defaultdict
import os

def compare_folder_contents(file_paths):
    try:
        # Read all files
        file_contents = {}
        for path in file_paths:
            with open(path, 'r', encoding='utf-8') as f:
                file_contents[os.path.basename(path)] = f.read()
        
        # Compare all pairs
        similarity_matrix = defaultdict(dict)
        all_matches = defaultdict(list)
        filenames = list(file_contents.keys())
        
        for i in range(len(filenames)):
            for j in range(i+1, len(filenames)):
                file1 = filenames[i]
                file2 = filenames[j]
                text1 = file_contents[file1]
                text2 = file_contents[file2]
                
                # Calculate similarity
                matcher = difflib.SequenceMatcher(None, text1, text2)
                similarity = round(matcher.ratio() * 100, 2)
                similarity_matrix[file1][file2] = similarity
                similarity_matrix[file2][file1] = similarity
                
                # Find matching blocks
                for block in matcher.get_matching_blocks():
                    if block.size > 10:  # Only consider matches longer than 10 chars
                        match_text = text1[block.a:block.a+block.size]
                        all_matches[match_text].append((file1, file2))
        
        # Prepare highlighted results
        highlighted_results = []
        for match_text, files in all_matches.items():
            if len(files) > 1:  # Only show matches found in multiple files
                file_list = ", ".join(set(f"{f1} and {f2}" for f1, f2 in files))
                highlighted_results.append({
                    'text': match_text,
                    'files': file_list,
                    'count': len(set(f for pair in files for f in pair))
                })
        
        # Sort by most common matches
        highlighted_results.sort(key=lambda x: (-x['count'], x['text']))
        
        return {
            'similarity_matrix': similarity_matrix,
            'common_matches': highlighted_results,
            'total_files': len(filenames)
        }
    
    except Exception as e:
        raise Exception(f"Error comparing folder contents: {str(e)}")