#!/usr/bin/env python3
"""
Clean up the ue5_world_generator.py file by removing leftover C++ code
"""

def cleanup_ue5_generator():
    """Remove leftover C++ code from the Python file"""
    
    file_path = "ue5_world_generator.py"
    
    print("🧹 Cleaning up ue5_world_generator.py...")
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        print(f"📄 Original file has {len(lines)} lines")
        
        # Find the end of the JSON-based methods
        json_methods_end = -1
        for i, line in enumerate(lines):
            if "self.create_json_based_quest_classes(source_folder, world_data, safe_name)" in line:
                json_methods_end = i
                break
        
        if json_methods_end == -1:
            print("❌ Could not find end of JSON-based methods")
            return
        
        # Find the start of clean methods
        clean_methods_start = -1
        for i in range(json_methods_end + 1, len(lines)):
            if "def create_blueprint_files_with_embedded_data(self, world_folder, world_data, safe_name):" in lines[i]:
                clean_methods_start = i
                break
        
        if clean_methods_start == -1:
            print("❌ Could not find start of clean methods")
            return
        
        print(f"🔍 Found JSON methods end at line {json_methods_end + 1}")
        print(f"🔍 Found clean methods start at line {clean_methods_start + 1}")
        print(f"🗑️ Removing {clean_methods_start - json_methods_end - 1} lines of leftover code")
        
        # Create cleaned lines
        cleaned_lines = lines[:json_methods_end + 1]  # Keep up to JSON methods end
        cleaned_lines.append("\n")  # Add blank line
        cleaned_lines.extend(lines[clean_methods_start:])  # Add clean methods
        
        # Write cleaned file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(cleaned_lines)
        
        print(f"✅ Cleaned file now has {len(cleaned_lines)} lines")
        print(f"✅ Removed {len(lines) - len(cleaned_lines)} lines of leftover code")
        
    except Exception as e:
        print(f"❌ Error cleaning file: {e}")

if __name__ == "__main__":
    cleanup_ue5_generator()
