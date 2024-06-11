from typing import List, Dict, Optional
from label_studio_ml.model import LabelStudioMLBase
from label_studio_ml.response import ModelResponse
from mmpose.apis import MMPoseInferencer
from urllib.parse import unquote
from PIL import Image, ImageOps
import numpy as np
import json

def get_image_size(filepath):
    img = Image.open(filepath)
    img = ImageOps.exif_transpose(img)
    return img.size


def convert(obj):
    if isinstance(obj, np.float32):
        return float(obj)
    elif isinstance(obj, list):
        return [convert(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert(value) for key, value in obj.items()}
    return obj

class NewModel(LabelStudioMLBase):
    """Custom ML Backend model
    """
    
    def setup(self):
        """Configure any parameters of your model here
        """
        self.set("model_version", "0.0.1")
        self.inferencer = MMPoseInferencer('human')
        # self.inferencer = MMPoseInferencer('rtmo-l_16xb16-600e_body7-640x640')

    def predict_one_task(self, task):
        labels = self.parsed_label_config['kp-1']['labels']
        label_to_id = {label: id for id, label in enumerate(labels)}
        id_to_label = {id: label for label, id in label_to_id.items()}
        img_path = unquote(task['data']['img']).replace('/data/local-files/?d=ccn2a/u', '/ccn2a/u')
        print(f"Image path:{img_path}")
        img_width, img_height = get_image_size(img_path)
        # instantiate the inferencer using the model alias
        # The MMPoseInferencer API employs a lazy inference approach,
        # creating a prediction generator when given input
        result_generator = self.inferencer(img_path, show=False)
        result = dict(next(result_generator))
        all_predictions = result['predictions'][0]

        all_results = []
        all_scores = []
        for prediction in all_predictions:
            # dict_keys(['keypoints', 'keypoint_scores', 'bbox', 'bbox_score'])
            keypoints = prediction['keypoints']
            keypoint_scores = prediction['keypoint_scores']
            mean_keypoint_score = np.mean(keypoint_scores)
            bbox = list(prediction['bbox'])[0]
            bbox_score = prediction['bbox_score']
            bbox_label = "person-bbox"
            box_x, box_y, box_xmax, box_ymax = bbox
            mean_score = (mean_keypoint_score + bbox_score) / 2

            
            for point_id in range(len(keypoints)):
                keypoint = keypoints[point_id]
                x,y = keypoint
                keypoint_label_name = id_to_label[point_id]
                kp_score = keypoint_scores[point_id]
                # set the keypoint to 0,0 if the score is less than 0.5
                if kp_score < 0.5:
                    x = 0
                    y = 0
                else:
                    x = float(x) / img_width * 100
                    y = float(y) / img_height * 100
                keypoint_label_dict = {
                    # "id": point_id,
                    "from_name": "kp-1",
                    "to_name": "img-1",
                    "type": "keypointlabels",
                    "origin":"manual",
                    "original_width":img_width,
                    "original_height":img_height,
                    "image_rotation":0,
                    "value": {
                            "x": x,
                            "y": y,
                            "width": 0.1707941929974381,
                            "keypointlabels":[
                                keypoint_label_name
                            ],
                    "score": keypoint_scores[point_id],
                    },
                }
                all_results.append(keypoint_label_dict)

            box_width = (float(box_xmax) - float(box_x)) / img_width * 100
            box_height = (float(box_ymax) - float(box_y)) / img_height * 100

            box_x = float(box_x) / img_width * 100
            box_y = float(box_y) / img_height * 100

            if box_x == 0 and box_y == 0:
                box_width = 0
                box_height = 0
            
            box_dict = {
                # "id": "0",
                "from_name": "label",
                "to_name": "img-1",
                "type": "rectanglelabels",
                "origin":"manual",
                "original_width":img_width,
                "original_height":img_height,
                "image_rotation":0,
                "value": {
                    "rectanglelabels": [bbox_label],
                    "x": box_x,
                    "y": box_y,
                    "width": box_width,
                    "height": box_height,
                    "rotation":0,
                },
                "score": bbox_score,
            }
            all_results.append(box_dict)
            all_scores.append(mean_score)
        all_results = convert(all_results)
        score = float(np.mean(all_scores))
        return {
            "model_version": self.get("model_version"),
            "score": score,
            "result": all_results
        }


    def predict(self, tasks: List[Dict], context: Optional[Dict] = None, **kwargs) -> ModelResponse:
        """ Write your inference logic here
            :param tasks: [Label Studio tasks in JSON format](https://labelstud.io/guide/task_format.html)
            :param context: [Label Studio context in JSON format](https://labelstud.io/guide/ml_create#Implement-prediction-logic)
            :return model_response
                ModelResponse(predictions=predictions) with
                predictions: [Predictions array in JSON format](https://labelstud.io/guide/export.html#Label-Studio-JSON-format-of-annotated-tasks)
        """
        predictions = []
        print(f"Numbers of task:{len(tasks)}")
        for task in tasks:
            predictions.append(self.predict_one_task(task))
        return ModelResponse(predictions=predictions)


    def fit(self, event, data, **kwargs):
        """
        This method is called each time an annotation is created or updated
        You can run your logic here to update the model and persist it to the cache
        It is not recommended to perform long-running operations here, as it will block the main thread
        Instead, consider running a separate process or a thread (like RQ worker) to perform the training
        :param event: event type can be ('ANNOTATION_CREATED', 'ANNOTATION_UPDATED', 'START_TRAINING')
        :param data: the payload received from the event (check [Webhook event reference](https://labelstud.io/guide/webhook_reference.html))
        """

        # use cache to retrieve the data from the previous fit() runs
        old_data = self.get('my_data')
        old_model_version = self.get('model_version')
        print(f'Old data: {old_data}')
        print(f'Old model version: {old_model_version}')

        # store new data to the cache
        self.set('my_data', 'my_new_data_value')
        self.set('model_version', 'my_new_model_version')
        print(f'New data: {self.get("my_data")}')
        print(f'New model version: {self.get("model_version")}')

        print('fit() completed successfully.')

