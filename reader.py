import struct

def read_index_entries(file_path, offset, entry_size, num_entries):
    with open(file_path, 'rb') as f:
        f.seek(offset)
        index_entries = []
        for _ in range(num_entries):
            entry = f.read(entry_size)
            if len(entry) < entry_size:
                break  # End of file or malformed entry
            # Unpack entry as (DD, SS, ls, LL)
            disk_number = entry[0]
            start_sector = (entry[1] << 8) | entry[2]
            length = entry[3]  # Correctly using the 4th byte for length
            index_entries.append((disk_number, start_sector, length))
        return index_entries

def extract_data_from_sectors(disk_path, start_sector, num_sectors, sector_size=512):
    with open(disk_path, 'rb') as f:
        f.seek(start_sector * sector_size)
        data = f.read(num_sectors * sector_size)
        return data

def save_data(data, output_path):
    with open(output_path, 'wb') as f:
        f.write(data)

def main():
    disk1_file_path = 'ten_a.fdi'  # Path to the first disk image
    disk2_file_path = 'ten_b.fdi'  # Path to the second disk image
    index_offset = 0x1412
    entry_size = 4
    num_entries = 10  # Number of entries in the index (adjust based on your file)

    index_entries = read_index_entries(disk1_file_path, index_offset, entry_size, num_entries)

    for i, (disk_number, start_sector, length) in enumerate(index_entries):
        disk_path = disk2_file_path if disk_number == 2 else disk1_file_path
        data = extract_data_from_sectors(disk_path, start_sector, length)
        output_file_path = f'extracted_file_{i}.bin'
        save_data(data, output_file_path)
        print(f'Extracted file {i}: {output_file_path}')

if __name__ == '__main__':
    main()
