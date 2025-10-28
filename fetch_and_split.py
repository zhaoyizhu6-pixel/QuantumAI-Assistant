import os, tarfile, math, hashlib
from pathlib import Path

# 1) 下载并保存向量模型
#    使用 sentence-transformers 自动下载并缓存后，保存到 ./model 目录
from sentence_transformers import SentenceTransformer

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
OUT_DIR = Path(".")
MODEL_DIR = OUT_DIR / "model" / MODEL_NAME
ARCHIVE = OUT_DIR / "VectorModel.tar.gz"
PARTS_DIR = OUT_DIR / "parts"
CHUNK_MB = 95  # 每个分包约 95MB，可自行调整

def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def write_sha256_line(out, path: Path):
    out.write(f"{path.name}\t{sha256_of_file(path)}\n")

def main():
    print("==> 下载中文向量模型（如已存在会直接读取缓存）...")
    model = SentenceTransformer(MODEL_NAME)
    MODEL_DIR.parent.mkdir(parents=True, exist_ok=True)
    model.save(str(MODEL_DIR))
    print(f"✅ 模型已保存到：{MODEL_DIR}")

    # 2) 打包成 tar.gz
    if ARCHIVE.exists():
        ARCHIVE.unlink()
    print("==> 打包为 VectorModel.tar.gz ...")
    with tarfile.open(ARCHIVE, "w:gz") as tar:
        tar.add(MODEL_DIR, arcname=f"model/{MODEL_NAME}")
    print(f"✅ 归档完成：{ARCHIVE} (size={ARCHIVE.stat().st_size/1e6:.1f} MB)")

    # 3) 切分分包
    PARTS_DIR.mkdir(exist_ok=True)
    chunk_bytes = CHUNK_MB * 1024 * 1024
    total = ARCHIVE.stat().st_size
    n = math.ceil(total / chunk_bytes)
    print(f"==> 切分为 {n} 个分包，每个约 {CHUNK_MB}MB ...")

    with open(ARCHIVE, "rb") as src:
        for i in range(1, n+1):
            part_path = PARTS_DIR / f"VectorModel.part{i:02d}"
            with open(part_path, "wb") as dst:
                dst.write(src.read(chunk_bytes))
            print(f"  - 写入 {part_path} ({part_path.stat().st_size/1e6:.1f} MB)")

    # 4) 校验和
    with open(OUT_DIR/"sha256.txt","w",encoding="utf-8") as out:
        write_sha256_line(out, ARCHIVE)
        for i in range(1, n+1):
            write_sha256_line(out, PARTS_DIR / f"VectorModel.part{i:02d}")
    print("✅ 已生成 sha256.txt 校验文件")
    print("🎉 完成。请将 parts/ 拷贝到目标机器。")

if __name__ == "__main__":
    main()
