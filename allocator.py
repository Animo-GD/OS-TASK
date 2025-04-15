import sys
from memory_allocator import run_allocator

def main():
    if len(sys.argv) != 2:
        print("Usage: python allocator.py <total_memory>")
        sys.exit(1)
    
    try:
        total_memory = int(sys.argv[1])
        if total_memory <= 0:
            print("Error: Total memory must be positive")
            sys.exit(1)
    except ValueError:
        print("Error: Total memory must be an integer")
        sys.exit(1)
    
    run_allocator(total_memory)

if __name__ == "__main__":
    main()