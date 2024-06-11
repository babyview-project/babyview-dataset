cd mmpose
python tools/test.py ../benchmark_exps_configs/rtmo-l_16xb16-600e_babyview_coco-640x640.py https://download.openmmlab.com/mmpose/v1/projects/rtmo/rtmo-l_16xb16-600e_coco-640x640-516a421f_20231211.pth
python tools/test.py ../benchmark_exps_configs/rtmpose-l_8xb256-420e_aic-babyview-coco-384x288.py https://download.openmmlab.com/mmpose/v1/projects/rtmposev1/rtmpose-l_simcc-aic-coco_pt-aic-coco_420e-384x288-97d6cb0f_20230228.pth
python tools/test.py ../benchmark_exps_configs/simcc_res50_8xb32-140e_babyview_coco-384x288.py https://download.openmmlab.com/mmpose/v1/body_2d_keypoint/simcc/coco/simcc_res50_8xb32-140e_coco-384x288-45c3ba34_20220913.pth
python tools/test.py ../benchmark_exps_configs/yoloxpose_l_8xb32-300e_babyview_coco-640.py https://download.openmmlab.com/mmpose/v1/body_2d_keypoint/yolox_pose/yoloxpose_l_8xb32-300e_coco-640-de0f8dee_20230829.pth
python tools/test.py ../benchmark_exps_configs/td-hm_hrformer-base_8xb32-210e_babyview_coco-384x288.py https://download.openmmlab.com/mmpose/top_down/hrformer/hrformer_base_coco_384x288-ecf0758d_20220316.pth
python tools/test.py ../benchmark_exps_configs/td-hm_ViTPose-huge_8xb64-210e_babyview_coco-256x192.py https://download.openmmlab.com/mmpose/v1/body_2d_keypoint/topdown_heatmap/coco/td-hm_ViTPose-huge_3rdparty_coco-256x192-5b738c8e_20230314.pth
