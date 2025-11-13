import time

class Disk:
    def __init__(self, num_blocks=100):
        self.num_blocks = num_blocks
        self.blocks = [None] * num_blocks
        self.free_blocks = list(range(num_blocks))

    def allocate_block(self):
        if not self.free_blocks:
            raise RuntimeError("Disk dolu!")
        return self.free_blocks.pop(0)

    def free_block(self, block_index):
        self.blocks[block_index] = None
        self.free_blocks.append(block_index)


class INodeFileSystem:
    def __init__(self, disk):
        self.disk = disk
        self.inode_table = {}

    def create_file(self, name, size_blocks):
        if name in self.inode_table:
            print("Hata: Dosya zaten mevcut.")
            return
        try:
            blocks = [self.disk.allocate_block() for _ in range(size_blocks)]
        except RuntimeError as e:
            print(e)
            return

        
        for i, block in enumerate(blocks):
            self.disk.blocks[block] = f"{name} içeriği (blok {i})"
 
        inode = {
            "name": name,
            "blocks": blocks
        }
        self.inode_table[name] = inode
        print(f"{name} oluşturuldu ({size_blocks} blok).")

    def read_file(self, name):
        if name not in self.inode_table:
            print("Dosya bulunamadı.")
            return

        inode = self.inode_table[name]
        print(f"\n--- {name} içeriği ---")
        for block in inode["blocks"]:
            print(f"Blok {block}: {self.disk.blocks[block]}")
        print(f"Blok listesi: {inode['blocks']}\n")

    def delete_file(self, name):
        if name not in self.inode_table:
            print("Dosya bulunamadı.")
            return

        inode = self.inode_table[name]
        for block in inode["blocks"]:
            self.disk.free_block(block)
        del self.inode_table[name]
        print(f"{name} silindi.")

    def list_files(self):
        if not self.inode_table:
            print("Sistemde hiç dosya yok.")
        else:
            print("Dosyalar:", list(self.inode_table.keys()))


def run_cli():
    disk = Disk(num_blocks=20)
    fs = INodeFileSystem(disk)

    while True:
        cmd = input("Komut (create/read/delete/ls/exit): ").strip().lower()
        if cmd == "exit":
            break
        elif cmd == "create":
            name = input("Dosya adı: ")
            size = int(input("Kaç blokluk dosya: "))
            fs.create_file(name, size)
        elif cmd == "read":
            name = input("Dosya adı: ")
            fs.read_file(name)
        elif cmd == "delete":
            name = input("Dosya adı: ")
            fs.delete_file(name)
        elif cmd == "ls":
            fs.list_files()
        else:
            print("Geçersiz komut!")


if __name__ == "__main__":
    run_cli()


