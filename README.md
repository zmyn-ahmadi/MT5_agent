<div align="center">

# 📈 MT5 Historical Data Agent

**Pull your MetaTrader 5 trading history straight into clean, analysis-ready CSV files.**

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MetaTrader 5](https://img.shields.io/badge/MetaTrader-5-1E88E5?style=for-the-badge)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![License](https://img.shields.io/badge/License-TBD-lightgrey?style=for-the-badge)

[Features](#-features) •
[How it works](#-how-it-works) •
[Quick start](#-quick-start) •
[Output](#-output) •
[Project structure](#-project-structure)

</div>

---

## ✨ Overview

An automated Python agent that connects to your **MetaTrader 5** terminal, retrieves your historical deals and orders, **reconstructs full positions** from the raw deal records, and exports everything to CSV, ready for Excel, pandas, or your journaling and backtesting tools.

## 🚀 Features

|     | Feature                     | Description                                                                 |
| --- | --------------------------- | --------------------------------------------------------------------------- |
| 🔌  | **MT5 connection**          | Connects to a running MetaTrader 5 terminal through the official Python API |
| 🧾  | **Deals and orders**        | Retrieves your complete historical deals and orders                         |
| 🧩  | **Position reconstruction** | Rebuilds historical positions from individual deal records                  |
| 📅  | **Date-range filtering**    | Export only the period you care about                                       |
| 💾  | **CSV export**              | Clean, tidy files powered by Pandas                                         |

## 🔄 How it works

```mermaid
flowchart LR
    A[🔌 Connect to MT5] --> B[📥 Retrieve deals & orders]
    B --> C[🧩 Reconstruct positions]
    C --> D[💾 Export to CSV]
```

1. **Connect** to the MT5 terminal.
2. **Retrieve** historical trading data for your chosen date range.
3. **Process** the deals and reconstruct position history.
4. **Export** the results to CSV files.

## 🛠 Tech stack

- 🐍 **Python**
- 📊 **MetaTrader 5 Python API**
- 🐼 **Pandas**

## ⚡ Quick start

### Prerequisites

- The **MetaTrader 5 terminal** is installed, **running**, and **logged in** to your trading account.
- Python is installed.

> [!NOTE]
> The official `MetaTrader5` Python package works with the desktop terminal, which is Windows-only.

### Installation

```bash
git clone <repository-url>
cd mt5-agent

pip install -r requirements.txt
```

### Configuration

Set the following in the agent settings:

| Setting                 | Purpose                                  |
| ----------------------- | ---------------------------------------- |
| 🖥 **Terminal path**    | Location of your MT5 terminal            |
| 📅 **Date range**       | Start and end of the history to retrieve |
| 📁 **Output directory** | Where the CSV files are written          |

### Run

```bash
python main.py
```

## 📦 Output

The agent writes two files to the `data/` directory:

| File               | Description                        |
| ------------------ | ---------------------------------- |
| 📄 `deals.csv`     | Historical executed trading deals  |
| 📄 `positions.csv` | Reconstructed historical positions |

## 🗂 Project structure

```text
mt5-agent/
├── src/
│   ├── agent.py              # Orchestrates the full workflow
│   ├── mt5_connector.py      # Handles the MT5 terminal connection
│   ├── history_retriever.py  # Fetches deals, orders and positions
│   └── csv_exporter.py       # Writes results to CSV
├── data/
│   ├── deals.csv
│   └── positions.csv
├── main.py                   # Entry point
├── requirements.txt
└── README.md
```

## 📄 License

[Specify License]

<div align="center">

<sub>Built for traders who want their data, not a screenshot of it.</sub>

</div>
