import time
from fat_cli import FATFileSystem, Disk as FATDisk
from inode_cli import INodeFileSystem, Disk as INodeDisk

def test_filesystem(fs_class, disk_class, label):
    disk = disk_class(num_blocks=200)
    fs = fs_class(disk)

    start = time.time()

    for i in range(50):
        fs.create_file(f"dosya_{i}.txt", 2)

    for i in range(50):
        fs.read_file(f"dosya_{i}.txt")

    for i in range(0, 50, 2):
        fs.delete_file(f"dosya_{i}.txt")

    elapsed = time.time() - start
    print(f"{label} sistemi {elapsed:.4f} saniyede tamamladı.\n")
    return elapsed

def main():
    print("=== FAT ve INODE Karşılaştırılması ===\n")

    fat_time = test_filesystem(FATFileSystem, FATDisk, "FAT")
    inode_time = test_filesystem(INodeFileSystem, INodeDisk, "INODE")

    print("=== Sonuçlar ===")
    print(f"FAT süresi  : {fat_time:.4f} saniye")
    print(f"INODE süresi  : {inode_time:.4f} saniye")

    if inode_time < fat_time:
        print("\nINODE sistemi daha hızlı çalıştı.")
    else:
        print("\nFAT sistemi daha hızlı çalıştı.")

if __name__ == "__main__":
    main()
