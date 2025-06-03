import os
import subprocess
import requests
from utils.logger import get_logger
from utils.helpers import save_to_output

logger = get_logger("EVIL_JWT_FORCE.osint")

class OSINTScanner:
    def __init__(self, target_url=None):
        self.target_url = target_url
        self.theharvester_available = self.check_theharvester()

    def check_theharvester(self):
        """Check if theHarvester is installed and available in the system PATH."""
        try:
            result = subprocess.run(['theHarvester', '-h'], capture_output=True, text=True)
            if result.returncode == 0:
                logger.info("theHarvester detected on system. Enhanced OSINT capabilities enabled.")
                return True
        except FileNotFoundError:
            logger.warning("theHarvester not found. Falling back to built-in OSINT methods.")
        return False

    def run(self):
        if not self.target_url:
            self.target_url = input("Enter the target URL or domain for OSINT scanning: ")
        
        logger.info(f"Starting OSINT scan on {self.target_url}")
        
        if self.theharvester_available:
            logger.info("Using theHarvester for advanced OSINT scanning.")
            self.run_theharvester()
        else:
            logger.info("Using built-in OSINT scanning method.")
            self.run_builtin_osint()

    def run_theharvester(self):
        """Run theHarvester with basic parameters for OSINT scanning."""
        try:
            domain = self.target_url.split('://')[-1].split('/')[0]
            cmd = [
                'theHarvester',
                '-d', domain,
                '-l', '500',
                '-s', '0',
                '-b', 'all'
            ]
            logger.info(f"Executing theHarvester command: {' '.join(cmd)}")
            process = subprocess.run(cmd, capture_output=True, text=True)
            output = process.stdout + process.stderr
            logger.info("theHarvester execution completed.")
            save_to_output("osint_theharvester", output)
            print("OSINT scan with theHarvester completed. Results saved to output/osint_theharvester.txt")
        except Exception as e:
            logger.error(f"Error running theHarvester: {e}")
            print(f"Error running theHarvester: {e}")

    def run_builtin_osint(self):
        """Run built-in OSINT scanning using simple web requests."""
        try:
            domain = self.target_url.split('://')[-1].split('/')[0]
            logger.info(f"Performing basic OSINT on {domain}")
            # Placeholder for basic OSINT logic
            response = requests.get(f"http://ip-api.com/json/{domain}", timeout=5)
            data = response.json()
            results = f"OSINT Results for {domain}:\n"
            results += f"IP: {data.get('query', 'N/A')}\n"
            results += f"Location: {data.get('city', 'N/A')}, {data.get('country', 'N/A')}\n"
            results += f"ISP: {data.get('isp', 'N/A')}\n"
            logger.info(results)
            save_to_output("osint_builtin", results)
            print("Built-in OSINT scan completed. Results saved to output/osint_builtin.txt")
        except Exception as e:
            logger.error(f"Error during built-in OSINT scan: {e}")
            print(f"Error during built-in OSINT scan: {e}")

if __name__ == "__main__":
    scanner = OSINTScanner()
    scanner.run() 