#!/usr/bin/env python3
"""
Chart Image Indexer and Duplicate Renamer

This script:
1. Finds all PNG files in the workspace
2. Creates an index organized by folder
3. Detects duplicate filenames and renumbers them
4. Generates both a text index and JSON index
"""

import os
import json
from pathlib import Path
from collections import defaultdict
import shutil

def find_all_png_files(root_dir):
    """Find all PNG files in the directory tree."""
    png_files = []
    root_path = Path(root_dir)
    
    for png_file in root_path.rglob("*.png"):
        if png_file.is_file():
            png_files.append(png_file)
    
    return png_files

def organize_by_folder(png_files, root_dir):
    """Organize PNG files by their folder paths."""
    root_path = Path(root_dir)
    folder_index = defaultdict(list)
    
    for png_file in png_files:
        # Get relative folder path
        relative_path = png_file.relative_to(root_path)
        folder_path = str(relative_path.parent) if relative_path.parent != Path('.') else "root"
        
        folder_index[folder_path].append({
            'filename': png_file.name,
            'full_path': str(png_file),
            'relative_path': str(relative_path)
        })
    
    return folder_index

def detect_and_handle_duplicates(folder_index, rename_mode='dry_run'):
    """
    Detect duplicate filenames across folders and handle them.
    
    Args:
        folder_index: Dictionary of folders and their PNG files
        rename_mode: 'dry_run' (just report), 'rename' (actually rename files)
    
    Returns:
        Dictionary with duplicate information and rename operations
    """
    # Track all filenames across all folders
    filename_locations = defaultdict(list)
    
    for folder, files in folder_index.items():
        for file_info in files:
            filename_locations[file_info['filename']].append({
                'folder': folder,
                'full_path': file_info['full_path']
            })
    
    # Find duplicates (files that appear in multiple locations)
    duplicates = {name: locations for name, locations in filename_locations.items() 
                  if len(locations) > 1}
    
    rename_operations = []
    
    if rename_mode == 'rename' and duplicates:
        print("\n🔄 RENAMING DUPLICATE FILES...")
        
        for filename, locations in duplicates.items():
            # Keep the first one as-is, rename others with numbers
            for idx, location in enumerate(locations):
                if idx == 0:
                    # Keep first occurrence as-is
                    continue
                
                old_path = Path(location['full_path'])
                stem = old_path.stem
                suffix = old_path.suffix
                
                # Create new filename with number
                new_filename = f"{stem}_{idx}{suffix}"
                new_path = old_path.parent / new_filename
                
                # Handle case where numbered file already exists
                counter = idx
                while new_path.exists():
                    counter += 1
                    new_filename = f"{stem}_{counter}{suffix}"
                    new_path = old_path.parent / new_filename
                
                try:
                    shutil.move(str(old_path), str(new_path))
                    rename_operations.append({
                        'old_path': str(old_path),
                        'new_path': str(new_path),
                        'status': 'success'
                    })
                    print(f"  ✓ Renamed: {old_path.name} → {new_filename}")
                    print(f"    Location: {location['folder']}")
                except Exception as e:
                    rename_operations.append({
                        'old_path': str(old_path),
                        'new_path': str(new_path),
                        'status': 'failed',
                        'error': str(e)
                    })
                    print(f"  ✗ Failed to rename {old_path.name}: {e}")
    
    return duplicates, rename_operations

