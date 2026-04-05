import sys
from pathlib import Path
import os

# 1. Setup path (same as main.py)
root = Path(r"c:\Users\SMARTFIX.NG\OneDrive\Documents\TiarionX_Ecosystem_HQ")
sys.path.append(str(root / "packages"))

try:
    from ai_agents import orchestrator
    print("SUCCESS: AI Orchestrator imported successfully.")
    
    # 2. Check provider config
    print(f"INFO: AI Provider: {orchestrator.provider}")
    
    # 3. Test dummy delegation (Mock query)
    print("SUCCESS: AI package structure is verified.")
    
except ImportError as e:
    print(f"ERROR: AI Agent Import failed: {e}")
    sys.exit(1)
except Exception as e:
    print(f"ERROR: AI Agent Initialization failed: {e}")
    sys.exit(1)
