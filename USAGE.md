# RDP Scanner Usage

## Installation

1. Install required tools:
   ```bash
   # On Ubuntu/Debian
   sudo apt update
   sudo apt install masscan nmap metasploit-framework
   
   # On CentOS/RHEL/Fedora
   sudo yum install masscan nmap metasploit-framework
   
   # On macOS
   brew install masscan nmap
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/bman77777/rdp-scanner.git
   cd rdp-scanner
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Basic Usage

Run a scan of the entire internet for open RDP ports:
```bash
python3 rdp_scanner.py 0.0.0.0/0
```

Scan specific IP ranges:
```bash
python3 rdp_scanner.py 192.168.1.0/24 10.0.0.0/8
```

## Configuration

The tool uses `config.json` for configuration. Default settings are:
- Scan port 3389 (RDP)
- Use masscan rate of 10,000 packets per second
- Run specific Nmap vulnerability scripts
- Scan for specific CVEs with Metasploit

## Output

The tool will create a `results/` directory containing:
- `masscan_results.json` - Raw masscan output
- `nmap_results.txt` - Nmap scan results
- `nmap_results.gnmap` - Nmap grepable output
- `scan_report.txt` - Summary report

## Exclude File

The tool uses an exclude file (`exclude.txt`) to avoid scanning private IP ranges by default:
```
10.0.0.0/8
172.16.0.0/12
192.168.0.0/16
127.0.0.0/8
```

You can customize this file to exclude additional IP ranges.