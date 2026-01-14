#!/usr/bin/env python3
"""
SecureCartography v2 - Export CLI

Command-line interface for exporting network topology to various formats.

Usage:
    # Export map.json to GraphML
    python -m sc2.export graphml map.json output.graphml
    
    # Export with custom options
    python -m sc2.export graphml map.json network.graphml --no-icons --layout circle
    
    # Export excluding endpoints
    python -m sc2.export graphml map.json topology.graphml --no-endpoints
"""

import argparse
import json
import sys
from pathlib import Path

from .graphml_exporter import GraphMLExporter


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        prog='sc2.export',
        description='SecureCartography Network Topology Export Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Export to GraphML with icons
  python -m sc2.export graphml map.json network.graphml
  
  # Export without icons (shapes only)
  python -m sc2.export graphml map.json network.graphml --no-icons
  
  # Export with circular layout
  python -m sc2.export graphml map.json network.graphml --layout circle
  
  # Export excluding endpoint devices
  python -m sc2.export graphml map.json network.graphml --no-endpoints
  
  # Export with custom icons directory
  python -m sc2.export graphml map.json network.graphml --icons-dir /path/to/icons
  
  # Export connected devices only (exclude standalone nodes)
  python -m sc2.export graphml map.json network.graphml --connected-only
        """
    )
    
    subparsers = parser.add_subparsers(dest='format', help='Export format')
    
    # GraphML export command
    graphml_parser = subparsers.add_parser(
        'graphml',
        help='Export to yEd GraphML format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Export network topology to yEd-compatible GraphML format with icons'
    )
    
    graphml_parser.add_argument(
        'input',
        type=Path,
        help='Input topology JSON file (map.json)'
    )
    
    graphml_parser.add_argument(
        'output',
        type=Path,
        help='Output GraphML file path'
    )
    
    graphml_parser.add_argument(
        '--no-icons',
        action='store_true',
        help='Use shapes instead of embedded icons'
    )
    
    graphml_parser.add_argument(
        '--no-endpoints',
        action='store_true',
        help='Exclude endpoint devices (phones, cameras, etc.)'
    )
    
    graphml_parser.add_argument(
        '--connected-only',
        action='store_true',
        help='Only include devices that have at least one connection'
    )
    
    graphml_parser.add_argument(
        '--icons-dir',
        type=Path,
        help='Custom directory containing icon files'
    )
    
    graphml_parser.add_argument(
        '--layout',
        choices=['grid', 'circle', 'list'],
        default='grid',
        help='Initial layout algorithm (default: grid)'
    )
    
    graphml_parser.add_argument(
        '--font-size',
        type=int,
        default=12,
        help='Font size for labels (default: 12)'
    )
    
    graphml_parser.add_argument(
        '--font-family',
        default='Dialog',
        help='Font family for labels (default: Dialog)'
    )
    
    return parser


def cmd_graphml(args) -> int:
    """Execute GraphML export command."""
    # Validate input file
    if not args.input.exists():
        print(f"ERROR: Input file not found: {args.input}", file=sys.stderr)
        return 1
    
    # Load topology JSON
    try:
        with open(args.input, 'r') as f:
            topology = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {args.input}: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"ERROR: Failed to read {args.input}: {e}", file=sys.stderr)
        return 1
    
    # Validate topology structure
    if not isinstance(topology, dict):
        print(f"ERROR: Invalid topology format (expected dict, got {type(topology).__name__})", 
              file=sys.stderr)
        return 1
    
    # Create exporter
    try:
        exporter = GraphMLExporter(
            use_icons=not args.no_icons,
            icons_dir=args.icons_dir if args.icons_dir else None,
            include_endpoints=not args.no_endpoints,
            connected_only=args.connected_only,
            layout_type=args.layout,
            font_size=args.font_size,
            font_family=args.font_family
        )
    except Exception as e:
        print(f"ERROR: Failed to initialize exporter: {e}", file=sys.stderr)
        return 1
    
    # Export topology
    try:
        exporter.export(topology, args.output)
    except Exception as e:
        print(f"ERROR: Export failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1
    
    # Success - print summary
    print(f"✓ Exported to {args.output}")
    print(f"  Nodes: {len(topology)}")
    print(f"  Icons: {'enabled' if not args.no_icons else 'disabled'}")
    print(f"  Layout: {args.layout}")
    print(f"  Endpoints: {'included' if not args.no_endpoints else 'excluded'}")
    if args.connected_only:
        print(f"  Filter: connected devices only")
    
    return 0


def main(argv=None):
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args(argv)
    
    if not args.format:
        parser.print_help()
        return 1
    
    if args.format == 'graphml':
        return cmd_graphml(args)
    else:
        print(f"ERROR: Unknown format: {args.format}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
