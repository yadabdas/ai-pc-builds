# Ubuntu 24.04: Kernel 7.0 + NVIDIA 595 Open Driver Upgrade

**Date:** 2026-10-31  
**Machine:** `Custom` — local AI workstation  
**Outcome:** Successful upgrade and GPU compute verification  
**Scope:** Kernel and NVIDIA driver; CUDA Toolkit and Conda environments retained

## 1. System and motivation

| Component | Before | After |
|---|---|---|
| OS | Ubuntu 24.04 | Ubuntu 24.04 |
| Kernel | `6.14.0-37-generic` | `7.0.0-42-generic` |
| NVIDIA driver | `575.51.03-open` (DKMS) | `595.99.02-open` (Ubuntu precompiled module) |
| GPU | GeForce RTX 5080 (Blackwell, 16 GB) | Same |
| CUDA Toolkit (`nvcc`) | 12.9 | 12.9.41 (unchanged) |
| Python environments | Conda environments including `genai-math-lab` | Preserved |

Other hardware: Ryzen 9 9950X, ASUS ROG Strix X870E-E, 128 GB RAM. Root filesystem is ext4 on NVMe; `/boot` is on the root filesystem and `/boot/efi` is a separate EFI partition. Secure Boot was disabled.

The objective was to upgrade the kernel and NVIDIA driver without reinstalling Ubuntu, breaking CUDA tooling, or disturbing local development environments.

## 2. Previous failed attempt: kernel 6.17

An earlier attempt to install `6.17.0-35-generic` encountered two separate issues:

1. **Boot failure:** `VFS: Unable to mount root fs on unknown-block(0,0)` after an interrupted installation left the kernel without a usable initramfs. The initramfs and GRUB configuration were repaired to recover bootability.
2. **NVIDIA DKMS failure:** The existing NVIDIA 575 open driver did not compile successfully for kernel 6.17. The reported errors included missing NVIDIA internal headers such as `os-interface.h`, `nv-firmware.h`, and `nv-platform.h`.

The 6.17 kernel was subsequently removed, and the machine returned to its working 6.14 configuration.

**Lessons:** Do not assume a new kernel is bootable merely because its image package is installed. Verify its initramfs, GRUB entry, and matching NVIDIA module *before* rebooting. Also, avoid relying on an unverified DKMS build for a new kernel.

## 3. Package selection and dry-run investigation

Initial simulations for kernel `6.17.0-35-generic` with precompiled NVIDIA modules failed because the kernel-specific module packages had incompatible constraints on the NVIDIA kernel-common package:

- NVIDIA 595 module for 6.17 required `nvidia-kernel-common-595 <= 595.71.05-1`, while the available driver candidate was `595.99.02`.
- NVIDIA 580 module for 6.17 similarly required an older kernel-common version than the available `580.178.04` candidate.

The compatible Ubuntu 24.04 HWE combination was:

- `linux-generic-hwe-24.04` → kernel `7.0.0-42-generic`
- `linux-modules-nvidia-595-open-generic-hwe-24.04` → precompiled NVIDIA 595 module for that kernel
- `nvidia-driver-595-open` → NVIDIA driver `595.99.02`

The successful simulation was:

```bash
apt-get -s install \
  linux-generic-hwe-24.04 \
  linux-modules-nvidia-595-open-generic-hwe-24.04 \
  nvidia-driver-595-open
```

The plan added 30 packages and removed 16 older NVIDIA 575 packages, without removing the existing kernel 6.14 or CUDA Toolkit 12.9. The NVIDIA 575 DKMS package would be removed; no NVIDIA 595 DKMS package was needed for kernel 7.0 because the matching module was precompiled.

A concurrent `unattended-upgrades` run held the package-manager lock and was allowed to finish rather than being killed.

## 4. First real installation: package file conflict

Executed:

```bash
sudo apt install \
  linux-generic-hwe-24.04 \
  linux-modules-nvidia-595-open-generic-hwe-24.04 \
  nvidia-driver-595-open
```

APT downloaded approximately 567 MB and removed the old NVIDIA 575 packages. It unpacked the kernel 7.0 and precompiled NVIDIA 595 kernel-module packages, but failed while unpacking `libnvidia-gl-595`:

