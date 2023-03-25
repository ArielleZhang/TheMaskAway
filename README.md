# Triple-Dots
ECE324 Course Project

### Datasets and Preprocessing ###
We used the MaksTheFace: https://github.com/aqeelanwar/MaskTheFace to generate the masks. TFill is taking two inputs: the original image and the mask only. We modified the ```mask_the_face.py``` file to generate and save the mask. We also wrote our own script to preprocess the data options are set ```--convert``` to convert all images to either jpg format, set ```--resize``` to resize the images, and set ```--compare_dir``` compared the input dir and masks dir and remove all the images in the input image dir wich does not have a corresponding mask.

We preprocessed three different datasets:
1. Faces Kaggle dataset: https://www.kaggle.com/datasets/varump66/face-images-13233, with 256 by 256 resolution but only the last 8k examples (roughly).
2. FFHQ Kaggle dataset: https://www.kaggle.com/datasets/arnaud58/flickrfaceshq-dataset-ffhq, with 512 by 512 resolution but only the first 10k examples (roughly).
3. A small personalized dataset containing 100 images (roughly) of Arielle.
4. And a small test dataset for quick test purposes, only 5 images.
Notice that every dataset contains original images and the corresponding masks.

### Training Models ###

#### MAT #### 
to be added later

#### TFill ####
To train on Nvidia RTX3060 GPU, we had to modify their ```environment.yaml``` file to make the ```cudatoolkit``` version match with the Nvidia dirver, as well as some of the configurations in ```base_options.py```. We also modified the ```data_loader.py``` to train on our own mask instead of their generated mask. We trainined/are still trainig three models now.

_Model 1_: ```M1_faces_from_scratch``` on the Faces Kaggle dataset, this one is -depricated-, because the dataset does not have a high quality as FFHQ.
_Model 2_: ```M2_FFHQ_from_scratch``` on FFHQ with our own masks, training model from scratch. We so far ran 60000 iterations but TFill ffhq model ran for 2000000 iterations, so to get a better performance, we need to train for longer.
_Model 3_: ```M3_FFHQ_pretrained``` on FFHQ with our own masks, training model on top of their pretrained ffhq model which is trained on ffhq___ for 20000000 iterations. We so far ran ___ iterations.
!!!!!!!NOTICE: MODEL3 IS STILL NOT DONE YET, WILL UPDATE TMR!!!!!!!

Saved models and training outcomes are in the checkpoints folder, testing results in the testing folder.

### Future Steps ###
Once we get the models and testing results, these parts will be added to the Training Models Section.

Fine tune for the user (more customized), pick a best pretrained model then train and fine tune it using user input datasets (ex. Arielle 100 datasets) to make sure the face generated looks similar to the person.

