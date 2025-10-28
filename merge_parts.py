import os, tarfile, hashlib
from pathlib import Path

BASE = Path(".")
PARTS_DIR = BASE / "parts"
ARCHIVE = BASE / "VectorModel.tar.gz"
TARGET_DIR = BASE / "model" / "paraphrase-multilingual-MiniLM-L12-v2"

def sha256_of_file(path: Path) -> str:
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    assert PARTS_DIR.exists(), "未找到 parts/ 目录"
    parts = sorted(PARTS_DIR.glob("VectorModel.part*"))
    assert parts, "parts/ 内没有分包文件"
    print(f"==> 检测到 {len(parts)} 个分包，开始合并 ...")

    # 合并为单个 tar.gz
    with open(ARCHIVE, "wb") as out:
        for p in parts:
            with open(p, "rb") as src:
                out.write(src.read())
            print(f"  - 合并 {p.name}")
    print(f"✅ 合并完成：{ARCHIVE} (size={ARCHIVE.stat().st_size/1e6:.1f} MB)")

    # 解包到 model/ 目录
    TARGET_DIR.parent.mkdir(parents=True, exist_ok=True)
    print("==> 解包模型到 model/ ...")
    with tarfile.open(ARCHIVE, "r:gz") as tar:
        tar.extractall(BASE)
    print(f"✅ 模型已解压到：{TARGET_DIR}")
    print("🎉 完成。现在可以启动 app.py 使用向量/混合检索。")

if __name__ == "__main__":
    main()
