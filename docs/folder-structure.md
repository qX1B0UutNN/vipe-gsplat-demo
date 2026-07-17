## Expected Folder Structure
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
│       └── Frame sequence converted into .mp4
│  
├── docs
│   ├── how-to-run.md
│   ├── folder-structure.md
│   ├── results.md
│   └── install.md
│  
├── ext
│   ├── gsplat
│   │   └── gsplat repo
│   │  
│   └── vipe
│       └── VIPE repo
│  
├── results
│   ├── v1
│   ├── ...
│   └── v3
│       ├── gsplat
│       │   └── gsplat outputs for run v3.
│       │  
│       └── vipe
│           ├── colmap_format
│           │   └── VIPE output converted into COLMAP format.
│           │  
│           └── VIPE outputs for run v3
│  
├── scripts
│   ├── Custom scripts folder.
│   │  
│   ├── downscale_images.py
│   └── frames_to_video.py
│  
├── README.md
└── requirements.txt
```
