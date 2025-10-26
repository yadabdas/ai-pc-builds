# 🧠 AI PC Build Guide

[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](https://github.com/yadabdas/ai-pc-builds)

*A practical, community-driven reference for building and benchmarking affordable AI workstations for research, learning, and small-scale experimentation.*

Welcome to **AI PC Build Guide**, a collaborative open-source project that helps developers **build and configure PCs for AI workloads at home**.  
This repository provides detailed hardware and software guides, troubleshooting tips, performance benchmarks, and a directory of community-submitted builds.

👉 Project home: [github.com/yadabdas/ai-pc-builds](https://github.com/yadabdas/ai-pc-builds)

---

## 💬 Founder’s Note

This project started as a personal experiment to make AI development **simpler and more affordable**.  
After struggling with hardware limits, driver issues, and the high cost of cloud compute, I realized how many developers face the same barriers just to get started.

So I built this guide — not as a benchmark contest, but as a **shared notebook for AI builders**.  
It’s a place where anyone can learn, share, and optimize their own setup without burning time or money on trial and error.

> The mission is simple: make local AI experimentation accessible to everyone who wants to build, learn, and explore.

---

## 🎯 Goals
- **Assist developers** starting AI projects with practical, tested PC build guides.  
- **Foster collaboration** by allowing contributors to share their builds, get feedback, and learn from others’ setups.

---

## ⚙️ Features
- **Hardware Guides** — Recommendations for CPUs, GPUs, RAM, and storage optimized for AI (e.g., NVIDIA RTX 5080, 128 GB DDR5).  
- **Software Setup** — Step-by-step instructions for Ubuntu 24.04, CUDA, PyTorch, TensorFlow, PyCUDA, and more.  
- **Troubleshooting** — Solutions for common issues (e.g., NVIDIA driver errors, PCIe lane conflicts).  
- **Benchmarks** — Performance metrics for AI workloads (e.g., training times, inference speeds).  
- **Community Builds** — Directory for user-submitted PC builds with configs and scripts.

---

## 🧩 Example Build
**Based on a real setup (Summer 2025) for asset-level price prediction (3.2 GB dataset):**

### 🔧 Hardware
| Component | Details |
|-----------|---------|
| CPU | AMD Ryzen 9 9950X (16 cores, 5.7 GHz) |
| GPU | ASUS TUF RTX 5080 (16 GB GDDR7, CUDA 12.9) |
| RAM | 128 GB DDR5-5600 (Crucial, 2×64 GB) |
| Storage | 3 TB NVMe SSD (Samsung 990 PRO) + 4 TB HDD |

### 💻 Software
- **OS**: Ubuntu 24.04 LTS  
- **Environments**: Conda (`cuda_env`, `tf_env`, `pytorch_env`)  
- **Tools**: PyTorch 2.5.1, TensorFlow 2.14.0, PyCUDA 2025.1, ONNX Runtime 1.22.0  

### 📊 Sample Results (Observed on This Build)
These are sample metrics collected during local experimentation — not official benchmarks.

| Task | Metric | Result |
|------|---------|--------|
| PyTorch MLP (asset-level dataset) | Final loss | ~0.02 after 100 samples |
| ONNX C++ inference | Latency | ~0.1 s for 47 records (< $500 K each) |
| CUDA profiling | Host→device transfer | ~2.6 MB/s during batch inference |


### ⚡ Quick Start
Set up a PyTorch environment:
```bash
conda create -n pytorch_env python=3.11 -c conda-forge
conda activate pytorch_env
conda install pytorch==2.5.1 pytorch-cuda=12.4 -c pytorch -c nvidia
python -c "import torch; print(torch.cuda.is_available())"
```

---

## 🚀 Getting Started
1. **Explore Builds:** Browse [`builds/`](./builds) for example setups (e.g., `build_1_yadab_2025`).  
2. **Read Guides:** See [`docs/`](./docs) for hardware/software recommendations and troubleshooting.  
3. **Run Benchmarks:** Use scripts in [`scripts/benchmark_scripts/`](./scripts/benchmark_scripts) to test performance.  
4. **Contribute:** Submit your own build using the [`template/`](./builds/template) (see [`CONTRIBUTING.md`](./CONTRIBUTING.md)).

---

## 🤝 How to Contribute
1. Fork this repository and create a new directory under `builds/` (e.g., `build_2_yourname_year`).  
2. Include:  
   - `hardware.md`  
   - `software.md`  
   - `issues.md`  
   - `benchmarks.md`  
   - *(Optional)* `scripts/` for setup or tests  
3. Follow the format in [`builds/template/`](./builds/template).  
4. Submit a pull request — details in [`CONTRIBUTING.md`](./CONTRIBUTING.md).

---

## 📄 License
📜 Licensed under the [MIT License](./LICENSE).  
See also the [Disclaimer](./DISCLAIMER.md) for usage terms and safety notices.

---

## 📬 Contact
For questions or collaboration:  
- Open an issue on GitHub  
- Join the discussion in [GitHub Discussions](https://github.com/yadabdas/ai-pc-builds/discussions)

---

## 🧭 Roadmap
- Add `build_2_midrange_4070Ti` and `build_3_entry_4060` examples  
- Publish community benchmark scripts  
- Include ROCm and Windows/WSL2 build guides  

**Note**: This repository shall be updated with new hardware (e.g., RTX 5090, Zen 6 CPUs) and software as they release.