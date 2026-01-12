#!/usr/bin/env python3
"""
Semantic Inspector - CLI tool to explore Secret Server's library modules

This tool provides a "semantic overlay" to understand the codebase by:
- Listing all modules and their purpose
- Showing function definitions with docstrings
- Explaining what each component does in plain language
"""

import sys
import inspect as pyinspect
import importlib
import os

# Add lib to path
sys.path.insert(0, os.path.dirname(__file__))

# Semantic descriptions of each module
MODULE_DESCRIPTIONS = {
    "auth": "Authentication - Manages user credentials and verification",
    "config": "Configuration - System-wide settings and paths",
    "crypto": "Secrecy - Handles GPG encryption and decryption",
    "fs_mapper": "Filesystem Mapper - Converts JSON to/from directory structures",
    "network": "Network - Socket communication utilities",
    "protocol": "Protocol - Message formatting for client-server communication",
    "storage": "Storage - Persists encrypted payloads to disk",
    "utils": "Utilities - Helper functions (autovivification, deep updates)"
}

def list_modules():
    """Show all available library modules with descriptions"""
    print("\n" + "="*60)
    print("SECRET SERVER - LIBRARY MODULES")
    print("="*60 + "\n")
    
    for module_name, description in MODULE_DESCRIPTIONS.items():
        print(f"📦 lib.{module_name:<15} - {description}")
    
    print("\n" + "-"*60)
    print("Usage: ./semantic.py <module_name>")
    print("Example: ./semantic.py crypto")
    print("-"*60 + "\n")

def inspect_module(module_name):
    """Show detailed information about a specific module"""
    try:
        # Import the module
        mod = importlib.import_module(f"lib.{module_name}")
        
        print("\n" + "="*60)
        print(f"MODULE: lib.{module_name}")
        print("="*60)
        
        # Show description
        if module_name in MODULE_DESCRIPTIONS:
            print(f"\n📋 Purpose: {MODULE_DESCRIPTIONS[module_name]}")
        
        # Show module docstring if available
        if mod.__doc__:
            print(f"\n📖 Documentation:\n{mod.__doc__.strip()}")
        
        print("\n" + "-"*60)
        print("FUNCTIONS & CLASSES")
        print("-"*60 + "\n")
        
        # Get all functions and classes
        members = pyinspect.getmembers(mod)
        
        for name, obj in members:
            # Skip private/imported items
            if name.startswith('_') or pyinspect.ismodule(obj):
                continue
            
            if pyinspect.isfunction(obj):
                # Get signature
                try:
                    sig = pyinspect.signature(obj)
                    print(f"🔧 {name}{sig}")
                except:
                    print(f"🔧 {name}(...)")
                
                # Get docstring
                if obj.__doc__:
                    doc_lines = obj.__doc__.strip().split('\n')
                    for line in doc_lines[:3]:  # First 3 lines
                        print(f"   {line.strip()}")
                print()
            
            elif pyinspect.isclass(obj):
                print(f"📦 class {name}")
                if obj.__doc__:
                    print(f"   {obj.__doc__.strip().split(chr(10))[0]}")
                print()
        
        # Show constants/variables
        constants = [(name, obj) for name, obj in members 
                    if not name.startswith('_') 
                    and not pyinspect.isfunction(obj) 
                    and not pyinspect.isclass(obj)
                    and not pyinspect.ismodule(obj)]
        
        if constants:
            print("-"*60)
            print("CONSTANTS & VARIABLES")
            print("-"*60 + "\n")
            for name, value in constants:
                print(f"📌 {name} = {repr(value)}")
        
        print("\n" + "="*60 + "\n")
        
    except ModuleNotFoundError:
        print(f"\n❌ Error: Module 'lib.{module_name}' not found.")
        print(f"   Available modules: {', '.join(MODULE_DESCRIPTIONS.keys())}\n")
    except Exception as e:
        print(f"\n❌ Error inspecting module: {e}\n")

def show_semantic_map():
    """Show the semantic architecture - how modules relate to each other"""
    print("\n" + "="*60)
    print("SECRET SERVER - SEMANTIC ARCHITECTURE")
    print("="*60 + "\n")
    
    print("The 4-Block Security Model:\n")
    
    print("1️⃣  VIVIFY (Input Layer)")
    print("    └─ web_server.py - Web interface for user input")
    print("    └─ lib.utils - Autovivification helpers\n")
    
    print("2️⃣  SECRECY (Encryption Layer)")
    print("    └─ lib.crypto - GPG encryption/decryption")
    print("    └─ lib.config - Encryption settings\n")
    
    print("3️⃣  PAYLOAD (Packaging Layer)")
    print("    └─ lib.protocol - Message formatting")
    print("    └─ lib.network - Communication utilities\n")
    
    print("4️⃣  SERVER (Storage Layer)")
    print("    └─ lib.storage - Payload persistence")
    print("    └─ lib.fs_mapper - Filesystem hierarchy")
    print("    └─ lib.auth - User authentication\n")
    
    print("="*60 + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        list_modules()
        print("\nOther commands:")
        print("  ./semantic.py --map    - Show semantic architecture")
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "--map":
        show_semantic_map()
    elif command in MODULE_DESCRIPTIONS:
        inspect_module(command)
    else:
        print(f"\n❌ Unknown module or command: {command}")
        list_modules()
