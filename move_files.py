#!/usr/bin/env python3
"""
This script allows users to clean up their Terra workspace by moving files from
within a TSV table to a more user-friendly interface. This is super messy as
all files/path names are hard-coded for my purposes. Places you'll have to edit
for yourself are marked accordingly.
"""

import argparse

def generate_tsv_and_move_script(tsv_name):
    with open(tsv_name, 'r') as fn:
        with open("new_table.tsv", 'w') as new_table:
            with open("move_cmds.txt", 'w') as ofn:
                for line in fn:
                    # This line checks for whether there are items in the line.
                    # Swap out with your bucket ID.
                    if "gs://fc-51aefb1c-4e8e-4dcb-a59c-62e318ea351a/" in line:
                        line = line.split('\t')
                        for idx, item in enumerate(line):
                            # Checks if the files haven't been cleaned up yet.
                            # Update with your path accordingly.
                            if "gs://" in item and "1KGP" not in item:
                                item_name = item.split('/')[-1].strip()
                                new_location = ""
                                # Cases for each column in the TSV. Swap out
                                # for your own purpose.
                                if item.endswith(".hc.vcf"):
                                    new_location = "gs://fc-51aefb1c-4e8e-4dcb-a59c-62e318ea351a/1KGP/HG002-Y/haplotype_caller/uncompressed/{}".format(item_name)
                                elif ".cram" in item:
                                    new_location = "gs://fc-51aefb1c-4e8e-4dcb-a59c-62e318ea351a/1KGP/HG002-Y/alignment/CRAMs/{}".format(item_name)
                                elif item.endswith(".global.dist.txt"):
                                    new_location = "gs://fc-51aefb1c-4e8e-4dcb-a59c-62e318ea351a/1KGP/HG002-Y/alignment/statistics/mosdepth/global_dist/{}".format(item_name)
                                elif "regions.bed.gz" in item:
                                    new_location = "gs://fc-51aefb1c-4e8e-4dcb-a59c-62e318ea351a/1KGP/HG002-Y/alignment/statistics/mosdepth/regions_bed/{}".format(item_name)
                                elif item.endswith(".region.dist.txt"):
                                    new_location = "gs://fc-51aefb1c-4e8e-4dcb-a59c-62e318ea351a/1KGP/HG002-Y/alignment/statistics/mosdepth/regions_dist/{}".format(item_name)
                                elif item.endswith(".summary.txt"):
                                    new_location = "gs://fc-51aefb1c-4e8e-4dcb-a59c-62e318ea351a/1KGP/HG002-Y/alignment/statistics/mosdepth/summary/{}".format(item_name)
                                elif ".samtools.stats.txt" in item:
                                    new_location = "gs://fc-51aefb1c-4e8e-4dcb-a59c-62e318ea351a/1KGP/HG002-Y/alignment/statistics/samtools/{}".format(item_name)
                                elif ".hc.vcf.gz" in item:
                                    new_location = "gs://fc-51aefb1c-4e8e-4dcb-a59c-62e318ea351a/1KGP/HG002-Y/haplotype_caller/compressed/{}".format(item_name)
                                elif item.endswith(".tar"):
                                    new_location = "gs://fc-51aefb1c-4e8e-4dcb-a59c-62e318ea351a/1KGP/HG002-Y/100_samples/joint_genotyping/genomics_db/{}".format(item_name)
                                elif item.endswith(".genotyped.vcf"):
                                    new_location = "gs://fc-51aefb1c-4e8e-4dcb-a59c-62e318ea351a/1KGP/HG002-Y/100_samples/joint_genotyping/interval_VCFs/uncompressed/{}".format(item_name)
                                elif ".genotyped.vcf.gz" in item:
                                    new_location = "gs://fc-51aefb1c-4e8e-4dcb-a59c-62e318ea351a/1KGP/HG002-Y/100_samples/joint_genotyping/interval_VCFs/compressed/{}".format(item_name)
                                # end cases.

                                if new_location:
                                    # Writes to new bucket.
                                    ofn.write("gsutil mv "+ item.strip() + " {}\n".format(new_location))
                                    # I have a requester pays bucket. You won't
                                    # be using the following line.
                                    # ofn.write("gsutil -u t2t-nhgri mv "+ item.strip() + " {}\n".format(new_location))
                                    line[idx] = new_location
                                else:
                                    line[idx] = item
                        if line[-1].endswith('\n'):
                            new_table.write('\t'.join(line))
                        else:
                            new_table.write('\t'.join(line) + '\n')
                    else:
                        new_table.write(line)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_tsv", type=str, help="the TSV file for the Terra table you want to move")
    args = parser.parse_args()
    print("Accessing TSV file {0}".format(args.input_tsv))

    generate_tsv_and_move_script(args.input_tsv)
    print("New TSV file and move script generated.")

main()