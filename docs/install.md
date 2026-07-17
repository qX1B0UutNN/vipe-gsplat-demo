## How to install

Code was tested in such environment:
- ubuntu 22.04
- python 3.12
- cuda version 13.0
- gpu - nvidia rtx 3060
- code is running in dedicated conda env.

Installation steps:
- Clone repo
  ```
  git clone --recurse-submodules https://github.com/qX1B0UutNN/vipe-gsplat-demo.git
  ```

- Install dependencies from requirement file.
  ```
  pip install -r requirements.txt
  ```

- Install vipe and gspalt from submodules separately
  ```
  python -m pip install -e ./ext/vipe
  python -m pip install -e ./ext/gsplat
  ```
