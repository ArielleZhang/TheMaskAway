# Triple-Dots
ECE324 Course Project

### Set up ###
We used MaskTheFace, MAT, TFill repos, we attached the link to their repo when they are later referenced, all the modified and added scripts are uploaded here in our repo to set up you need to clone their repo and replace the corresponding file with our modified file as indicated by their path.

We used Nvidia RTX3060 (sm_86) to train, which requires cuda 11.0 above so the corresponding cudatoolkit is also 11.0 above for python.

### Datasets and Preprocessing ###
We used the MaksTheFace: https://github.com/aqeelanwar/MaskTheFace to generate the masks. TFill is taking two inputs: the original image and the mask only. We modified the ```mask_the_face.py``` file to generate and save the mask. We also wrote our own script ```preproc.py``` to preprocess the data options are set ```--convert``` to convert all images to either jpg format, set ```--resize``` to resize the images, and set ```--compare_dir``` compared the input dir and masks dir and remove all the images in the input image dir wich does not have a corresponding mask.

We preprocessed three different datasets:
1. Faces Kaggle dataset: https://www.kaggle.com/datasets/varump66/face-images-13233, with 256 by 256 resolution but only the last 8k examples (roughly).
2. FFHQ Kaggle dataset: https://www.kaggle.com/datasets/arnaud58/flickrfaceshq-dataset-ffhq, with 512 by 512 resolution but only the first 10k examples (roughly).
3. A small personalized dataset containing 100 images (roughly) of Arielle.

### Training Models ###

#### MAT #### 
We used the MAT: https://github.com/fenglinglwb/MAT for part of our exploration.
We tried their pretrained model on CelebA, using only several photos from the faces dataset and my own photo, we realized that MAT is not a suitable model for our task therefore we did not continue training/fine tuning. Sample testing outputs in the MAT_results folder.

#### TFill ####
We finally decided to use TFill: https://github.com/lyndonzheng/TFill 
To train on Nvidia RTX3060 GPU, we had to modify their ```environment.yaml``` file to make the ```cudatoolkit``` version match with the Nvidia dirver, as well as some of the configurations in ```options/base_options.py```. We also modified the ```dataloader/data_loader.py``` to train on our own mask instead of their generated mask. We trainined/are still trainig three models now.

_Model 1_: ```M1_faces_from_scratch``` on the Faces Kaggle dataset, the faces dataset has a busier background so we might as well continue training to explore if the computational resource allows. We so far ran 127k iterations.

_Model 2_: ```M2_FFHQ_from_scratch``` on FFHQ with our own masks, training model from scratch. We so far ran 373500 iterations but in their paper, the TFill model ran for 2000000 iterations, so to get a better performance, we need to train for longer.

_Model 3_: ```M3_FFHQ_pretrained``` on FFHQ with our own masks, training model on top of their pretrained ffhq model which is trained on FFHQ512 for 20000000 iterations. We so far ran 148k iterations. *We will be focuing on this option for now and is currently training this model.*

Saved training outcomes are in the checkpoints folder, saved training models can be found here: https://drive.google.com/drive/folders/1dYA3I32faUzpwaiH8NCgcDqTCo44OqzY?usp=sharing, testing results in the TFill_results folder, we will be adding more later including FID scores and other metrics that may be useful and will add 100 more testing photos.

### Future Steps ###
Once we get the models and testing results, these parts will be added to the Training Models Section.

Fine tune for the user (more customized), pick a best pretrained model then train and fine tune it using user input datasets (ex. Taylor Swift 100 datasets) to make sure the face generated looks similar to the person.

