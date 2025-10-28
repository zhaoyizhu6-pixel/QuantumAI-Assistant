# Part 2 — VectorModel Splitter（向量模型分包工具）

本工具用于在**有网的环境**下载中文向量模型 `paraphrase-multilingual-MiniLM-L12-v2`，
并将其**切分为多个小包**，以便你拷贝到目标演示机上离线使用。

## 一、下载安装与分包（在有网电脑执行）
```bash
uv sync
uv run python fetch_and_split.py
```
完成后会在当前目录生成：
```
VectorModel.tar.gz        # 模型完整归档
parts/
  VectorModel.part01
  VectorModel.part02
  ...
sha256.txt                # 完整包与分包的校验和
```

## 二、在目标机上合并（可完全离线）
将 `parts/` 整个文件夹复制到目标机器的
`QuantumAI-Memory-Assistant-v2.0/` 目录下，然后执行：
```bash
uv run python merge_parts.py
```
合并成功后，会得到：
```
model/paraphrase-multilingual-MiniLM-L12-v2/   # 模型文件夹
```
重启 `uv run python app.py`，即可在网页中把检索模式切换为「向量/混合」。

---

## 说明
- 你可以调整分包大小：编辑 `fetch_and_split.py` 里的 `CHUNK_MB`。
- 如果你已经手动放入模型文件夹（`model/paraphrase-multilingual-MiniLM-L12-v2`），无需使用此分包工具。
