class MemoryAllocator:
    def __init__(self, total_memory):
        self.total_memory = total_memory
        self.memory_blocks = [{'start': 0, 'end': total_memory - 1, 'process': None, 'allocated': False}]
        self.processes = {}
    
    def request_memory(self, process_name, size, strategy):
        if process_name in self.processes:
            print(f"Error: Process {process_name} already exists")
            return False
        
        holes = [] # index, start, size of free blocks
        for i, block in enumerate(self.memory_blocks):
            if not block['allocated'] and (block['end'] - block['start'] + 1) >= size:
                holes.append((i, block['start'], block['end'] - block['start'] + 1))
        
        if not holes:
            print(f"Error: Not enough memory to allocate {size} bytes")
            return False
        
        if strategy == 'F':
            selected = holes[0]
        elif strategy == 'B':
            selected = min(holes, key=lambda x: x[2])
        elif strategy == 'W':
            selected = max(holes, key=lambda x: x[2])
        else:
            print(f"Error: Invalid strategy '{strategy}'. Use F, B, or W")
            return False
        
        block_index, hole_start, hole_size = selected
        hole_end = hole_start + hole_size - 1
        
        allocated_block = {
            'start': hole_start,
            'end': hole_start + size - 1,
            'process': process_name,
            'allocated': True
        }
        
        remaining_block = {
            'start': hole_start + size,
            'end': hole_end,
            'process': None,
            'allocated': False
        }
        
        self.memory_blocks.pop(block_index)
        if remaining_block['start'] <= remaining_block['end']:
            self.memory_blocks.insert(block_index, remaining_block)
        self.memory_blocks.insert(block_index, allocated_block)
        
        self.processes[process_name] = allocated_block
        
        print(f"Allocated {size} bytes to process {process_name}")
        return True
    
    def release_memory(self, process_name):
        if process_name not in self.processes:
            print(f"Error: Process {process_name} not found")
            return False
        
        for i, block in enumerate(self.memory_blocks):
            if block['process'] == process_name:
                block['process'] = None
                block['allocated'] = False
                self._merge_adjacent_holes()
                del self.processes[process_name]
                print(f"Released memory allocated to process {process_name}")
                return True
        
        print(f"Error: Could not find memory block for process {process_name}")
        return False
    
    def _merge_adjacent_holes(self):
        i = 0
        while i < len(self.memory_blocks) - 1:
            current = self.memory_blocks[i]
            next_block = self.memory_blocks[i + 1]
            
            if not current['allocated'] and not next_block['allocated']:
                merged_block = {
                    'start': current['start'],
                    'end': next_block['end'],
                    'process': None,
                    'allocated': False
                }
                self.memory_blocks[i:i+2] = [merged_block]
            else:
                i += 1
    
    def compact_memory(self):
        allocated_blocks = [b for b in self.memory_blocks if b['allocated']]
        free_blocks = [b for b in self.memory_blocks if not b['allocated']]
        
        if not free_blocks:
            print("No free blocks to compact")
            return
        
        total_free = sum(b['end'] - b['start'] + 1 for b in free_blocks)
        new_blocks = []
        current_start = 0
        
        for block in allocated_blocks:
            size = block['end'] - block['start'] + 1
            new_block = {
                'start': current_start,
                'end': current_start + size - 1,
                'process': block['process'],
                'allocated': True
            }
            new_blocks.append(new_block)
            current_start += size
            self.processes[block['process']] = new_block
        
        if total_free > 0:
            new_blocks.append({
                'start': current_start,
                'end': current_start + total_free - 1,
                'process': None,
                'allocated': False
            })
        
        self.memory_blocks = new_blocks
        print("Memory compaction completed")
    
    def status_report(self):
        print("\nMemory Status Report:")
        for block in sorted(self.memory_blocks, key=lambda x: x['start']):
            if block['allocated']:
                print(f"Addresses [{block['start']}:{block['end']}] Process {block['process']}")
            else:
                print(f"Addresses [{block['start']}:{block['end']}] Unused")
        print(f"Total memory: {self.total_memory} bytes")
        print(f"Allocated: {sum(b['end'] - b['start'] + 1 for b in self.memory_blocks if b['allocated'])} bytes")
        print(f"Free: {sum(b['end'] - b['start'] + 1 for b in self.memory_blocks if not b['allocated'])} bytes\n")

def run_allocator(total_memory):
    allocator = MemoryAllocator(total_memory)
    print(f"Memory allocator initialized with {total_memory} bytes")
    print("Available commands:")
    print("  RQ <process> <size> <strategy> - Request memory (strategies: F, B, W)")
    print("  RL <process> - Release memory")
    print("  C - Compact memory")
    print("  STAT - Status report")
    print("  X - Exit")
    
    while True:
        try:
            command = input("allocator> ").strip().split()
            if not command:
                continue
            
            cmd = command[0].upper()
            
            if cmd == 'RQ' and len(command) == 4:
                try:
                    size = int(command[2])
                    if size <= 0:
                        print("Error: Size must be positive")
                        continue
                    allocator.request_memory(command[1], size, command[3].upper())
                except ValueError:
                    print("Error: Size must be an integer")
            
            elif cmd == 'RL' and len(command) == 2:
                allocator.release_memory(command[1])
            
            elif cmd == 'C' and len(command) == 1:
                allocator.compact_memory()
            
            elif cmd == 'STAT' and len(command) == 1:
                allocator.status_report()
            
            elif cmd == 'X' and len(command) == 1:
                print("Exiting memory allocator")
                break
            
            else:
                print("Invalid command. Available commands:")
                print("  RQ <process> <size> <strategy>")
                print("  RL <process>")
                print("  C")
                print("  STAT")
                print("  X")
        
        except KeyboardInterrupt:
            print("\nExiting memory allocator")
            break
        except Exception as e:
            print(f"Error: {e}")