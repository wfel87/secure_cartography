#!/usr/bin/env python3
"""
SecureCartography v2 - Export Module Entry Point

Allows running the export CLI as a module:
    python -m sc2.export graphml map.json output.graphml
"""

from .cli import main

if __name__ == '__main__':
    exit(main())
