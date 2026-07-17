## Expected Folder structure
```
.
├── data
│   ├── zavod70
│   │   └── Original frame sequence
│   │  
│   ├── zavod70-x4-downscale
│   │   └── Frame sequence downscaled by x4 factor
│   │  
│   └── zavod70-x4-downscale.mp4
│       └── Frame sequnce converted into .mp4
│  
├── docs
│   ├── how-to-run.md
│   ├── folder-structure.md
│   └── install.md
│  
├── ext
│   ├── gsplat
│   │   └── Gsplat repo
│   │  
│   └── vipe
│       └── Vipe repo
│  
├── results
│   ├── v1
│   ├── ...
│   └── v3
│       ├── gsplat
│       │   └── Gspalt outputs for run v3.
│       │  
│       └── vipe
│           ├── colmap_format
│           │   └── Vipe output converted into COLMAP format.
│           │  
│           └── Vipe outputs for run v3
│  
├── scripts
│   ├── Custom scripts folder.
│   │  
│   ├── downscale_images.py
│   └── frames_to_video.py
│  
├── readme.md
└── requirements.txt
```