```text
dpkg: error processing archive ...libnvidia-gl-595_595.99.02...deb (--unpack):
 trying to overwrite '/usr/share/egl/egl_external_platform.d/20_nvidia_xcb.json',
 which is also in package libnvidia-egl-xcb1:amd64 1.0.0-0ubuntu1
E: Sub-process /usr/bin/dpkg returned an error code (1)
```

**Diagnosis:** An older installed NVIDIA EGL platform package owned a file now supplied by `libnvidia-gl-595`. This was a **package file-ownership conflict**, not a kernel/NVIDIA module build failure.

At this stage the package database contained partially unpacked/unconfigured packages. **Rebooting was deliberately avoided.**

## 5. Why the first repair attempt failed

We inspected the installed packages and reverse dependencies:

```bash
dpkg -l libnvidia-egl-xcb1 libnvidia-egl-xlib1 libnvidia-gl-595
apt-cache rdepends --installed libnvidia-egl-xcb1
apt-cache rdepends --installed libnvidia-egl-xlib1
```

Both `libnvidia-egl-xcb1` and `libnvidia-egl-xlib1` were installed at `1.0.0-0ubuntu1`; no installed reverse dependencies were reported. `libnvidia-gl-595` was not successfully installed.

A plain simulated removal failed because `nvidia-driver-595-open` already had an unmet dependency on `libnvidia-gl-595`. We then simulated a combined repair:

```bash
sudo apt-get -s --fix-broken install \
  libnvidia-egl-xcb1- \
  libnvidia-egl-xlib1- \
  libnvidia-gl-595
```

The simulation looked correct: remove two older EGL packages, install `libnvidia-gl-595`, configure 29 pending packages. However, running the real command still failed with the same file-overwrite error.

**Root cause of the repeated failure:** The real `dpkg` transaction tried to **unpack the new GL package before removing the two old EGL packages**. APT's final proposed package set was correct, but its execution order did not resolve the overlapping file ownership.

## 6. Successful recovery: remove first, repair second

We removed the two conflicting packages directly, without force flags:

```bash
sudo dpkg --remove libnvidia-egl-xcb1 libnvidia-egl-xlib1
```

This succeeded. We then finished the interrupted installation:

```bash
sudo apt-get --fix-broken install
```

This time `libnvidia-gl-595` unpacked and configured successfully, followed by the remaining kernel and NVIDIA packages.

Key successful log entries:

```text
Setting up nvidia-driver-595-open (595.99.02-0ubuntu0.24.04.1) ...
Setting up linux-modules-nvidia-595-open-7.0.0-42-generic ...
Setting up linux-image-7.0.0-42-generic ...
update-initramfs: Generating /boot/initrd.img-7.0.0-42-generic
Generating grub configuration file ...
Found linux image: /boot/vmlinuz-7.0.0-42-generic
Found initrd image: /boot/initrd.img-7.0.0-42-generic
Found linux image: /boot/vmlinuz-6.14.0-37-generic
Found initrd image: /boot/initrd.img-6.14.0-37-generic
```

The DKMS post-install hooks reported completion; this does **not** imply that NVIDIA 595 was built using DKMS. The selected NVIDIA 595 module was supplied as a precompiled Ubuntu kernel module.

**Caution:** This exact removal procedure applies to the observed package conflict and dependency graph. On another machine, inspect installed reverse dependencies and the proposed transaction before removing packages.

## 7. Pre-reboot verification

Commands:

```bash
sudo dpkg --audit
sudo apt-get check

ls -lh \
  /boot/vmlinuz-7.0.0-42-generic \
  /boot/initrd.img-7.0.0-42-generic \
  /boot/vmlinuz-6.14.0-37-generic \
  /boot/initrd.img-6.14.0-37-generic

modinfo -k 7.0.0-42-generic nvidia | \
  grep -E 'filename:|version:|vermagic:'

dkms status

lsinitramfs /boot/initrd.img-7.0.0-42-generic | \
  grep -E 'nvme|ext4|nvidia' | head -40
```

Observed:

- `dpkg --audit`: no output (clean).
- `apt-get check`: completed without dependency errors.
- Kernel 7.0 image: **17 MB**.
- Kernel 7.0 initramfs: **76 MB**.
- Kernel 6.14 image/initramfs remained available: **15 MB / 75 MB**.
- `modinfo` found `/lib/modules/7.0.0-42-generic/kernel/nvidia-595-open/nvidia.ko`, version `595.99.02`, with `vermagic` matching `7.0.0-42-generic`.
- `lsinitramfs` showed NVMe kernel modules (`nvme.ko.zst`, `nvme-core.ko.zst`) and ext4 filesystem-checking utilities. Absence of a separate `ext4.ko` line in the filtered output alone does not imply ext4 support is missing; it may be built into the kernel.
- `dkms status` produced no entries in the observed output.

