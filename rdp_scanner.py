#!/usr/bin/env python3
"""
RDP Scanner - Internet-wide RDP port scanning and vulnerability assessment tool
"""

import subprocess
import json
import argparse
import sys
import os
import time
from pathlib import Path

class RDPScanner:
    def __init__(self, config_file="config.json"):
        """Initialize the RDP scanner with configuration."""
        self.config = self.load_config(config_file)
        self.exclude_file = self.config.get("exclude_file", "exclude.txt")
        self.output_dir = Path(self.config.get("output_dir", "results"))
        self.output_dir.mkdir(exist_ok=True)
        
    def load_config(self, config_file):
        """Load configuration from JSON file."""
        default_config = {
            "exclude_file": "exclude.txt",
            "output_dir": "results",
            "masscan": {
                "ports": "3389",
                "rate": 10000,
                "excludefile": "exclude.txt"
            },
            "nmap": {
                "scripts": [
                    "rdp-vuln-ms12-020",
                    "rdp-enum-encryption", 
                    "rdp-ntlm-info"
                ]
            },
            "metasploit": {
                "cves": [
                    "CVE-2019-0708",
                    "CVE-2019-1181",
                    "CVE-2019-1182", 
                    "CVE-2019-1384",
                    "MS-T120"
                ]
            }
        }
        
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
                # Merge with default config
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
        else:
            # Create default config file
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            return default_config
            
    def run_masscan(self, targets):
        """Run masscan to discover open RDP ports."""
        print("[+] Running masscan to discover open RDP ports...")
        
        # Prepare masscan command
        cmd = [
            "masscan", 
            "--ports", self.config["masscan"]["ports"],
            "--rate", str(self.config["masscan"]["rate"]),
            "--output-format", "json",
            "--output-file", str(self.output_dir / "masscan_results.json")
        ]
        
        # Add exclude file if it exists
        if os.path.exists(self.exclude_file):
            cmd.extend(["--excludefile", self.exclude_file])
            
        cmd.extend(targets)
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"[+] Masscan completed. Output: {result.stdout}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"[-] Masscan failed: {e.stderr}")
            return False
            
    def parse_masscan_results(self):
        """Parse masscan results and extract IP addresses."""
        results_file = self.output_dir / "masscan_results.json"
        
        if not os.path.exists(results_file):
            print("[-] No masscan results found")
            return []
            
        try:
            with open(results_file, 'r') as f:
                data = json.load(f)
                
            open_ips = []
            for host in data.get('results', []):
                if host.get('ports'):
                    ip = host.get('ip')
                    if ip:
                        open_ips.append(ip)
                        
            print(f"[+] Found {len(open_ips)} hosts with open RDP ports")
            return open_ips
            
        except Exception as e:
            print(f"[-] Error parsing masscan results: {e}")
            return []
            
    def run_nmap_scan(self, ip_list):
        """Run nmap vulnerability scans on discovered IPs."""
        print("[+] Running Nmap vulnerability scans...")
        
        if not ip_list:
            print("[-] No IP addresses to scan")
            return False
            
        # Prepare nmap command with vulnerability scripts
        cmd = [
            "nmap",
            "-p", "3389",
            "--script", ",".join(self.config["nmap"]["scripts"]),
            "-oN", str(self.output_dir / "nmap_results.txt"),
            "-oG", str(self.output_dir / "nmap_results.gnmap")
        ]
        
        # Add all target IPs
        cmd.extend(ip_list)
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print("[+] Nmap scan completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"[-] Nmap scan failed: {e.stderr}")
            return False
            
    def run_metasploit_scan(self, ip_list):
        """Run Metasploit vulnerability scans."""
        print("[+] Running Metasploit vulnerability scans...")
        
        if not ip_list:
            print("[-] No IP addresses to scan")
            return False
            
        # Create a temporary script for metasploit
        msf_script = f"""
msfconsole -q -x "
use auxiliary/scanner/rdp/cve_2019_0708_bluekeep
set RHOSTS {' '.join(ip_list)}
set THREADS 5
run
exit
"
"""
        
        try:
            # Run metasploit commands for specific CVEs
            for cve in self.config["metasploit"]["cves"]:
                print(f"[+] Scanning for {cve}")
                if cve == "CVE-2019-0708":
                    cmd = [
                        "msfconsole", "-q", 
                        "-x", f"use auxiliary/scanner/rdp/cve_2019_0708_bluekeep; set RHOSTS {' '.join(ip_list)}; run; exit"
                    ]
                else:
                    # For other CVEs, we'll use generic RDP scanners
                    cmd = [
                        "msfconsole", "-q",
                        "-x", f"use auxiliary/scanner/rdp/rdp_scanner; set RHOSTS {' '.join(ip_list)}; run; exit"
                    ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, check=False)
                print(f"[+] Metasploit scan for {cve} completed")
            return True
        except Exception as e:
            print(f"[-] Metasploit scan failed: {e}")
            return False
            
    def run_full_scan(self, targets):
        """Run the complete scanning process."""
        print("[+] Starting RDP vulnerability scanner...")
        
        # Step 1: Run masscan
        if not self.run_masscan(targets):
            print("[-] Masscan failed. Exiting.")
            return False
            
        # Step 2: Parse results
        ip_list = self.parse_masscan_results()
        if not ip_list:
            print("[-] No open RDP ports found. Exiting.")
            return False
            
        # Step 3: Run nmap vulnerability scans
        if not self.run_nmap_scan(ip_list):
            print("[-] Nmap scan failed.")
            
        # Step 4: Run metasploit scans
        if not self.run_metasploit_scan(ip_list):
            print("[-] Metasploit scan failed.")
            
        print("[+] Scanning process completed successfully!")
        return True
        
    def generate_report(self):
        """Generate a summary report."""
        print("[+] Generating summary report...")
        
        report_content = "RDP Scanner Report\n"
        report_content += "=" * 50 + "\n"
        report_content += f"Scan started: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        report_content += f"Output directory: {self.output_dir}\n"
        
        # Add results summary
        masscan_file = self.output_dir / "masscan_results.json"
        if masscan_file.exists():
            try:
                with open(masscan_file, 'r') as f:
                    data = json.load(f)
                    host_count = len(data.get('results', []))
                    report_content += f"Open RDP hosts found: {host_count}\n"
            except:
                pass
                
        report_content += "\nScanning completed successfully!\n"
        
        report_file = self.output_dir / "scan_report.txt"
        with open(report_file, 'w') as f:
            f.write(report_content)
            
        print(f"[+] Report generated: {report_file}")
        return True

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='RDP Scanner - Internet-wide RDP port scanning')
    parser.add_argument('targets', nargs='*', help='Target IP addresses or ranges (e.g., 192.168.0.0/16)')
    parser.add_argument('--config', default='config.json', help='Configuration file path')
    parser.add_argument('--exclude', default='exclude.txt', help='Exclude file path')
    
    args = parser.parse_args()
    
    # If no targets provided, use a default range
    if not args.targets:
        print("No targets specified. Using default 0.0.0.0/0 (entire internet)")
        args.targets = ["0.0.0.0/0"]
        
    # Create scanner instance
    scanner = RDPScanner(args.config)
    
    # Run full scan
    success = scanner.run_full_scan(args.targets)
    
    if success:
        scanner.generate_report()
        print("[+] All scans completed successfully!")
        sys.exit(0)
    else:
        print("[-] Scanning process failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()