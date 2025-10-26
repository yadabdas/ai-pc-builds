# 💻 Software – Build <yourname>, <year>

Document your software environment setup and any tools you used.

## 🖥️ OS & Installation
- Distro: `<ex: Ubuntu 24.04 LTS Desktop>`
- Install Target: `<ex: /dev/nvme0n1>`
- Verification:
  ```bash
  lsb_release -a
  ```

## 🧩 Conda Environments
Example format:

### `cuda_env`
- Purpose: `<ex: PyTorch + CUDA work>`
- Setup:
  ```bash
  conda create -n cuda_env python=3.11 jupyter pandas numpy -c conda-forge
  conda activate cuda_env
  conda install pytorch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 pytorch-cuda=12.4 -c pytorch -c nvidia
  ```
- Verification:
  ```bash
  python -c "import torch; print(torch.cuda.is_available())"
  ```

### `tf_env`
- Purpose: TensorFlow work  
- Notes: Keep separate to avoid CUDA conflicts

## 🧰 Tools
List key developer tools:
- VS Code, IntelliJ, Nsight, Git, Maven, etc.

## ⚡ Quick GPU Test
```bash
python -c "import torch, time; x=torch.rand((4096,4096),device='cuda'); t=time.time(); _=torch.mm(x,x); print('Time:', time.time()-t)"
```

⚠️ **Disclaimer:** Installing drivers or disabling Secure Boot can affect system stability. See the [project disclaimer](../../DISCLAIMER.md).
