# 🚩 Issues and Resolutions – Build 1 (Yadab, 2025)

This file documents key issues encountered during the AI PC build setup and their resolutions, focusing on hardware, software, and AI workload challenges.  
The build was optimized for **AI workloads such as asset valuation and model experimentation**.

---

### 🧩 GPU PCIe Sharing Issue
- **Issue:** RTX 5080 in PCIe 5.0 x16 slot downgraded to x8 lanes due to conflict with M.2_1 slot (Samsung 990 PRO 2TB), causing `nvidia-smi` failure.  
- **Impact:** GPU detected as x8, reducing data throughput and training efficiency.  
- **Resolution:** Moved 1 TB SSD to M.2_4 slot (PCIe 4.0), freeing lanes for GPU (restored to x16, 64 GB/s). Updated BIOS to version 0805.  
  ```bash
  sudo lspci -v -s 01:00.0
  # Expected: LnkSta: Speed 16GT/s, Width x16
  ```

---

### ⚙️ NVIDIA Driver Not Detecting GPU
- **Issue:** `nvidia-smi` returned “No devices were found” due to outdated Nouveau driver.  
- **Impact:** GPU unavailable to CUDA and PyTorch environments.  
- **Resolution:** Purged Nouveau and installed NVIDIA open kernel modules.  
  ```bash
  sudo apt purge nvidia-*
  sudo apt install nvidia-driver-575-open nvidia-dkms-575-open nvidia-utils-575
  sudo dkms autoinstall
  sudo reboot
  nvidia-smi
  # Expected: RTX 5080, driver 575.51.03, CUDA 12.9
  ```
- **Additional Step:** Blacklisted Nouveau to prevent future conflicts.  
  ```bash
  echo -e "blacklist nouveau\noptions nouveau modeset=0" | sudo tee /etc/modprobe.d/blacklist-nouveau.conf
  sudo update-initramfs -u
  sudo reboot
  ```

---

### 🧠 PyCUDA libstdc++ Linkage Error
- **Issue:** `ImportError: /home/yadab/miniconda3/envs/cuda_env/lib/libstdc++.so.6: version 'GLIBCXX_3.4.32' not found`.  
- **Impact:** PyCUDA failed to load due to conflicting GCC libraries in Conda.  
- **Resolution:** Used system `libstdc++` (GCC 13.3.0) instead of Conda’s version.  
  ```bash
  export LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:/usr/local/cuda-12.9/lib64:$LD_LIBRARY_PATH
  pip install pycuda --no-cache-dir
  ```

---

### 💥 PyCUDA cuda_fp16.h Compilation Errors
- **Issue:** `CompileError: more than one instance of overloaded function "operator++" has "C" linkage` in `cuda_fp16.h` for sm_120 architecture.  
- **Impact:** Kernel compilation failed on CUDA 12.9.  
- **Resolution:** Switched to `float` kernels to avoid CUDA 12.9 FP16 linkage bug.  
- **Follow-up:** Monitoring PyCUDA and NVIDIA repositories for upstream fix.

---

### 🧰 Motherboard Invalid Display Codes
- **Issue:** Q-Code LED errors (“0d”, “15”) during POST, likely due to early BIOS not supporting Ryzen 9 9950X or DDR5-5600.  
- **Impact:** System failed to boot until multiple restarts.  
- **Resolution:** Flashed BIOS to version 0805 using ASUS EZ Flash 3 via USB (SanDisk Ultra 16GB).  
  ```bash
  # Download BIOS from ASUS support, copy to FAT32 USB drive, and update through BIOS > Tools > EZ Flash 3 Utility
  ```

---

### 🧱 ONNX Runtime Compilation Errors
- **Issue:** `infer_folios.cpp` failed to compile due to incorrect include paths and ONNX Runtime API mismatches.  
- **Impact:** C++ inference build incomplete.  
- **Resolution:** Corrected paths and reinstalled ONNX Runtime 1.22.0.  
  ```bash
  sudo rm -rf /usr/local/include/onnxruntime
  sudo mv onnxruntime-linux-x64-gpu-1.22.0/include/* /usr/local/include/
  sudo mv onnxruntime-linux-x64-gpu-1.22.0/lib/* /usr/local/lib/
  sudo ldconfig
  ```

---

## ✅ Verification Summary
After all fixes and optimizations:
- `nvidia-smi` detects RTX 5080 with CUDA 12.9  
- PCIe slot confirmed at x16 bandwidth (64 GB/s)  
- PyCUDA and ONNX Runtime build successfully  
- BIOS stable with Ryzen 9 9950X and DDR5-5600  
- All AI workloads (PyTorch, TensorFlow, C++) operational

---

⚠️ **Disclaimer:** Hardware and software modifications (e.g., BIOS flashing, driver replacement) may void warranties or cause instability.  
Refer to the [project disclaimer](../DISCLAIMER.md) for detailed terms and limitations of liability.