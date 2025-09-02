# 📊 Depreciation & Discounted Cash Flow (DCF) Financial Analysis Tool

**A comprehensive Python toolkit for depreciation calculations, discounted cash flow forecasting, and financial metrics analysis with interactive CLI and visualization capabilities.**

## 🎯 Project Overview

This project provides a modular financial analysis toolkit that supports:

- **🧮 Depreciation Methods**: Sum of Years' Digits (SOYD) and Declining Double Balance (DDB) calculations
- **💰 DCF Analysis**: Complete discounted cash flow modeling with NPV, IRR, and payback period calculations  
- **📈 Financial Metrics**: ROI, DCFROR, cumulative cash flows, and risk assessments
- **📊 Interactive Visualizations**: Comprehensive plotting of cash flows, NPV sensitivity analysis, and financial projections
- **⚙️ Flexible Configuration**: Command-line interface with interactive prompts and parameter overrides

## 📁 Project Structure

```
📦 Financial Analysis Tool
├── 📄 main.py                    # Main CLI application entry point
├── 📄 README.md                  # Project documentation
├── 📄 directory_structure.txt    # Generated folder structure
├── 📁 config/
│   └── 📄 example_config.py      # Configuration templates and parameters
├── 📁 depreciation/
│   ├── 📄 ddb.py                 # Declining Double Balance method
│   └── 📄 soyd.py                # Sum of Years' Digits method
├── 📁 finance/
│   ├── 📄 engine.py              # Core DCF computation engine
│   └── 📄 metrics.py             # Financial metrics calculations
└── 📁 plotting/
    └── 📄 plots.py               # Data visualization and charting
```

## 🚀 Features

### **Depreciation Methods**
- **SOYD (Sum of Years' Digits)**: Accelerated depreciation with higher early-year deductions
- **DDB (Declining Double Balance)**: Double-declining balance depreciation method
- **Customizable Parameters**: Asset life, salvage value, and depreciation timing

### **Financial Analysis**
- **Net Present Value (NPV)**: Time-value adjusted project valuation
- **Internal Rate of Return (IRR)**: DCFROR calculations with sensitivity analysis
- **Payback Period**: Investment recovery time analysis
- **Cash Flow Projections**: Period-by-period financial forecasting
- **Tax Impact Analysis**: After-tax cash flow considerations

### **Visualization & Reporting**
- **Cash Flow Charts**: Visual representation of periodic cash flows
- **Cumulative Analysis**: Running totals and break-even visualization  
- **NPV Sensitivity**: Interest rate impact on project viability
- **Interactive Plots**: Matplotlib-based financial dashboards

## 🛠️ Installation & Setup

### Prerequisites
- **Python 3.9+** 
- **Required Libraries**: numpy, matplotlib, pandas (see requirements.txt)

### Installation Steps

```bash
# Clone the repository
git clone https://github.com/yourusername/financial-analysis-tool.git
cd financial-analysis-tool

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 💻 Usage

### **Basic Usage**
```bash
# Run with default settings
python main.py

# Specify depreciation method
python main.py --method SOYD

# Skip visualizations
python main.py --no_plots
```

### **Command Line Parameters**
```bash
python main.py \
  --method DDB \
  --FCI_L1 500000 \
  --FCI_L2 100000 \
  --intr 0.12 \
  --t 0.25 \
  --periods 10
```

### **Interactive Mode**
The application will prompt for financial parameters:
- Fixed Capital Investment (L1, L2)
- Working Capital and Land Costs
- Discount Rate and Tax Rate
- Revenue and Operating Cost projections
- Depreciation life and timing parameters

### **Sample Output**
```
Method: SOYD
NPV: 125,847.32
DCFROR (approx): 0.158200
Payback Period: 4.2 years
ROI: 0.245000
```

## 🧪 Example Configuration

```python
CONFIG = {
    "FCI_L1": 175.0,
    "FCI_L2": 125.0,
    "L": 10.0,
    "WC": 20.0,
    "S": 10.0,
    "intr": 0.08,   # discount rate
    "t": 0.25,      # tax rate
    # Scalar revenue and COM per period (periods 0..12); first 3 will be ignored for ops
    "R_scalar": 110.0,
    "COM_scalar": 30.0,
    # Depreciation horizon mapping: indices 3..9 carry annual depreciation; >=10 write-off remaining BV
    "life_years": 7,         # useful life for planned depreciation years
    "depr_start_idx": 3,     # first operating year index (0-based) for depreciation charges
    "periods": 13,
    # DCFROR scan range
    "irr_scan_min": 0.05,
    "irr_scan_max": 0.30,
    "irr_scan_points": 10000,
}
```

## 📊 Output Metrics

| Metric | Description |
|--------|-------------|
| **NPV** | Net Present Value of cash flows |
| **DCFROR** | Discounted Cash Flow Rate of Return |
| **PBP** | Payback Period (years) |
| **ROROI** | Return on Original Investment |
| **CCP** | Cumulative Cash Position |
| **CCR** | Cash Coverage Ratio |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/enhancement`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/enhancement`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👨‍💻 Author

**[Aadityaamlan Panda]**
- GitHub: [@Aadityaamlan-Panda](https://github.com/Aadityaamlan-Panda)
- Email: aadityaap22@tk.ac.in
- LinkedIn: [Aadityaamlan Panda](https://www.linkedin.com/in/aadityaamlan-panda-a07403a1/)

***

## 🎯 Project Tags

`financial-analysis` `depreciation` `dcf` `python` `fintech` `investment-analysis` `cash-flow` `financial-modeling` `matplotlib` `numpy`

***

*This project serves as a comprehensive demonstration of financial modeling, software architecture, and data visualization techniques for investment and accounting analysis.*


