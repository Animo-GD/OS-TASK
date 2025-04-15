def translate_virtual_address(virtual_address):
    """
    Translates a 32-bit virtual address to page number and offset for a 4KB page size system.
    
    Args:
        virtual_address (int): The virtual address to translate
        
    Returns:
        tuple: (page_number, offset) or None if invalid input
    """
    if not isinstance(virtual_address, int) or virtual_address < 0 or virtual_address >= 2**32:
        return None
    
    page_size = 4096  # 4KB
    page_number = virtual_address // page_size
    offset = virtual_address % page_size
    
    return page_number, offset

def print_address_translation(virtual_address):
    """
    Prints the translation of a virtual address in the required format.
    
    Args:
        virtual_address (int): The virtual address to translate and print
    """
    result = translate_virtual_address(virtual_address)
    if result is None:
        print("Error: Virtual address must be a 32-bit unsigned integer (0 to 4,294,967,295)")
        return
    
    page_number, offset = result
    print(f"The address {virtual_address} contains:")
    print(f"page number = {page_number}")
    print(f"offset = {offset}")

if __name__ == "__main__":
    virtual_address = 19986
    print_address_translation(virtual_address)