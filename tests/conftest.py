import sys
from pathlib import Path

# Agrega la carpeta padre al path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))