# 📊 Benchmarks – Build 1 (Yadab, 2025)

This file presents performance metrics for the AI PC build, tested with a **structured asset-valuation workload** (100 records, 3.2 GB dataset) using PyTorch, ONNX Runtime, and PyCUDA on the NVIDIA RTX 5080.

---

## 🎯 Benchmark Goals
These benchmarks measure real-world compute and I/O efficiency for mid-size structured datasets — suitable for developers running local AI experiments on similar data scales.  
The goal is to assess **training throughput, inference latency, and GPU utilization** on consumer-grade AI hardware.

---

## ⚙️ System Configuration Summary
| Component | Details |
|------------|----------|
| **CPU** | AMD Ryzen 9 9950X (16 cores, 32 threads, 5.7 GHz) |
| **GPU** | ASUS TUF RTX 5080 (16 GB GDDR7, CUDA 12.9) |
| **RAM** | 128 GB DDR5-5600 |
| **Storage** | Samsung 990 PRO NVMe (2 TB) |
| **OS** | Ubuntu 24.04 LTS |
| **Frameworks** | PyTorch 2.5.1, ONNX Runtime 1.22.0, PyCUDA 2025.1 |

---

## 🧩 Workload Overview
- **Dataset:** 100 asset records (`records.parquet`) with attributes such as `value` (USD, float), `coverage` (%, float), `frontage` (m, float), `area` (sq. m, float).  
- **Model:** Multi-layer perceptron (MLP, ~1M parameters) trained in PyTorch and exported to ONNX (`model.onnx`).  
- **Task:** Predict record values and filter those below $500K.  

---

## 🧠 Benchmarks

### 1. PyTorch Training
- **Setup:** `python train_model.py` in `cuda_env`.  
- **Metrics:**
  - Loss: 0.0233 after 500 epochs  
  - Value range: ~$100K–$1M (e.g., $478,779.72 for record 0)  
  - Time: ~10 minutes on RTX 5080 (CUDA 12.9)  
- **Command:**
  ```bash
  conda activate cuda_env
  python train_model.py
  ```

---

### 2. ONNX C++ Inference
- **Setup:** `./compile_and_profile.sh` using `infer_records.cpp` with ONNX Runtime 1.22.0 (CUDA backend).  
- **Metrics:**
  - Output: 47 records with predicted values < $500K  
  - Inference Time: ~0.1 seconds  
  - Host-to-Device Transfer: 2.642 MB (Nsight Systems)  
- **Command:**
  ```bash
  cd ~/project/asset_pipeline/src
  ./compile_and_profile.sh
  ```

---

### 3. PyCUDA Performance
- **Setup:** `python test_pycuda.py` – matrix addition kernel (1024 elements, `float`).  
- **Metrics:**
  - Execution: Successful, no linkage errors  
  - Time: ~0.01 seconds for 1024-element addition  
- **Command:**
  ```bash
  conda activate cuda_env
  python test_pycuda.py
  ```

---

## 🔍 Profiling
- **Tool:** Nsight Systems  
- **Command:**
  ```bash
  nsys profile --trace=cuda,osrt --cuda-memory-usage=true --output=profile_report --force-overwrite=true ./infer_records
  nsys stats profile_report.nsys-rep > report_stats.txt
  ```
- **Results:**
  - Confirmed CUDA kernel activity (CUTLASS GEMM)  
  - 2.642 MB host-to-device transfers  
  - GPU utilization: ~80% during training (monitored via `nvtop`)  

---

## 🧾 Notes
- Dataset scaling supported up to 3.2 GB by adjusting `n_records` in `generate_records.py`.  
- Training reproducible using `scripts/train_model.py` under identical seed and environment conditions.  
- Profiling reports stored in `/mnt/data/profiles/` for long-term comparison.

---

⚙️ **Note:** These results are provided as an illustrative example of local AI workload performance.  
They are **not official benchmarks** and are **not intended for hardware comparison or certification purposes**.  
Performance may vary depending on drivers, system configuration, and workload size.


⚠️ **Disclaimer:** These benchmarks are for educational and experimental use only.  
System-level modifications (e.g., overclocking, driver changes) may affect results.  
Refer to the [project disclaimer](../../DISCLAIMER.md) for detailed terms and liability limitations.