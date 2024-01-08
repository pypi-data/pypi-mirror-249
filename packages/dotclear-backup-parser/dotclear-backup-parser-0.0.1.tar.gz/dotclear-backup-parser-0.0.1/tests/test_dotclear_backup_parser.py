import sys
import unittest
from pathlib import Path

TEST_DIR = Path(__file__).parent
ROOT_DIR = TEST_DIR.parent
PYTHON_DIR = ROOT_DIR / "src"

path = TEST_DIR / "ressources" / "2024-01-07-11-22-dotclear-backup.txt"

sys.path.append(str(PYTHON_DIR))

from dotclear_backup_parser import load


class TestDcBackupParser(unittest.TestCase):
    """Main Dotclear backup parser test class."""
    def test_load(self):
        """Test parser load function."""
        with path.open() as f:
            parser = load(f)

        for table in parser:
            for i, col_name in enumerate(table.column_names):
                print(f"  {col_name}")
