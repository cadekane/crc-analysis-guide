import os
import csv
import re
import sys
from datetime import datetime

def process_directory(sample_dir, csv_writer, sequence_date, sequence_platform, sequence_center):
    sample_name = os.path.basename(sample_dir)
    sample_type = 'N' if '_NA' in sample_name else 'T' if '_TA' in sample_name else 'Unknown'
    subject_id = sample_name.replace('_NA', '').replace('_TA', '')

    file_list = os.listdir(sample_dir)
    file_list = [f for f in file_list if f.endswith('.fq.gz')]

    pattern = re.compile(r'^(V\d+)_L(\d+)_([A-Za-z0-9-]+)-(\d+)_(\d)\.fq\.gz$')

    processed_readgroups = set()  # Store processed readgroups

    for filename in file_list:
        match = pattern.match(filename)
        if match:
            identifier, lane, sample, hyphen_number, pair = match.groups()
            fq1_path = os.path.abspath(os.path.join(sample_dir, f"{identifier}_L{lane}_{sample}-{hyphen_number}_1.fq.gz"))
            fq2_path = os.path.abspath(os.path.join(sample_dir, f"{identifier}_L{lane}_{sample}-{hyphen_number}_2.fq.gz"))
            readgroup = f"{sample_name}_L{lane}_{hyphen_number}"

            if readgroup in processed_readgroups:
                # Skip processing if readgroup has already been processed
                continue

            # Add readgroup to processed set
            processed_readgroups.add(readgroup)

            csv_writer.writerow([
                readgroup,  # readgroup
                sample_name,  # sample_name
                subject_id,  # subject_id
                sample_type,  # sample_type
                fq1_path,  # absolute_path_to_fq1
                fq2_path,  # absolute_path_to_fq2
                sample_name,  # library_name
                sample_name,  # platform_unit
                sequence_date,  # sequence_date
                sequence_platform,  # sequence_platform
                sequence_center  # sequence_center
            ])
        else:
            print(f'Filename did not match pattern: {filename}')

def main(parent_directory, output_csv_path):
    sequence_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    sequence_platform = 'ILLUMINA'  # Replace with actual platform
    sequence_center = 'BGI'      # Replace with actual center

    with open(output_csv_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([
            'readgroup', 'sample_name', 'subject_id', 'sample_type',
            'absolute_path_to_fq1', 'absolute_path_to_fq2', 'library_name',
            'platform_unit', 'sequence_date', 'sequence_platform', 'sequence_center'
        ])

        for sample_dir in os.listdir(parent_directory):
            sample_dir_path = os.path.join(parent_directory, sample_dir)
            if os.path.isdir(sample_dir_path):
                process_directory(sample_dir_path, csv_writer, sequence_date, sequence_platform, sequence_center)

    print(f'File list with extracted data written to {output_csv_path}')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <parent_directory> <output_csv_path>")
        sys.exit(1)

    parent_directory = sys.argv[1]
    output_csv_path = sys.argv[2]

    main(parent_directory, output_csv_path)
