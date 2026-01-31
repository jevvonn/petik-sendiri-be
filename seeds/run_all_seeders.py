"""
Run all seeders
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from seeds.user_seeder import seed_demo_user


def run_all_seeders():
    """Run all database seeders."""
    print("=" * 50)
    print("Running all seeders...")
    print("=" * 50)
    
    # Run user seeder
    print("\n[1/1] Running user seeder...")
    seed_demo_user()
    
    print("\n" + "=" * 50)
    print("All seeders completed!")
    print("=" * 50)


if __name__ == "__main__":
    run_all_seeders()
