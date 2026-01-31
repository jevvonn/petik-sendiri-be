"""
Run all seeders
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from seeds.user_seeder import seed_demo_user
from seeds.plant_seeder import seed_plants
from seeds.vendor_seeder import seed_vendors


def run_all_seeders():
    """Run all database seeders."""
    print("=" * 70)
    print("Running all seeders...")
    print("=" * 70)
    
    # Run user seeder
    print("\n[1/3] Running user seeder...")
    seed_demo_user()
    
    # Run plant seeder
    print("\n[2/3] Running plant seeder...")
    seed_plants()
    
    # Run vendor seeder
    print("\n[3/3] Running vendor seeder...")
    seed_vendors()
    
    print("\n" + "=" * 70)
    print("✅ All seeders completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    run_all_seeders()
