## How to install

The code was tested in the following environment:
- Ubuntu 22.04
- Python 3.12
- CUDA 13.0
- GPU: NVIDIA RTX 3060
- The code runs in a dedicated conda environment.


Installation steps:
- Clone the repo.
  ```
  git clone --recurse-submodules https://github.com/qX1B0UutNN/vipe-gsplat-demo.git
  ```

- Install dependencies from the requirements file.
  ```
  pip install -r requirements.txt
  ```

- Install VIPE and gsplat from submodules separately.
  ```
  python -m pip install -e ./ext/vipe
  python -m pip install -e ./ext/gsplat
  ```

  The custom forks fix small inconsistencies, such as missing subfolder structure, and add features such as exporting to PLY.


  Installing VIPE from GitHub allows using the `run.py` interface, which is not available from the pip installation.
