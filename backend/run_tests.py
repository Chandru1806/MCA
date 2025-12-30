import sys
import pytest

if __name__ == '__main__':
    args = [
        'tests/',
        '-v',
        '--tb=short',
        '--color=yes'
    ]
    
    if len(sys.argv) > 1:
        args = sys.argv[1:]
    
    exit_code = pytest.main(args)
    sys.exit(exit_code)
