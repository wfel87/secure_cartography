#!/usr/bin/env python3
"""
Example: Programmatic Use of GraphML Exporter

This example demonstrates how to use the GraphMLExporter class
directly from Python code for custom workflows and automation.
"""

import json
import sys
from pathlib import Path

# Add parent directory to path for running from examples folder
sys.path.insert(0, str(Path(__file__).parent.parent))

from sc2.export import GraphMLExporter


def example_basic_export():
    """Basic export with default settings."""
    print("Example 1: Basic GraphML Export")
    print("-" * 50)
    
    # Load topology from JSON file
    topology_path = Path("map.json")
    with open(topology_path, 'r') as f:
        topology = json.load(f)
    
    # Create exporter with default settings
    exporter = GraphMLExporter()
    
    # Export to GraphML
    output_path = Path("network_topology.graphml")
    exporter.export(topology, output_path)
    
    print(f"✓ Exported {len(topology)} nodes to {output_path}")
    print()


def example_custom_export():
    """Export with custom settings."""
    print("Example 2: Custom Export Settings")
    print("-" * 50)
    
    # Load topology
    with open("map.json", 'r') as f:
        topology = json.load(f)
    
    # Create exporter with custom settings
    exporter = GraphMLExporter(
        use_icons=True,              # Enable device icons
        include_endpoints=False,      # Exclude phones, cameras, etc.
        connected_only=True,          # Only show connected devices
        layout_type='circle',         # Use circular layout
        font_size=14,                 # Larger font
        font_family='Arial'           # Custom font
    )
    
    # Export
    output_path = Path("network_custom.graphml")
    exporter.export(topology, output_path)
    
    print(f"✓ Exported with custom settings to {output_path}")
    print(f"  - Layout: circle")
    print(f"  - Icons: enabled")
    print(f"  - Endpoints: excluded")
    print(f"  - Connected only: yes")
    print()


def example_multiple_formats():
    """Export the same topology in multiple formats."""
    print("Example 3: Export Multiple Variants")
    print("-" * 50)
    
    # Load topology
    with open("map.json", 'r') as f:
        topology = json.load(f)
    
    # Export with icons
    exporter_icons = GraphMLExporter(use_icons=True, layout_type='grid')
    exporter_icons.export(topology, Path("topology_with_icons.graphml"))
    print("✓ Exported with icons (grid layout)")
    
    # Export without icons (shapes only)
    exporter_shapes = GraphMLExporter(use_icons=False, layout_type='circle')
    exporter_shapes.export(topology, Path("topology_shapes.graphml"))
    print("✓ Exported with shapes (circle layout)")
    
    # Export core devices only (no endpoints)
    exporter_core = GraphMLExporter(
        use_icons=True, 
        include_endpoints=False,
        connected_only=True
    )
    exporter_core.export(topology, Path("topology_core.graphml"))
    print("✓ Exported core network only")
    print()


def example_custom_icons():
    """Use custom icon directory."""
    print("Example 4: Custom Icon Directory")
    print("-" * 50)
    
    # Load topology
    with open("map.json", 'r') as f:
        topology = json.load(f)
    
    # Use custom icons directory
    custom_icons_dir = Path("/path/to/custom/icons")
    
    exporter = GraphMLExporter(
        use_icons=True,
        icons_dir=custom_icons_dir  # Point to custom icon files
    )
    
    output_path = Path("topology_custom_icons.graphml")
    exporter.export(topology, output_path)
    
    print(f"✓ Exported with custom icons from {custom_icons_dir}")
    print()


def example_process_discovery_output():
    """Process discovery output directory."""
    print("Example 5: Process Discovery Output")
    print("-" * 50)
    
    # Path to discovery output directory
    discovery_dir = Path("./discovery_output_20260114")
    
    # Find map.json in discovery output
    map_file = discovery_dir / "map.json"
    
    if not map_file.exists():
        print(f"ERROR: {map_file} not found")
        return
    
    # Load topology
    with open(map_file, 'r') as f:
        topology = json.load(f)
    
    # Export to same directory
    output_file = discovery_dir / "topology.graphml"
    
    exporter = GraphMLExporter(
        use_icons=True,
        include_endpoints=False,
        layout_type='grid'
    )
    
    exporter.export(topology, output_file)
    
    print(f"✓ Processed discovery output:")
    print(f"  Input:  {map_file}")
    print(f"  Output: {output_file}")
    print(f"  Nodes:  {len(topology)}")
    print()


def example_batch_processing():
    """Batch process multiple topology files."""
    print("Example 6: Batch Processing")
    print("-" * 50)
    
    # Find all map.json files in subdirectories
    topology_files = list(Path(".").glob("**/map.json"))
    
    print(f"Found {len(topology_files)} topology files")
    
    exporter = GraphMLExporter(use_icons=True, layout_type='grid')
    
    for topology_file in topology_files:
        # Load topology
        with open(topology_file, 'r') as f:
            topology = json.load(f)
        
        # Generate output filename
        output_file = topology_file.parent / "topology.graphml"
        
        # Export
        exporter.export(topology, output_file)
        
        print(f"✓ {topology_file.parent.name}: {len(topology)} nodes → {output_file.name}")
    
    print()


if __name__ == '__main__':
    print("=" * 50)
    print("GraphML Exporter API Examples")
    print("=" * 50)
    print()
    
    # Note: These examples assume map.json exists
    # Uncomment the examples you want to run:
    
    # example_basic_export()
    # example_custom_export()
    # example_multiple_formats()
    # example_custom_icons()
    # example_process_discovery_output()
    # example_batch_processing()
    
    print("See the source code for usage examples.")
    print("Uncomment the example you want to run.")
