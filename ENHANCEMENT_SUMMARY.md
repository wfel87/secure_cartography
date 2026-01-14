# Enhancement Summary: Python CLI and JSON Export Features

## Overview

This enhancement adds comprehensive Python CLI tools and JSON export capabilities to Secure Cartography, making it easier to export network topology data to standardized formats for visualization and documentation.

## What Was Added

### 1. Python CLI Export Tool

**Command:** `sc2-export` or `python -m sc2.export`

A new command-line tool for exporting topology data from JSON format to GraphML:

```bash
# Basic export
sc2-export graphml map.json network.graphml

# With options
sc2-export graphml map.json network.graphml --no-icons --layout circle
```

**Features:**
- Export to yEd-compatible GraphML format
- Embedded device icons (Cisco, Arista, Juniper, etc.)
- Multiple layout algorithms (grid, circle, list)
- Filtering options (exclude endpoints, connected-only)
- Customizable fonts and styling

### 2. Python API

**Module:** `sc2.export`

Programmatic access to export functionality:

```python
from sc2.export import GraphMLExporter
import json

# Load topology
with open('map.json', 'r') as f:
    topology = json.load(f)

# Export
exporter = GraphMLExporter(use_icons=True, layout_type='circle')
exporter.export(topology, Path('network.graphml'))
```

**Use Cases:**
- Automated export workflows
- Custom processing pipelines
- Batch processing of multiple discoveries
- Integration with other tools

### 3. Enhanced Documentation

**Updated:** `README.md`

- New "Exporting Topology" section with examples
- Updated CLI reference with export commands
- New "Export & Integration" feature category
- Updated development status
- Quick start examples

**New:** `examples/` directory

- Comprehensive API usage examples
- Six different usage patterns demonstrated
- README with setup instructions

### 4. File Changes

**New Files:**
- `sc2/export/__init__.py` - Module initialization with exports
- `sc2/export/__main__.py` - Module entry point
- `sc2/export/cli.py` - Command-line interface (5.7KB)
- `examples/export_examples.py` - API examples (5.9KB)
- `examples/README.md` - Examples documentation (1.7KB)

**Modified Files:**
- `setup.py` - Added `sc2-export` console script
- `README.md` - Added export documentation (~118 lines)
- `sc2/export/graphml_exporter.py` - Improved exception handling

## Technical Details

### Architecture

```
sc2/export/
├── __init__.py          # Exposes GraphMLExporter
├── __main__.py          # Module entry point
├── cli.py               # CLI implementation
└── graphml_exporter.py  # Core export logic (existing)
```

### CLI Options

| Option | Description |
|--------|-------------|
| `--no-icons` | Use shapes instead of icons |
| `--no-endpoints` | Exclude endpoint devices |
| `--connected-only` | Only include connected devices |
| `--layout {grid,circle,list}` | Layout algorithm |
| `--icons-dir PATH` | Custom icon directory |
| `--font-size SIZE` | Label font size |
| `--font-family FAMILY` | Label font family |

### Supported Export Formats

- **GraphML** - yEd-compatible format with embedded icons
- Platform-specific icons for Cisco, Arista, Juniper, Palo Alto, Fortinet
- Generic icons for routers, switches, firewalls, wireless APs

### Integration with Existing Features

- Works seamlessly with `map.json` from discovery module
- Compatible with `discovery_to_map.py` conversion tool
- No PyQt6 dependency for CLI export (can run headless)
- Reuses existing icon library from UI module

## Benefits

1. **Easy Visualization** - Export discoveries to yEd for interactive visualization
2. **Documentation** - Generate network diagrams for documentation
3. **Automation** - CLI tools for scripted workflows
4. **Flexibility** - Python API for custom integrations
5. **No GUI Required** - Export works in headless environments

## Usage Examples

### Quick Export
```bash
python -m sc2.scng.discovery crawl 192.168.1.1 -d 3 -o ./output
python -m sc2.export graphml ./output/map.json network.graphml
```

### Filtered Export
```bash
sc2-export graphml map.json topology.graphml \
    --no-endpoints \
    --connected-only \
    --layout circle
```

### Programmatic Export
```python
from sc2.export import GraphMLExporter

exporter = GraphMLExporter(
    include_endpoints=False,
    connected_only=True,
    layout_type='circle'
)
exporter.export(topology, output_path)
```

## Testing

All functionality has been tested:
- ✅ CLI help and argument parsing
- ✅ GraphML export with sample topology
- ✅ Various layout options (grid, circle, list)
- ✅ Filtering options (endpoints, connected-only)
- ✅ Error handling for invalid inputs
- ✅ Code review feedback addressed
- ✅ Security scan (0 vulnerabilities)

## Future Enhancements

Potential future additions:
- Additional export formats (PNG, SVG, Visio, Draw.io)
- GUI integration for direct export from UI
- Custom styling options
- Layout optimization algorithms
- Topology comparison/diff exports

## Security Summary

**CodeQL Analysis:** No vulnerabilities detected

The export functionality:
- Does not handle credentials or sensitive data
- Validates input files before processing
- Uses safe XML generation (no string concatenation)
- Properly handles exceptions
- No external network calls

## Conclusion

This enhancement successfully adds comprehensive Python CLI and JSON export capabilities to Secure Cartography, making it easier to integrate discovered topologies into documentation and visualization workflows. The implementation is clean, well-documented, and follows the project's existing patterns.
