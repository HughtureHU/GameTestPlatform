# scripts/ci_test.py
import platform

print("=================================================")
print("Hello from a Python script run by Jenkins CI!")
print(f"This script is running on a '{platform.system()}' system.")
print("=================================================")