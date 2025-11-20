import time
from pipeline.result_frontend import convert_scene_results
from prediction.predict_folder import predict_folder
from preprocessing.split_video import split_video
from preprocessing.tensor_conversion import folder_to_tensor
from resnet50.load_resnet50 import load_resnet50_model
from tsm import load_tsm
from post_analysis.clean_up import delete_resource

resnet50_model = load_resnet50_model(device=None)
tsm_model = load_tsm.load_TSM(pt_path="tsm/tsm_feature_epoch_12.pt", feature_dim=2048, num_classes=2, n_segment=4)

def pipeline(video_path):
  start = time.time()
  output_dir = split_video(video_path, duration=1)
  print("[TIME] Split:", time.time() - start)

  start = time.time()
  json_tensor = folder_to_tensor(output_dir, resnet50_model, T=1, device=None)
  print("[TIME] Tensor conversion:", time.time() - start)

  start = time.time()
  json_prediction = predict_folder(json_tensor, tsm_model)
  print("[TIME] Prediction:", time.time() - start)

  json_front_end = convert_scene_results(json_prediction)
  delete_resource(video_path)
  return json_front_end