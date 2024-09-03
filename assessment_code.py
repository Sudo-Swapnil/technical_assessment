import csv
from collections import Counter
from typing import List, Dict, Tuple


def read_flow_data(path: str, seperator) -> List[List[str]]:
    """Read flow data from a text file and return it as a list of lists."""
    try:
        with open(path) as f:
            flow_data = []
            for data in f.read().splitlines():
                segments = data.strip()
                if segments != '':
                    segments = segments.split(seperator)
                    if len(segments) == 14:
                        flow_data.append(segments)
            return flow_data
    except Exception as e:
        print(f"Error reading flow data: {e}")
        return []


def create_protocol_map(path: str) -> Dict[str, str]:
    """Create a protocol mapping dictionary from a CSV file."""
    protocol_mapping = {}
    try:
        with open(path, mode='r') as file:
            next(file) # Skip header line
            for line in file:
                row = line.strip().split(',')
                protocol_mapping[row[0]] = row[1].lower()
    except Exception as e:
        print(f"Error reading protocol map: {e}")
    return protocol_mapping


def read_look_up_and_map(path: str) -> Dict[Tuple[str, str], str]:
    """Read a lookup TXT file and return a dictionary mapping."""
    dst_protocol_tag_map = {}
    try:
        with open(path, mode='r') as file:
            next(file) # Skip header line
            for line in file:
                row = line.strip().split(',')
                if any(row):
                    dst_protocol_tag_map[(row[0].strip(), row[1].strip().lower())] = row[2].lower().strip()
    except Exception as e:
        print(f"Error reading lookup map: {e}")
    return dst_protocol_tag_map


def map_dstport_protocol_tag(
    flow_data: List[List[str]], 
    protocol_mapping: Dict[str, str], 
    dst_protocol_tag_map: Dict[Tuple[str, str], str]
) -> Counter:
    """Map destination port and protocol to tags and count occurrences."""
    dst_port_idx, protocol_idx = 6, 7
    tag_count = Counter()
    port_protocol_count = Counter()
    for data in flow_data:
        composite_key = (data[dst_port_idx], protocol_mapping.get(data[protocol_idx]))
        port_protocol_count[composite_key] += 1
        if composite_key in dst_protocol_tag_map:
            tag = dst_protocol_tag_map[composite_key]
            tag_count[tag] += 1
        else:
            tag_count['untagged'] += 1
    return tag_count, port_protocol_count


def write_result_txt(tag_count: Counter, port_protocol_count: Counter, path: str):
    """Write the tag count and port/protocol count results to a text file."""
    try:
        with open(path, mode='w') as file:
            file.write("Count of matches for each tag, sample output shown below:\n\n")
            file.write("Tag, Count\n")
            for tag, count in tag_count.items():
                file.write(f"{tag},{count}\n")
            file.write("\n\nCount of matches for each port/protocol combination:\n\n")
            file.write("Port,Protocol,Count\n")
            for (port, protocol), count in port_protocol_count.items():
                file.write(f"{port},{protocol},{count}\n")
        print(f"SUCCESS: file {path}")
    except Exception as e:
        print(f"Error writing result TXT: {e}")

if __name__ == "__main__":
    flow_data = read_flow_data('./flow_log.txt', seperator=" ")
    protocol_mapping = create_protocol_map('./protocol_number_map.txt')
    dst_protocol_tag_map = read_look_up_and_map('./lookup.txt')
    tag_count, port_protocol_count = map_dstport_protocol_tag(flow_data, protocol_mapping, dst_protocol_tag_map)
    if tag_count:
        write_result_txt(tag_count, port_protocol_count, 'result.txt')
    else:
        print("Something went wrong, please check the input file paths / files / seperator of flow log")
 