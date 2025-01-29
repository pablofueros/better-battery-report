<div align="center">

<img src="https://raw.githubusercontent.com/pablofueros/better-battery-report/main/assets/banner.png" alt="BBRPY logo" width="600"/>

---

### **✨ Better Battery Report: A Python CLI tool that generates enhanced battery reports for Windows systems ✨**

[![Code Quality](https://github.com/pablofueros/bbrpy/actions/workflows/code-quality.yaml/badge.svg)](https://github.com/pablofueros/bbrpy/actions/workflows/code-quality.yaml)
[![Release](https://github.com/pablofueros/bbrpy/actions/workflows/release.yaml/badge.svg)](https://github.com/pablofueros/bbrpy/actions/workflows/release.yaml)
[![PyPI Latest Release](https://img.shields.io/pypi/v/bbrpy.svg)](https://pypi.org/project/bbrpy/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/bbrpy.svg?label=PyPI%20downloads)](https://pypi.org/project/bbrpy/)
![versions](https://img.shields.io/pypi/pyversions/bbrpy.svg)

---

</div>

## 📋 Features

- Display basic battery information
- Generate battery health reports with interactive visualizations
- Export reports as HTML files with Plotly graphs
- Track battery capacity changes over time

## 📦 Installation

Since this is a CLI application, it's recommended to run it using [uvx](https://docs.astral.sh/uv/guides/tools/):

```bash
uvx bbrpy
```

Alternatively, you can install it using pip:

```bash
pip install bbrpy
```

Or [pipx](https://github.com/pypa/pipx) to install it on an isolated environment:

```bash
pipx install bbrpy
```

## 💻 Usage

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

## 📘 Requirements

- Windows operating system
- Python 3.12 or higher
- Administrative privileges (for powercfg command)

## ⚙️ Technical Details

The tool uses:

- `powercfg` Windows command-line tool for battery data
- Plotly for interactive visualizations
- Pandas for data processing
- Typer for CLI interface

## ©️ License

MIT License
