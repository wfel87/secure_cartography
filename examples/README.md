# Secure Cartography Examples

This directory contains example scripts demonstrating various use cases for Secure Cartography.

## Export Examples

### `export_examples.py`

Demonstrates programmatic use of the GraphML exporter API:

1. **Basic Export** - Simple export with default settings
2. **Custom Export** - Export with custom settings (layout, fonts, filtering)
3. **Multiple Formats** - Generate multiple variants from the same topology
4. **Custom Icons** - Use custom icon directory
5. **Process Discovery Output** - Automatically export from discovery results
6. **Batch Processing** - Process multiple topology files

**Usage:**

```bash
# Make sure you have a map.json file in your current directory
python export_examples.py
```

Edit the script to uncomment the examples you want to run.

**API Example:**

```python
from sc2.export import GraphMLExporter
from pathlib import Path
import json

# Load topology
with open("map.json", 'r') as f:
    topology = json.load(f)

# Create exporter
exporter = GraphMLExporter(
    use_icons=True,
    include_endpoints=False,
    connected_only=True,
    layout_type='circle'
)

# Export
exporter.export(topology, Path("output.graphml"))
```

## Running Examples

All examples assume you have:
1. Installed Secure Cartography (`pip install -e .`)
2. A `map.json` file from a network discovery

To get a `map.json` file, run a discovery:

```bash
# Initialize vault and add credentials
python -m sc2.scng.creds init
python -m sc2.scng.creds add snmpv2c public --community public

# Run discovery
python -m sc2.scng.discovery crawl 192.168.1.1 -d 2 -o ./discovery_output

# The map.json will be in ./discovery_output/map.json
```
