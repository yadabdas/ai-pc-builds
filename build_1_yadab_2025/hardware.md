# 🛠️ Hardware – Build 1 (Yadab, 2025)

This build lists the hardware components used in a workstation optimized for **AI workloads such as asset valuation and data-driven modeling**.  
All prices are *approximate* in CAD, based on Amazon.ca / Best Buy Canada as of **Summer 2025**.

| Component | Specification | Approx. Price (CAD) | Vendor / Source |
|------------|---------------|---------------------|-----------------|
| **CPU** | AMD Ryzen 9 9950X (16 cores, 32 threads, 5.7 GHz max) | ~$770 | Best Buy (store pickup) |
| **Motherboard** | ASUS ROG Strix X870E-E Gaming WiFi (AM5, X870, ATX) | ~$720 | Amazon.ca (Summer 2025 order) |
| **GPU** | ASUS TUF Gaming GeForce RTX 5080 OC Edition (16 GB GDDR7, 10 752 CUDA cores, CUDA 12.9) | ~$1 960 | Best Buy (store pickup) |
| **RAM** | Crucial 128 GB Kit (2 × 64 GB) DDR5-5600 (UDIMM, MemTest86 passed) | ~$480 | Amazon.ca (Summer 2025 order) |
| **Storage – SSD 1** | Samsung 990 PRO w/ Heatsink 2 TB (PCIe Gen 4 NVMe M.2, `nvme0n1`, Ubuntu 24.04 boot) | ~$290 | Amazon.ca |
| **Storage – SSD 2** | Samsung 990 PRO 1 TB (PCIe Gen 4 NVMe M.2, `nvme1n1`, `ext4`, mounted `/mnt/data`) | ~$170 | Amazon.ca |
| **Storage – HDD** | Seagate BarraCuda 4 TB (SATA III, 3.5-inch, 5400 RPM, `/mnt/backup`) | ~$110 | Amazon.ca |
| **Case** | Corsair 7000D Airflow Full-Tower ATX (Black) | ~$325 | Best Buy |
| **Cooler** | ARCTIC Liquid Freezer III Pro 360 A-RGB (Black, front-mounted) | ~$236 | Amazon.ca |
| **PSU** | CORSAIR RM1000x (1000 W, Fully Modular, ATX 3.1, PCIe 5.1, Cybenetics Gold) | ~$265 | Amazon.ca |
| **UPS** | CyberPower CP1500AVRLCD3 (1500 VA / 900 W) | ~$262 | Amazon.ca |
| **Fans** | 3 × Noctua NF-A12x25 PWM (2 × front intake, 1 × rear exhaust) | ~$90 | Amazon.ca |
| **Cables** | CableMod 8 + 8 Series Classic ModFlex (Black, routed through 7000D channels) | ~$38 | Amazon.ca |
| **Boot Device** | SanDisk Ultra 16 GB (USB 3.2 Gen 1, for Ubuntu install and BIOS update) | ~$10 | Amazon.ca |
| **Optional** | StarTech 18-inch SATA III Data Cable | ~$6 | Amazon.ca |

---

### 🧪 Performance Observations
- **CPU Temps:** Idle 30–40 °C, Load 60–62 °C (ARCTIC Liquid Freezer III Pro 360)  
- **GPU Temps:** Idle 25 °C, Load 60–65 °C (ASUS TUF RTX 5080)  
- **Noise Level:** ~38 dB under AI training load  

---

### 🧭 Notes
- Total build cost: ≈ **$5 430 CAD** (all components tested Summer 2025).  
- SSD 1 hosts OS and environments; SSD 2 stores datasets and checkpoints; HDD used for archives / backups.  
- Installed the **secondary NVMe drive** in the chipset-connected M.2 slot to avoid reducing GPU bandwidth from x16 to x8. Verified via `lspci` (GPU operating at PCIe Gen 5 x16).  
- BIOS updated to version 0805 (X870E-E) to resolve Q-Code errors and enable full Ryzen 9 9950X support.  
- **Fit adjustment:** The M.2 heatsink cover on the ASUS X870E-E had to be manually removed for the Samsung 990 PRO to fit under the GPU shroud.  
- Build validated with CUDA 12.9 / PyTorch 2.5.1 and compatible with upcoming RTX 5090 driver updates.  

---

⚠️ **Disclaimer:** Modifying or disassembling components (e.g., removing heatsinks or covers) may void warranties.  
Refer to the [project disclaimer](../../DISCLAIMER.md) for full terms and liability limitations.