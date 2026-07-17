## How to run

- Check expected folder structure and ensure input date located correctly.

- Downscale input frame size by x4.
  It prevent out of mem error on a local gpu.
  ```bash
  python scripts/downscale_images.py -s 4 ./data/zavod70/ ./data/zavod70-x4-downscale
  ```
- Convert frame sequnce to video file.
  So we will be sure in a correct order of frames.
  ```bash
python scripts/frames_to_video.py data/zavod70-x4-downscale/ data/zavod70-x4-downscale.mp4
  ```

- Create folder for output files.
  `RUN_VER` make it easier to track changes between different attempts.
  ```bash
export RUN_VER=v1
mkdir -p "results/$RUN_VER"
  ```

- Run vipe reconstruction.
  ```bash
CUBLAS_WORKSPACE_CONFIG=:4096:8 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True python ext/vipe/run.py \
    pipeline=no_vda \
    streams=raw_mp4_stream \
    streams.base_path=data/zavod70-x4-downscale.mp4 \
    "pipeline.output.path=results/$RUN_VER/vipe/" \
    pipeline.output.save_slam_map=true \
    pipeline.output.save_artifacts=true \
    pipeline.output.save_viz=false
  ```

- Convert vipe output into COLMAP format that is suitable with gsplat.
  ```bash
python ext/vipe/scripts/vipe_to_colmap.py \
    "results/$RUN_VER/vipe/" \
    --output "results/$RUN_VER/vipe/colmap_format/" \
    --use_slam_map
  ```

  Optionaly check vipe output by build-in visualizer.
  ```bash
vipe visualize ./vipe_results/ --port 8080
  ```

  Or convert into point cloud and check localy in point cloud viewer.
  ```bash
colmap model_converter --input_path ./sparse/0/ --output_path point_clouds.ply --output_type PLY
  ```

- Generate gaussian splatting with gsplat
  ```bash
CUDA_VISIBLE_DEVICES=0 python ext/gsplat/examples/simple_trainer.py \
    default \
    --data_dir "results/$RUN_VER/vipe/colmap_format/zavod70-x4-downscale" \
    --data_factor 1 \
    --result_dir "results/$RUN_VER/gsplat/" \
    --strategy.refine-stop-iter 12000 \
    --strategy.grow-grad2d 0.0012 \
    --packed \
    --max_steps 30000 \
    --strategy.absgrad \
    --antialiased \
    --strategy.prune_opa 0.08
  ```

- Render gaussian splatting flythrough along initial camera trajectory with same training script.
  ```bash
CUDA_VISIBLE_DEVICES=0 python ext/gsplat/examples/simple_trainer.py \
    default \
    --data_dir "results/$RUN_VER/vipe/colmap_format/zavod70-x4-downscale" \
    --data_factor 1 \
    --ckpt "results/$RUN_VER/gsplat/ckpts/ckpt_29999_rank0.pt" \
    --render_traj_path interp
  ```

- Check result in gsplat viewer.
  ```bash
python ext/gsplat/examples/simple_viewer.py \
    --ckpt "results/$RUN_VER/gsplat/ckpts/ckpt_29999_rank0.pt"
  ```

