import subprocess
import os

def run_tests():
    print("🚀 Running Playwright tests...\n")
    subprocess.run(["pytest", "-s"], check=False)

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))  # ensure we run from current folder
    run_tests()
