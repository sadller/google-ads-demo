"""
Development Server
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src'))


def main():
    from app import create_app
    
    app = create_app()
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 8000))
    
    print(f"\n{'='*50}")
    print(f"Pathik AI API - http://localhost:{port}")
    print(f"Health: http://localhost:{port}/api/v1/health")
    print(f"{'='*50}\n")
    
    app.run(host=host, port=port)


if __name__ == '__main__':
    main()
