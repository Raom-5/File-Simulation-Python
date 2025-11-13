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

class FATFileSystem:
    def __init__(self, disk):
        self.disk = disk
        self.fat = [-1] * disk.num_blocks
        self.files = {}

    def create_file(self, name, size_blocks):
        if name in self.files:
            print("Hata: Dosya zaten mevcut.")
            return
        try:
            blocks = [self.disk.allocate_block() for _ in range(size_blocks)]
        except RuntimeError as e:
            print(e)
            return
        
        for i in range(len(blocks) - 1):
            self.fat[blocks[i]] = blocks[i + 1]
        self.fat[blocks[-1]] = -1
        self.files[name] = blocks[0]

        for i, block in enumerate(blocks):
            self.disk.blocks[block] = f"{name} içeriği (blok {i})"

        print(f"{name} oluşturuldu ({size_blocks} blok).")

    def read_file(self, name):
        if name not in self.files:
            print("Dosya bulunamadı.")
            return
        block = self.files[name]
        chain = []
        print(f"\n--- {name} içeriği ---")
        while block != -1:
            chain.append(block)
            print(f"Blok {block}: {self.disk.blocks[block]}")
            block = self.fat[block]
        print(f"Blok zinciri: {chain}\n")

    def delete_file(self, name):
        if name not in self.files:
            print("Dosya bulunamadı.")
            return
        block = self.files[name]
        while block != -1:
            next_block = self.fat[block]
            self.disk.free_block(block)
            self.fat[block] = -1
            block = next_block
        del self.files[name]
        print(f"{name} silindi.")

    def list_files(self):
        if not self.files:
            print("Sistemde hiç dosya yok.")
        else:
            print("Dosyalar:", list(self.files.keys()))

def run_cli():
    disk = Disk(num_blocks=20)
    fs = FATFileSystem(disk)

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