After these checks, the machine was rebooted.

## 8. Post-reboot verification: success

```bash
uname -r
nvidia-smi
nvcc --version
```

Results:

```text
7.0.0-42-generic
NVIDIA-SMI 595.99.02   Driver Version: 595.99.02   CUDA Version: 13.2
GPU: NVIDIA GeForce RTX 5080
nvcc: Cuda compilation tools, release 12.9, V12.9.41
```

The GPU was detected, the NVIDIA kernel driver loaded, and the desktop Xorg process appeared in `nvidia-smi`.

**CUDA version distinction:** `nvidia-smi`'s **13.2** is the CUDA driver capability advertised by the installed driver, not the installed CUDA Toolkit version. `nvcc` confirmed that the locally installed Toolkit remained **12.9**.

### Actual GPU compute test

```bash
conda activate genai-math-lab

python - <<'PY'
import torch

print('PyTorch:', torch.__version__)
print('PyTorch CUDA:', torch.version.cuda)
print('CUDA available:', torch.cuda.is_available())

if torch.cuda.is_available():
    print('GPU:', torch.cuda.get_device_name(0))
    x = torch.randn(2048, 2048, device='cuda')
    y = x @ x
    torch.cuda.synchronize()
    print('GPU matrix multiplication:', y.shape, 'SUCCESS')
PY
```

Observed:

```text
PyTorch: 2.8.0.dev20250528+cu128
PyTorch CUDA: 12.8
CUDA available: True
GPU: NVIDIA GeForce RTX 5080
GPU matrix multiplication: torch.Size([2048, 2048]) SUCCESS
```

The PyTorch build uses CUDA 12.8, the installed Toolkit is 12.9, and the NVIDIA driver advertises CUDA 13.2 support. The successful matrix multiplication demonstrates that this particular PyTorch environment can execute GPU workloads with the new kernel and driver.

## 9. Precautions and remaining work

- **Do not run `apt autoremove` blindly.** APT listed `libarrow2000` and `libparquet2000` as automatically removable, along with other packages. These may be needed by local data-processing workflows.
- Keep `6.14.0-37-generic` installed temporarily as a kernel recovery option. **Caveat:** the old NVIDIA 575 DKMS module was removed, so booting 6.14 does not guarantee working NVIDIA graphics/compute.
- The APT output reported **244 packages not upgraded**. Review those separately; they were outside the scope of this change.
- Only `genai-math-lab` was explicitly GPU-tested in this record. Other Conda environments, PyCUDA, Numba, ONNX Runtime, and custom CUDA extensions should be tested independently as needed.
- No evidence in these logs indicates that the CUDA Toolkit or Conda environments were modified by the kernel/driver transaction.

## 10. Reusable checklist for future kernel + NVIDIA upgrades

1. Record baseline: `uname -r`, `nvidia-smi`, `nvcc --version`, `dkms status`, `dpkg --audit`, and `df -h /boot /boot/efi`.
2. Check available matching kernel and NVIDIA **precompiled** module packages; inspect version constraints.
3. Run `apt-get -s install ...` and review **every removal** before approving.
4. Wait for unattended upgrades or other package-manager activity to finish; do not forcibly remove locks.
5. Install and **do not reboot if APT/dpkg reports an error**.
6. If a package file conflict occurs, identify the owner with `dpkg -S <path>`, inspect reverse dependencies, and remove conflicting obsolete packages only when safe; avoid `--force-overwrite` as a first response.
7. Finish pending configuration and validate `dpkg --audit` and `apt-get check`.
8. Verify kernel image, **nonempty initramfs**, matching NVIDIA module (`modinfo -k <kernel> nvidia`), and GRUB entries before reboot.
9. After reboot, verify `uname -r`, `nvidia-smi`, and `nvcc --version`.
10. Run a real GPU workload in each important environment; preserve the old kernel until the new setup is proven stable.

---

**Final result:** Ubuntu 24.04 booted successfully on `7.0.0-42-generic` with NVIDIA `595.99.02-open`. The RTX 5080 was recognized and PyTorch CUDA matrix multiplication succeeded. The CUDA Toolkit remained at 12.9.
