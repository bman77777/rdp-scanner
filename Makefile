# Makefile for RDP Scanner

.PHONY: install setup run clean

install:
	@echo "Installing RDP Scanner..."
	@chmod +x setup.sh
	@./setup.sh

setup:
	@echo "Setting up RDP Scanner environment..."
	@chmod +x setup.sh
	@./setup.sh

run:
	@echo "Running RDP Scanner..."
	python3 rdp_scanner.py 0.0.0.0/0

clean:
	@echo "Cleaning up results..."
	rm -rf results/