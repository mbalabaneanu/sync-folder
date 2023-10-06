# imports
import argparse
import os
import shutil
import filecmp
import time

# sync 2 folders -- syncing done periodically
# important parameter list:
# source_folder
# replica_folder
# log_file
# parser -- Object type that includes the main attributes: source_folder (path to it), 
# replica_folder (path to it), log_file (path to it), interval (int -- measured in seconds)

def synchronize_folders(source_folder, replica_folder, log_file):
    if not os.path.exists(source_folder):
        print(f"Source folder '{source_folder}' does not exist.")
        return
    if not os.path.exists(replica_folder):
        os.makedirs(replica_folder)
    dcmp = filecmp.dircmp(source_folder, replica_folder)

    for filename in dcmp.left_only + dcmp.diff_files:
        src_file = os.path.join(source_folder, filename)
        dst_file = os.path.join(replica_folder, filename)
        shutil.copy2(src_file, dst_file)
        print(f"Copied: {src_file} -> {dst_file}")
        log_file.write(f"Copied: {src_file} -> {dst_file}\n")
    for filename in dcmp.right_only:
        dst_file = os.path.join(replica_folder, filename)
        os.remove(dst_file)
        print(f"Removed: {dst_file}")
        log_file.write(f"Removed: {dst_file}\n")
    for subfolder in dcmp.common_dirs:
        synchronize_folders(
            os.path.join(source_folder, subfolder),
            os.path.join(replica_folder, subfolder),
            log_file)

def main():
    parser = argparse.ArgumentParser(description="Synchronize two folders.")
    parser.add_argument("source_folder", help="Source folder path")
    parser.add_argument("replica_folder", help="Replica folder path")
    parser.add_argument("log_file", help="Log file path")
    parser.add_argument("interval", type=int, help="Synchronization interval (seconds)")

    args = parser.parse_args()
    
    try:
        if args.interval <= 0:
            raise ValueError("Interval must be a positive integer.")
    except ValueError as e:
        print(f"Error: {e}")
        return

    if not os.path.exists(args.log_file):
        with open(args.log_file, "w") as log_file:
            log_file.write("Synchronization Log\n")

    while True:
        with open(args.log_file, "a") as log_file:
            synchronize_folders(args.source_folder, args.replica_folder, log_file)
        print(f"Synchronization completed. Waiting {args.interval} seconds for the next synchronization.")
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
