#!/usr/bin/env python3
"""
Fix Unicode characters in test files for Windows compatibility.
"""

import os
import re

def fix_unicode_in_file(filepath):
    """Fix Unicode characters in a file."""
    unicode_replacements = {
        '🔍': '[SEARCH]',
        '🔎': '[SEARCH]',
        '🧪': '[TEST]',
        '✅': '[OK]',
        '❌': '[ERROR]',
        '📊': '[CHART]',
        '🌙': '[MOON]',
        '🚀': '[ROCKET]',
        '📈': '[UP]',
        '💰': '[MONEY]',
        '🖥️': '[COMPUTER]',
        '🏭': '[FACTORY]',
        '🌕': '[FULL_MOON]',
        '🎯': '[TARGET]',
        '🎉': '[PARTY]',
        '🏁': '[FLAG]',
        '🔄': '[REFRESH]',
        '⚡': '[LIGHTNING]',
        '📱': '[PHONE]',
        '🕐': '[CLOCK]',
        '1️⃣': '[1]',
        '2️⃣': '[2]',
        '3️⃣': '[3]',
        '4️⃣': '[4]',
        '5️⃣': '[5]',
        '6️⃣': '[6]',
        '7️⃣': '[7]',
        '8️⃣': '[8]',
        '9️⃣': '[9]',
        '🔟': '[10]',
        '→': '->',
        '🌐': '[WEB]',
        '🔗': '[LINK]',
        '⚙️': '[GEAR]',
        '📋': '[CLIPBOARD]',
        '🔧': '[WRENCH]'
    }
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace Unicode characters
        for unicode_char, replacement in unicode_replacements.items():
            content = content.replace(unicode_char, replacement)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed Unicode in {filepath}")
        return True
        
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")
        return False

def main():
    """Fix Unicode in all test files."""
    test_files = [f for f in os.listdir('.') if f.startswith('test_') and f.endswith('.py')]
    
    for test_file in test_files:
        fix_unicode_in_file(test_file)
    
    print(f"Fixed Unicode in {len(test_files)} test files")

if __name__ == "__main__":
    main()