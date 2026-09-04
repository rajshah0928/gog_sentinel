# Plate detector weights

`plate_yolov8n.pt` is `license-plate-finetune-v1n.pt` from the HuggingFace
repo [`morsetechlab/yolov11-license-plate-detection`](https://huggingface.co/morsetechlab/yolov11-license-plate-detection)
(nano variant, ~5.5MB, 640x640 input, single `License_Plate` class).

- Architecture: YOLOv11n (loads fine via `ultralytics.YOLO()`, same API as YOLOv8).
- Trained on a general/multi-country Roboflow "License Plate Recognition" dataset
  (not Indian-plate-specific) — validate/consider light fine-tuning on Gujarat
  CCTV samples if detection recall on Indian plates proves weak.
- License: **AGPL-3.0** (inherited from Ultralytics YOLO training). Note this in
  the HLD's licensing/tech-stack section — AGPL requires source disclosure if
  this service is offered over a network to third parties. Acceptable for a
  hackathon prototype; flag for legal review before any production deployment.

Re-download with:
```python
from huggingface_hub import hf_hub_download
path = hf_hub_download(
    repo_id="morsetechlab/yolov11-license-plate-detection",
    filename="license-plate-finetune-v1n.pt",
)
```