def create_index_report(folder_index, duplicates, output_file='chart_index.txt'):
    """Create a human-readable index report."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("CHART IMAGE INDEX\n")
        f.write(f"Generated: {Path.cwd()}\n")
        f.write("=" * 80 + "\n\n")
        
        # Summary statistics
        total_files = sum(len(files) for files in folder_index.values())
        total_folders = len(folder_index)
        
        f.write(f"📊 SUMMARY\n")
        f.write(f"  Total PNG files: {total_files}\n")
        f.write(f"  Total folders: {total_folders}\n")
        f.write(f"  Duplicate filenames: {len(duplicates)}\n")
        f.write("\n" + "=" * 80 + "\n\n")
        
        # Duplicates section
        if duplicates:
            f.write("⚠️  DUPLICATE FILENAMES\n")
            f.write("-" * 80 + "\n")
            for filename, locations in sorted(duplicates.items()):
                f.write(f"\n📄 {filename} (found in {len(locations)} locations):\n")
                for loc in locations:
                    f.write(f"  • {loc['folder']}\n")
            f.write("\n" + "=" * 80 + "\n\n")
        
        # Folder index
        f.write("📁 FOLDER INDEX\n")
        f.write("-" * 80 + "\n\n")
        
        for folder in sorted(folder_index.keys()):
            files = folder_index[folder]
            f.write(f"\n📂 {folder}/ ({len(files)} files)\n")
            f.write("-" * 80 + "\n")
            for file_info in sorted(files, key=lambda x: x['filename']):
                f.write(f"  • {file_info['filename']}\n")
    
    return output_file

def create_json_index(folder_index, duplicates, rename_operations, output_file='chart_index.json'):
    """Create a machine-readable JSON index."""
    index_data = {
        'summary': {
            'total_files': sum(len(files) for files in folder_index.values()),
            'total_folders': len(folder_index),
            'duplicate_count': len(duplicates)
        },
        'duplicates': {
            filename: [{'folder': loc['folder'], 'path': loc['full_path']} 
                      for loc in locations]
            for filename, locations in duplicates.items()
        },
        'folders': {
            folder: [{'filename': f['filename'], 'path': f['full_path']} 
                    for f in files]
            for folder, files in folder_index.items()
        },
        'rename_operations': rename_operations
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2)
    
    return output_file

def create_html_viewer(folder_index, duplicates, rename_operations, output_file='chart_viewer.html'):
    """Create an HTML viewer with embedded JSON data (no CORS issues)."""
    
    # Prepare the data structure
    index_data = {
        'summary': {
            'total_files': sum(len(files) for files in folder_index.values()),
            'total_folders': len(folder_index),
            'duplicate_count': len(duplicates)
        },
        'duplicates': {
            filename: [{'folder': loc['folder'], 'path': loc['full_path']} 
                      for loc in locations]
            for filename, locations in duplicates.items()
        },
        'folders': {
            folder: [{'filename': f['filename'], 'path': f['full_path']} 
                    for f in files]
            for folder, files in folder_index.items()
        },
        'rename_operations': rename_operations
    }
    
    # Read the HTML template
    html_template = Path('chart_viewer.html').read_text()
    
    # Embed JSON data into the HTML
    json_data = json.dumps(index_data, indent=2)
    
    # Replace the fetch call with embedded data
    modified_html = html_template.replace(
        '        // Load JSON data\n        async function loadChartData() {\n            try {\n                const response = await fetch(\'chart_index.json\');\n                chartData = await response.json();',
        f'        // Load JSON data\n        async function loadChartData() {{\n            try {{\n                // Embedded JSON data (no CORS issues)\n                chartData = {json_data};'
    )
    
    # Write the modified HTML
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(modified_html)
    
    return output_file

def main():
    # Get the workspace root (current directory or parent)
    workspace_root = Path.cwd()
    
    print("=" * 80)
    print("📊 CHART IMAGE INDEXER AND DUPLICATE RENAMER")
    print("=" * 80)
    print(f"\n🔍 Scanning directory: {workspace_root}\n")
    
    # Step 1: Find all PNG files
    print("Step 1: Finding all PNG files...")
    png_files = find_all_png_files(workspace_root)
    print(f"  ✓ Found {len(png_files)} PNG files\n")
    
    # Step 2: Organize by folder
    print("Step 2: Organizing by folder...")
    folder_index = organize_by_folder(png_files, workspace_root)
    print(f"  ✓ Organized into {len(folder_index)} folders\n")
    
    # Step 3: Detect duplicates (dry run first)
    print("Step 3: Detecting duplicate filenames...")
    duplicates, _ = detect_and_handle_duplicates(folder_index, rename_mode='dry_run')
    
    if duplicates:
        print(f"  ⚠️  Found {len(duplicates)} duplicate filenames:\n")
        for filename, locations in list(duplicates.items())[:5]:  # Show first 5
            print(f"    • {filename} ({len(locations)} copies)")
        if len(duplicates) > 5:
            print(f"    ... and {len(duplicates) - 5} more")
        
        # Ask user if they want to rename
        print("\n" + "=" * 80)
        response = input("\n❓ Do you want to rename duplicate files? (yes/no): ").strip().lower()
        
        rename_operations = []
        if response in ['yes', 'y']:
            duplicates, rename_operations = detect_and_handle_duplicates(folder_index, rename_mode='rename')
            # Re-scan after renaming
            png_files = find_all_png_files(workspace_root)
            folder_index = organize_by_folder(png_files, workspace_root)
            print(f"\n  ✓ Renamed {len(rename_operations)} files\n")
        else:
            print("\n  ℹ️  Skipping rename operation\n")
    else:
        print("  ✓ No duplicate filenames found\n")
        rename_operations = []
    
    # Step 4: Create index reports
    print("Step 4: Creating index reports...")
    txt_file = create_index_report(folder_index, duplicates, 'chart_index.txt')
    json_file = create_json_index(folder_index, duplicates, rename_operations, 'chart_index.json')
    html_file = create_html_viewer(folder_index, duplicates, rename_operations, 'chart_viewer.html')
    
    print(f"  ✓ Text index: {txt_file}")
    print(f"  ✓ JSON index: {json_file}")
    print(f"  ✓ HTML viewer: {html_file}\n")
    
    print("=" * 80)
    print("✅ COMPLETE!")
    print("=" * 80)
    print(f"\n📄 View the index: {txt_file}")
    print(f"📄 JSON data: {json_file}")
    print(f"🌐 Open in browser: {html_file}\n")

if __name__ == "__main__":
    main()
