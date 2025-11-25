# Backend Project Structure

# This document outlines the structure of the backend project, detailing the purpose of each directory and key files within them.


```
backend/
├── main/
│   ├── __init__.py
│   ├── server.py                 # Entry point of the application
├── pipeline/
│   ├── __init__.py
│   ├── pipeline.py
│   ├── realtime_pipeline.py
│   ├── result_pipeline.py
│   ├── test_realtime.py
├── post_analysis/
│   ├── clean_up.py
├── prediction/
│   ├── __init__.py
│   ├── predict_folder.py      # The functionality for making predictions for a folder: json_tensor_list, tsm_model, expected_T=32, device=None, batch_size=16
├── preprocessing/
│   ├── __init__.py
│   ├── split_video.py  # Function to split video into smaller videos into temporatory folder
│   ├── tensor_conversion.py    # Function to convert folder of videos into folder of tensors
│   ├── tensor_conversion_experiment.py
├── realtime_handling/
│   ├── connect_phone_cam.py
│   ├── frame_to_vector.py
│   ├── prediction.py
├── resnet50/
│   ├── __init__.py
│   ├── load_resnet50.py        # Function to load resnet50 model
│   ├── resnet50_weights.pth
├── tsm/
│   ├── temporal-shift-module/
│           ├── .... # all things related to tsm cloned from Github
│   ├── __init__.py
│   ├── load_tsm.py        # Function to load TSM model
│   ├── tsm_class_definition.py # Definition of TSM class
│   ├── tsm_epoch_12.pt      # Pretrained TSM model weights
├── backend_structure.md
├── Dockerfile
├── requirements.txt
```

