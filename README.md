# Better Battery Report

A Python CLI tool that generates enhanced battery reports for Windows systems using the powercfg command with data visualization capabilities.

## Features

- Generate battery health reports with interactive visualizations
- Display basic battery information
- Export reports as HTML files with Plotly graphs
- Track battery capacity changes over time

## Installation

```bash
pip install bbrpy
```

> **_NOTE:_** It is highly recommended to use this tool with uvx: <https://docs.astral.sh/uv/guides/tools/>

## Usage

The tool provides two main commands:

### Display Battery Information

```bash
bbrpy info
```

This command shows basic battery information including:

- Computer name
- Last scan time
- Design capacity
- Current full charge capacity

### Generate Battery Report

```bash
bbrpy generate [--output PATH]
```

Options:

- `--output`: Specify the output path for the HTML report (default: "./reports/battery_report.html")

This command:

1. Generates a battery report using powercfg
2. Creates an interactive visualization of battery capacity history
3. Opens the report in your default web browser

## Requirements

- Windows operating system
- Python 3.7 or higher
- Administrative privileges (for powercfg command)

## Technical Details

The tool uses:

- `powercfg` Windows command-line tool for battery data
- Plotly for interactive visualizations
- Polars for data processing
- Typer for CLI interface

## License

MIT License
