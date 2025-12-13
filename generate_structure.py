#!/usr/bin/env python3
"""
Generate project structure visualization and documentation.
"""

import os
from pathlib import Path

def generate_tree_structure(directory=".", prefix="", max_depth=3, current_depth=0):
    """Generate a tree structure of the project."""
    if current_depth >= max_depth:
        return ""
    
    items = []
    path = Path(directory)
    
    # Skip hidden directories and common ignore patterns
    skip_patterns = {
        '.git', '__pycache__', '.pytest_cache', 'node_modules', 
        '.vscode', '.idea', 'venv', '.venv', 'env'
    }
    
    try:
        for item in sorted(path.iterdir()):
            if item.name.startswith('.') and item.name not in {'.gitignore', '.kiro'}:
                continue
            if item.name in skip_patterns:
                continue
            items.append(item)
    except PermissionError:
        return ""
    
    structure = ""
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        current_prefix = "└── " if is_last else "├── "
        
        if item.is_dir():
            structure += f"{prefix}{current_prefix}📁 {item.name}/\n"
            extension = "    " if is_last else "│   "
            structure += generate_tree_structure(
                item, prefix + extension, max_depth, current_depth + 1
            )
        else:
            # Add file type emoji
            emoji = get_file_emoji(item.suffix)
            structure += f"{prefix}{current_prefix}{emoji} {item.name}\n"
    
    return structure

def get_file_emoji(suffix):
    """Get appropriate emoji for file type."""
    emoji_map = {
        '.py': '🐍',
        '.md': '📄',
        '.yml': '⚙️',
        '.yaml': '⚙️',
        '.json': '📋',
        '.txt': '📝',
        '.sh': '🔧',
        '.gitignore': '🚫',
        '.env': '🔐',
    }
    return emoji_map.get(suffix, '📄')

def count_files_by_type():
    """Count files by type in the project."""
    counts = {}
    total_lines = 0
    
    for root, dirs, files in os.walk('.'):
        # Skip hidden and cache directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in {'__pycache__', 'node_modules'}]
        
        for file in files:
            if file.startswith('.'):
                continue
                
            suffix = Path(file).suffix or 'no_extension'
            counts[suffix] = counts.get(suffix, 0) + 1
            
            # Count lines for code files
            if suffix in {'.py', '.md', '.yml', '.yaml', '.json'}:
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        total_lines += len(f.readlines())
                except:
                    pass
    
    return counts, total_lines

def generate_project_stats():
    """Generate project statistics."""
    file_counts, total_lines = count_files_by_type()
    
    stats = "## 📊 Project Statistics\n\n"
    stats += f"- **Total Lines of Code**: {total_lines:,}\n"
    stats += f"- **Python Files**: {file_counts.get('.py', 0)}\n"
    stats += f"- **Documentation Files**: {file_counts.get('.md', 0)}\n"
    stats += f"- **Configuration Files**: {file_counts.get('.yml', 0) + file_counts.get('.yaml', 0) + file_counts.get('.json', 0)}\n"
    stats += f"- **Test Files**: {len([f for f in os.listdir('.') if f.startswith('test_')])}\n\n"
    
    return stats

def main():
    """Generate complete project structure documentation."""
    print("🔍 Generating project structure...")
    
    # Generate tree structure
    tree = generate_tree_structure(".", max_depth=4)
    
    # Generate statistics
    stats = generate_project_stats()
    
    # Create comprehensive structure file
    content = f"""# 🏗️ Stock Moon Dashboard - Project Structure

{stats}

## 📁 Directory Tree

```
stock-moon-dashboard/
{tree}```

## 🎯 Key Directories

### `/src` - Core Application
Contains all Python modules for the dashboard functionality.

### `/.kiro` - Development Configuration  
Kiro IDE specifications and settings for the project.

### `/test_*.py` - Test Suite
Comprehensive testing files for all components.

## 🚀 Quick Navigation

- **Start Here**: `README.md`
- **Run App**: `python app.py`
- **Deploy**: `DEPLOYMENT.md`
- **Contribute**: `CONTRIBUTING.md`
- **API Docs**: `src/mcp_tools.py`

Generated on: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    # Write to file
    with open('STRUCTURE_OVERVIEW.md', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Generated STRUCTURE_OVERVIEW.md")
    print(f"📊 Found {len([f for f in os.listdir('.') if f.endswith('.py')])} Python files")
    print(f"📄 Found {len([f for f in os.listdir('.') if f.endswith('.md')])} Markdown files")

if __name__ == "__main__":
    main()