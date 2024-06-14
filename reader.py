import struct

def read_index_entries(file_data, offset):
    entry_size = 4
    index_entries = []
    offset += 0x1000 # Skip FDI header
    while (offset + 4 <= len(file_data)) and (file_data[offset] != 0):
        # Unpack entry as (DD, SS, ls, LL) -> disk DD, start sector sSS, length in sectors LLl
        disk_number = file_data[offset]
        start_sector = file_data[offset + 1] | ((file_data[offset + 2] & 0x0F) << 8)
        length = (file_data[offset + 3] << 4) | ((file_data[offset + 2] & 0xF0) >> 4)
        index_entries.append((disk_number, start_sector, length))

        offset += 4
    return index_entries

def extract_data_from_sectors(disk_data, start_sector, num_sectors, sector_size=0x400):
    offset = start_sector * sector_size
    offset += 0x1000 # Skip FDI header
    end_offset = offset + num_sectors * sector_size
    data = disk_data[offset:end_offset]
    return data

def extract_entries(disk1_data, disk2_data, index_entries, suffix):
    for i, (disk_number, start_sector, length) in enumerate(index_entries):
        disk_data = disk2_data if disk_number == 2 else disk1_data
        data = extract_data_from_sectors(disk_data, start_sector, length)
        output_file_path = f'{suffix}_{i}.{suffix}'
        save_data(data, output_file_path)
        print(f'Extracted file {i}: {output_file_path}')

def save_data(data, output_path):
    with open(output_path, 'wb') as f:
        f.write(data)

def main():
    disk1_file_path = 'ten_a.fdi'  # Path to the first disk image
    disk2_file_path = 'ten_b.fdi'  # Path to the second disk image
    index_offsets = [0x2412, 0x2612, 0x2812, 0x2A12] # All on the first disk
    num_entries = 10  # Number of entries in the index (adjust based on your file)

    with open(disk1_file_path, 'rb') as f: disk1_data = f.read()
    with open(disk2_file_path, 'rb') as f: disk2_data = f.read()

    graphic_entries = read_index_entries(disk1_data, index_offsets[0])
    animation_entries = read_index_entries(disk1_data, index_offsets[1])
    script_entries = read_index_entries(disk1_data, index_offsets[2])
    music_entries = read_index_entries(disk1_data, index_offsets[3])

    extract_entries(disk1_data, disk2_data, graphic_entries, 'img')
    extract_entries(disk1_data, disk2_data, animation_entries, 'ani')
    extract_entries(disk1_data, disk2_data, script_entries, 'scd')
    extract_entries(disk1_data, disk2_data, music_entries, 'mus')

if __name__ == '__main__':
    main()
