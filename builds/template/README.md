# 🧠 Build Template

This directory documents an example AI workstation build.  
If you're contributing your own build, copy this entire `template/` folder to `builds/build_<yourname>_<year>/` and fill in each file.

## 👤 Build Owner
- Name / handle: `<your name or alias>`
- Location (optional): `<city / region>`
- Date built: `<Season Year>` (e.g. "Summer 2025")

## 💡 Intended Use
Describe what this machine is for. Examples:
- Local LLM fine-tuning
- Stable Diffusion / image generation
- CUDA programming / kernel profiling
- Asset valuation / tabular regression
- Robotics / perception models
- General ML experimentation

> This helps others pick a build that matches their needs.

## 📂 Contents
- [`hardware.md`](./hardware.md): Parts list (CPU, GPU, RAM, storage, PSU, case, etc.)  
- [`software.md`](./software.md): OS, drivers, Conda envs, versions, and tools  
- [`issues.md`](./issues.md): Problems you hit and how you fixed them  
- [`benchmarks.md`](./benchmarks.md): Training / inference / profiling results  
- [`scripts/`](./scripts): Optional helper scripts (install, train, profile, etc.)

⚠️ See the project-wide [DISCLAIMER](../../DISCLAIMER.md) before reproducing any build.
