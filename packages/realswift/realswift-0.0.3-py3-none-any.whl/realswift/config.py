#url = "https://www.google.com/gmail/about/"
import os
import json

class MyPackageConfig:
    def __init__(self):
        url = "https://lab5756.lab.pega.com/prweb"
        chrome_browser_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
        edge_browser_path = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
        offsetx = 0
        offsety = 0
        mousespeed = 0.2
        screenshot_path = 'target/screenshot.png'
        timeout = 60
        browser = 'chrome'
        output_path = 'target/output.jpg'
    def load_from_file(self, file_path):
        # Load configuration from a file (e.g., JSON)
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                config_data = json.load(file)
                self.url = config_data.get('url', self.url)
                self.chrome_browser_path = config_data.get('property2', self.chrome_browser_path)
                self.offsetx = config_data.get('offsetx', self.url)
                self.offsety = config_data.get('offsety', self.offsety)
                self.edge_browser_path = config_data.get('edge_browser_path', self.edge_browser_path)
                self.mousespeed = config_data.get('mousespeed', self.mousespeed)
                self.screenshot_path = config_data.get('screenshot_path', self.screenshot_path)
                self.timeout = config_data.get('property2', self.timeout)
                self.browser = config_data.get('property2', self.browser)
                self.output_path = config_data.get('output_path', self.output_path)

# Usage example
