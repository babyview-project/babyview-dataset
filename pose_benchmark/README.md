# Repository Notice
Due to data sensitivity, all data and annotations have been removed. Contact us for access.

# Labeling Pipeline
1. Install and setup [Label Studio](https://github.com/HumanSignal/label-studio)

2. Setup the Labeling Interface using this template code:

   ```xml
   <View>
     <KeyPointLabels name="kp-1" toName="img-1">
         
     <Label value="0-nose" background="#FFA39E"/><Label value="1-lefteye" background="#D4380D"/><Label value="2-righteye" background="#FFC069"/><Label value="3-leftear" background="#AD8B00"/><Label value="4-rightear" background="#D3F261"/><Label value="5-leftshoulder" background="#389E0D"/><Label value="6-rightshoulder" background="#5CDBD3"/><Label value="7-leftelbow" background="#096DD9"/><Label value="8-rightelbow" background="#ADC6FF"/><Label value="9-leftwrist" background="#F759AB"/><Label value="10-rightwrist" background="#FFA39E"/><Label value="11-lefthip" background="#D4380D"/><Label value="12-righthip" background="#FFC069"/><Label value="13-leftknee" background="#AD8B00"/><Label value="14-rightknee" background="#D3F261"/><Label value="15-leftankle" background="#389E0D"/><Label value="16-rightankle" background="#5CDBD3"/></KeyPointLabels>
     <PolygonLabels name="polygonlabel" toName="img-1">
         <Label value="person-seg" background="#0DA39E"/>
     </PolygonLabels>
     <RectangleLabels name="label" toName="img-1">
         <Label value="person-bbox" background="#DDA0EE"/>
     </RectangleLabels>
     <Image name="img-1" value="$img"/>
   </View>
   ```

3. Depoly AI Annotation Backend

   1. Install mmpose

      https://mmpose.readthedocs.io/en/latest/installation.html

   2. Start Pose backend

      `label-studio-ml start ./my_pose_ml_backend/`

# Pose Detection Test

1. Prepare Dataset and Annotation(contact us to get access and configuration)

2. Run test example

   ````bash
   python tools/test.py ../benchmark_exps_configs/rtmo-l_16xb16-600e_babyview_coco-640x640.py https://download.openmmlab.com/mmpose/v1/projects/rtmo/rtmo-l_16xb16-600e_coco-640x640-516a421f_20231211.pth
   ````

   

