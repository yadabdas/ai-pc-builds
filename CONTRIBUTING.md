# 🤝 Contributing to AI PC Build Guide

Thank you for your interest in contributing to the **AI PC Build Guide**!  
This repository is a collaborative effort to help developers build and configure PCs for AI workloads at home.  
By sharing builds, software setups, and benchmarks, contributors help others experiment with AI efficiently and cost-effectively.

Before contributing, please read the [README](./README.md) for an overview of the project and the [DISCLAIMER](./DISCLAIMER.md) for important notices on hardware risks and software usage.

---

## 🎯 Ways to Contribute

- **Submit a Build** – Share your AI PC setup, including hardware, software, issues faced, and benchmarks.  
- **Improve Documentation** – Enhance guides in the `docs/` directory (e.g., hardware recommendations, troubleshooting).  
- **Share Scripts** – Contribute setup or benchmarking scripts to `scripts/`.  
- **Report Issues** – Open GitHub Issues for bugs, suggestions, or questions.  
- **Join Discussions** – Participate in [GitHub Discussions](https://github.com/yadabdas/ai-pc-builds/discussions) to share ideas or feedback.

---

## 🧩 Contribution Steps

To ensure consistency and quality across contributions, please follow these steps.

### 1. Submitting a Build

1. **Fork the Repository**
   ```bash
   git clone https://github.com/your-username/ai-pc-builds.git
   cd ai-pc-builds
   ```

2. **Create a Build Directory**
   ```bash
   cp -r builds/template builds/build_<yourname>_<year>
   ```

3. **Include Required Files**
   - `hardware.md` – List components (CPU, GPU, RAM, storage) with specs and optional cost/source links.  
   - `software.md` – Describe OS, environments, and frameworks (e.g., Ubuntu 24.04, PyTorch 2.5.1, CUDA 12.9).  
   - `issues.md` – Log issues and resolutions (e.g., driver conflicts, BIOS settings).  
   - `benchmarks.md` – Include one reproducible metric (e.g., training loss, inference speed).  
   - *(Optional)* `scripts/` – For setup, profiling, or benchmarking automation.

4. **Test Your Build**
   - Verify functionality:  
     ```bash
     nvidia-smi
     python -c "import torch; print(torch.cuda.is_available())"
     ```  
   - Check scripts with `shellcheck` (bash) or `flake8` (Python).  
   - Ensure benchmarks are reproducible and include sample data if relevant.

5. **Commit and Push**
   ```bash
   git checkout -b build_<yourname>_<year>
   git add builds/build_<yourname>_<year>/
   git commit -m "Add build_<yourname>_<year> (RTX 5080 + PyTorch setup)"
   git push origin build_<yourname>_<year>
   ```

6. **Submit a Pull Request**
   - Open a PR to `yadabdas/ai-pc-builds` and summarize: hardware, workload, key metrics.  
   - Link related Issues or Discussions.  
   - Ensure required files match the `builds/template/` format.

---

### 2. Improving Documentation
- Update files in `docs/` (e.g., `hardware_guide.md`, `troubleshooting.md`) with new insights or fixes.  
- Example:
  ```markdown
  ### NVIDIA Driver Not Detecting GPU
  Run `sudo apt purge nvidia-*` then `sudo ubuntu-drivers autoinstall`
  ```

---

### 3. Contributing Scripts
- Add to `scripts/setup_scripts/` or `scripts/benchmark_scripts/`.  
- Include usage notes, dependencies, and inline comments.  
- Example:
  ```bash
  # scripts/setup_scripts/install_cuda.sh
  wget https://developer.download.nvidia.com/compute/cuda/12.9.0/local_installers/cuda_12.9.0_535.104.05_linux.run
  sudo sh cuda_12.9.0_535.104.05_linux.run
  ```

---

### 4. 🧹 Formatting & Style
- Use Markdown for documentation.  
- Prefer tables for specs and lists for steps.  
- Use fenced code blocks (```) for commands and examples.  
- Keep lines under ~100 characters for readability.

---

## ✅ Submission Checklist

Before submitting your PR, ensure:
- [ ] Your build directory follows the `builds/template/` structure.  
- [ ] All required files (`hardware.md`, `software.md`, etc.) are included.  
- [ ] Benchmarks are reproducible and documented.  
- [ ] Scripts are tested and include usage comments.  
- [ ] Commands and paths are correct.  
- [ ] PR description summarizes your contribution and links related discussions.  
- [ ] You’ve reviewed the [Disclaimer](./DISCLAIMER.md).

---

## 🛠️ Review Process

1. **Initial Review:** Maintainers check for completeness and formatting.  
2. **Feedback:** You’ll receive comments within 3–5 days.  
3. **Testing:** Builds or scripts may be tested for reproducibility.  
4. **Merge:** Once approved, your PR will be merged into the main branch.

---

## 💡 Tips for Great Contributions

- **Be Specific:** List exact models and software versions.  
- **Document Thoroughly:** Include troubleshooting and reasoning.  
- **Use Visuals:** Add build photos or diagrams.  
- **Standardize Benchmarks:** Use common workloads for comparison.  
- **Test Locally:** Verify all steps before submission.

---

## 📬 Getting Help
- Open a GitHub Issue for questions.  
- Join [Discussions](https://github.com/yadabdas/ai-pc-builds/discussions) to share feedback.  
- Tag maintainers for review or clarification.

---

## 🌱 Code of Conduct
- Be respectful, inclusive, and constructive.  
- Avoid personal attacks; focus on technical issues.  
- Follow the [MIT License](./LICENSE) and all third-party software terms.

---

## 🙌 Acknowledgments
Every contribution helps make AI experimentation more accessible.  
By sharing your build, you’re helping developers worldwide explore, learn, and innovate.  
Thank you for being part of this community!