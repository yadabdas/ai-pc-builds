# 💻 Software – Build 1 (Yadab, 2025)

This file details the software setup for the AI PC build, optimized for **AI workloads such as asset valuation and data-driven model experimentation**.  
The system runs Ubuntu 24.04 LTS with Conda environments for isolated development and testing.

---

## 🖥️ Operating System
- **Ubuntu 24.04 LTS Desktop**: Installed on Samsung 990 PRO 2 TB SSD (`nvme0n1`).
  ```bash
  # Boot from SanDisk Ultra 16GB USB and follow Ubuntu installer
  ```
- **Verification:**
  ```bash
  lsb_release -a
  # Expected: Ubuntu 24.04 LTS
  ```

---

## 🧩 Development Environments

### Miniconda
Used for managing Python environments and dependencies.
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

---

### Conda Environment: `cuda_env`
- **Purpose:** Primary environment for PyTorch and PyCUDA.
- **Python:** 3.11.7

**Setup:**
```bash
conda create -n cuda_env python=3.11 jupyter pandas numpy pyarrow torch onnx -c conda-forge
conda activate cuda_env
pip install onnxruntime-gpu==1.22.0
```

**PyCUDA (2025.1, source-built):**
```bash
git clone https://github.com/inducer/pycuda.git
cd pycuda
./configure.py --cuda-root=/usr/local/cuda-12.9 --no-use-shipped-boost
python setup.py install
```

**Verification:**
```bash
python -c "import pycuda.driver as cuda; cuda.init(); print(cuda.Device(0).compute_capability())"
# Expected: (12, 0)
```

---

### Conda Environment: `tf_env`
- **Purpose:** TensorFlow development.
- **Setup:**
```bash
conda create -n tf_env python=3.11 jupyter pandas numpy -c conda-forge
conda activate tf_env
conda install tensorflow-gpu=2.14.0 cudatoolkit=11.8 cudnn=8.8 -c conda-forge
pip uninstall torch torchvision torchaudio -y
```
**Verification:**
```bash
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
# Expected: [PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]
```

---

### Conda Environment: `pytorch_env`
- **Purpose:** PyTorch development.
- **Setup:**
```bash
conda create -n pytorch_env python=3.11 jupyter pandas numpy -c conda-forge
conda activate pytorch_env
conda install pytorch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 pytorch-cuda=12.4 -c pytorch -c nvidia
```
**Verification:**
```bash
python -c "import torch; print(torch.cuda.is_available())"
# Expected: True
python -c "import torch; x = torch.rand(5, 3, device='cuda'); print(x)"
```

---

## 🧰 Additional Tools

### IntelliJ IDEA Community Edition (2025.1.2)
For Java preprocessing and data conversions (e.g., XML → Parquet).
```bash
wget https://download.jetbrains.com/idea/ideaIC-2025.1.2.tar.gz
tar -xzf ideaIC-2025.1.2.tar.gz -C /opt/
/opt/idea-IC-2025.1.2/bin/idea.sh
```
**Dependencies:**
```bash
sudo apt install openjdk-21-jdk
```

---

### Visual Studio Code (1.90.0)
For Python development (PyTorch, TensorFlow).
```bash
wget -O code.deb https://update.code.visualstudio.com/latest/linux-deb-x64/stable
sudo apt install -y ./code.deb
```
**Extensions:** Python, PyTorch Snippets, Jupyter.

---

### Git & Maven
```bash
sudo apt install git maven
git config --global user.name "Yadab Das"
git config --global user.email "your.email@example.com"
```

---

### NVIDIA Drivers and CUDA
- **Driver:** 575.51.03 (CUDA 12.9 compatible)

**Installation:**
```bash
sudo apt update
sudo apt install nvidia-driver-575-open nvidia-dkms-575-open nvidia-utils-575
sudo dkms autoinstall
sudo reboot
```

> **Note:** Reboot after installation (`sudo reboot`) to activate the NVIDIA kernel modules.

**Verification:**
```bash
nvidia-smi
# Expected: RTX 5080, 16,303 MiB VRAM, CUDA 12.9
```

---

### Apache Arrow and Parquet
For reading and writing `.parquet` files in C++.
```bash
wget https://packages.apache.org/artifactory/arrow/ubuntu/apache-arrow-apt-source-latest-noble.deb
sudo apt install -y -V ./apache-arrow-apt-source-latest-noble.deb
sudo apt update
sudo apt install -y -V libarrow-dev libparquet-dev
```

---

### ONNX Runtime (1.22.0, GPU)
```bash
wget https://github.com/microsoft/onnxruntime/releases/download/v1.22.0/onnxruntime-linux-x64-gpu-1.22.0.tgz
tar -xzf onnxruntime-linux-x64-gpu-1.22.0.tgz
sudo mv onnxruntime-linux-x64-gpu-1.22.0/include/* /usr/local/include/
sudo mv onnxruntime-linux-x64-gpu-1.22.0/lib/* /usr/local/lib/
sudo ldconfig
```

---

## ⚡ Performance Check

Run this simple GPU test to confirm CUDA is active:
```bash
python -c "import torch, time; x=torch.rand((4096,4096),device='cuda'); t=time.time(); y=torch.mm(x,x); print('Time:', time.time()-t)"
```
**Expected:** The matrix multiply should complete within ~0.05–0.10 seconds on an RTX 5080.

---

## 🧭 Notes
- Secure Boot disabled in BIOS to allow Ubuntu boot.  
- Environment variable setup:
  ```bash
  export LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:/usr/local/cuda-12.9/lib64:$LD_LIBRARY_PATH
  ```

---

⚠️ **Disclaimer:** System-level changes such as driver installation or Secure Boot modification may affect system stability or warranties.  
Refer to the [project disclaimer](../DISCLAIMER.md) for full terms and liability limitations.