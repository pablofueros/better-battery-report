<div align="center">

<img src="https://raw.githubusercontent.com/pablofueros/better-battery-report/main/assets/banner.png" alt="BBRPY logo" width="600"/>

---

### **✨ Better Battery Report: A Python CLI tool that generates enhanced battery reports for Windows systems ✨**

[![Code Quality](https://github.com/pablofueros/bbrpy/actions/workflows/code-quality.yaml/badge.svg)](https://github.com/pablofueros/bbrpy/actions/workflows/code-quality.yaml)
[![Release](https://github.com/pablofueros/bbrpy/actions/workflows/release.yaml/badge.svg)](https://github.com/pablofueros/bbrpy/actions/workflows/release.yaml)
[![codecov](https://codecov.io/gh/pablofueros/better-battery-report/graph/badge.svg?token=YGVE6SADVQ)](https://codecov.io/gh/pablofueros/better-battery-report)
[![PyPI Latest Release](https://img.shields.io/pypi/v/bbrpy.svg)](https://pypi.org/project/bbrpy/)
[![PyPI Downloads](https://static.pepy.tech/badge/bbrpy)](https://pypi.org/project/bbrpy/)
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

> [!IMPORTANT]
> This will only install the essential dependencies for running the tool, making it lightweight and portable. For extended use, it may be necessary to install extra dependency groups as well.

It can also be installed into a persistent environment and added to the PATH:

```bash
uv tool install bbrpy
```

Alternatively, you can install it globally using pip:

```bash
pip install bbrpy
```

## 💻 Usage

The tool provides two main commands:

### Display Battery Information

```bash
bbrpy info
```

This command shows basic battery information including:

- Report scan time
- Capacity Status (current / design)

### Generate Battery Report

```bash
bbrpy report [--output PATH]
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

- `powercfg` Windows command-line tool for battery data
- `pydantic_xml` for the default report serialization
- `plotly` for interactive visualizations
- `pandas` for data processing
- `typer` for CLI interface

## ©️ License

MIT License
