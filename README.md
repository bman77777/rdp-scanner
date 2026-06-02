# RDP Scanner

An internet-wide RDP port scanner and vulnerability assessment tool.

This tool performs:
1. Masscan to discover open RDP ports (3389)
2. Nmap vulnerability scanning for RDP vulnerabilities
3. Metasploit integration for advanced CVE scanning

## Features

- Internet-wide RDP port scanning
- Vulnerability detection using nmap scripts
- Advanced CVE scanning with Metasploit
- Configuration file support
- Results reporting

## Requirements

- masscan
- nmap
- metasploit-framework
- Python 3.x

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

3. Make the setup script executable and run it:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

## Usage

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

## Supported CVEs

The scanner includes vulnerability detection for:
- RDP vulnerabilities (rdp-vuln-ms12-020)
- Encryption enumeration (rdp-enum-encryption)
- NTLM information (rdp-ntlm-info)
- CVE-2019-0708 BlueKeep
- CVE-2019-1181/1182 DejaBlue
- CVE-2019-1384/MS-T120

## License

MIT License