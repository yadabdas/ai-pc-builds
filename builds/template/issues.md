# 🚩 Issues and Resolutions – Build <yourname>, <year>

Describe any problems you encountered and how you solved them.

### 🧩 Example: GPU PCIe Link Width Reduced
- **Issue:** GPU dropped to x8 link width after installing NVMe in M.2_1.
- **Resolution:** Moved NVMe to chipset slot (M.2_4), verified x16 bandwidth.
  ```bash
  sudo lspci -v -s 01:00.0 | grep Width
  ```

### ⚙️ Example: NVIDIA Driver Not Detected
- **Issue:** `nvidia-smi` shows “No devices found.”
- **Resolution:**
  ```bash
  sudo apt purge nvidia-*
  sudo apt install nvidia-driver-575-open nvidia-dkms-575-open
  sudo reboot
  ```

### 💥 Example: PyCUDA Build Errors
- **Issue:** `libstdc++.so` mismatch or FP16 compile errors.
- **Resolution:** Adjusted `LD_LIBRARY_PATH` and rebuilt PyCUDA.

## ✅ Final Check
- GPU visible? `yes/no`
- CUDA operational? `yes/no`
- Model export successful? `yes/no`

⚠️ **Disclaimer:** BIOS flashing and kernel modifications may void warranties.  
See the [project disclaimer](../../DISCLAIMER.md).
