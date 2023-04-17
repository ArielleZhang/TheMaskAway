# Triple-Dots
ECE324 Course Project

### Set up ###
We used MaskTheFace, MAT, TFill repos, we attached the link to their repo when they are later referenced, all the modified and added scripts are uploaded here in our repo to set up you need to clone their repo and replace the corresponding file with our modified file as indicated by their path.

We used Nvidia RTX3060 (sm_86) to train, which requires cuda 11.0 above so the corresponding cudatoolkit is also 11.0 above for python.

### Datasets and Preprocessing ###
We modifed and cloned the MaskTheFace: https://github.com/aqeelanwar/MaskTheFace to generate the masks. TFill is taking two inputs: the original image and the mask only. We modified the ```MaskTheFace/mask_the_face.py``` file to generate and save the mask. We also wrote our own script ```MaskTheFace/preproc.py``` to preprocess the data options are set ```--convert``` to convert all images to either jpg format, set ```--resize``` to resize the images, and set ```--compare_dir``` compared the input dir and masks dir and remove all the images in the input image dir wich does not have a corresponding mask, and set ```--crop``` to crop and enlarge the input images which is used for enlarging the digital masks to make sure it covers the entire medical mask.

We preprocessed three different datasets:
1. Faces Kaggle dataset: https://www.kaggle.com/datasets/varump66/face-images-13233, with 256 by 256 resolution of 8k examples (roughly) + 2k testing examples, and 10-20% mask ratio.
2. FFHQ Kaggle dataset: https://www.kaggle.com/datasets/arnaud58/flickrfaceshq-dataset-ffhq, with 512 by 512 resolution of 10k examples (roughly) and 30-40% mask ratio.
3. A small personalized Taylor Swift dataset containing 133 examples + 16 testing examples, and 20-30% mask ratio.
4. A small personalized Benedict Cumberbatch dataset containing 115 examples + 14 testing examples, and 20-30% mask ratio.

Notice that every dataset contains original images and the corresponding masks and the cuztomized datasets can be found in the Customized_Datasets folder

### Training Models ###

#### MAT #### 
We used the MAT: https://github.com/fenglinglwb/MAT for part of our exploration.
We tried their pretrained model on CelebA, using only several photos from the faces dataset and my own photo, we realized that MAT is not a suitable model for our task therefore we did not continue training/fine tuning. Sample testing outputs in the results/MAT_results folder.

#### TFill ####
We finally decided to use TFill: https://github.com/lyndonzheng/TFill the TFill folder contains the cloned and modified scripts from the original repo.
To train on Nvidia RTX3060 GPU, we had to modify their ```TFill/environment.yaml``` file to make the ```cudatoolkit``` version match with the Nvidia dirver, as well as some of the configurations in ```TFill/options/base_options.py```. We also modified the ```TFill/dataloader/data_loader.py``` to train on our own mask instead of their generated mask. We trainined/are still trainig three models now. We modified scripts in the ```TFill/evaluations``` folder to obtain the FID scores.

_Model 1_: ```M1_faces_from_scratch``` on the Faces Kaggle dataset, the faces dataset has a busier background so we might as well continue training to explore if the computational resource allows. We so far ran 127k iterations.

_Model 2_: ```M2_FFHQ_from_scratch``` on FFHQ with our own masks, training model from scratch. We so far ran 373500 iterations but in their paper, the TFill model ran for 2,000,000 iterations, so to get a better performance, we need to train for longer.

_Model 3_: ```M3_FFHQ_pretrained``` on FFHQ with our own masks, training model on top of their pretrained ffhq model which is trained on FFHQ512 for 2,000,000 iterations. We trained the pretrained model on our own FFHQ masks dataset (10,000) for 800,000 iterations and to add diversity we further trained on the faces dataset (8000) for 400,000 iterations. *This one is the best base model we trained*

_Model 3 TaylorSwift_: ```M3_FFHQ_pretrained_TS``` fine tuned ```M3_FFHQ_pretrained``` on Taylor Swift (133 images) for 60,000 iterations untill the model converges. The plotted loss curve showed overfitting close to 60,000 thus we used the model saved at checkpoint 50,000.

_Model 3 BenedictCumberbatch_: ```M3_FFHQ_pretrained_BC``` fine tuned ```M3_FFHQ_pretrained``` on Benedict Cumberbatch (115 images) for 50,000 iterations untill the model converges. The plotted loss curve showed overfitting close to 40,000 thus we used the model saved at checkpoint 40,000.

Saved training outcomes are in the checkpoints folder, saved training models can be found here: https://drive.google.com/drive/folders/1dYA3I32faUzpwaiH8NCgcDqTCo44OqzY?usp=sharing

### Test ###

#### M3_Base Model ####
This is the base model we trained and any user can provide 100-200 selfies for us to customize the model by fine tuning on their photos for better inference results.
The base model is trained on both FFHQ and faces datasets with our own masks. For testing we selected 2000 from the faces datasets and calculated the FID score. Everything is in the results/M3 folder.
FID on the 2000 testing dataset: 6.8383

#### M3_Base Model TaylorSwift ####
We cuztomized the base model on Taylor Swift dataset (133 images). For testing we tested the Taylor Swift Model on the TS testing datasets and calculated the FID score. For a fair comparison we also tested the TS testing datasets on the M3 Model.
M3_TS FID: 33.8927 (with 20-30% mask ratio)
M3 FID: 68.6593 (with 20-30% mask ratio)

For qualitative testings we picked 4 images of Taylor Swift wearing a mask and used the Meta SAM API (code included in ```Mask_Extraction.ipynb```) to extract the mask for regeneration. 

Everything is in the results/TS folder.

#### M3_Base Model BenedictCumberbatch ####
We cuztomized the base model on Benedict Cumberbatch dataset (115 images). For testing we tested the Benedict Cumberbatch Model on the BC testing datasets and calculated the FID score. For a fair comparison we also tested the BC testing datasets on the M3 Model.
M3_BC FID: 23.2846 (with 20-30% mask ratio)
M3 FID: 27.6326 (with 20-30% mask ratio)



For qualitative testings we picked 4 images of Benedict Cumberbatch wearing a mask and used the Meta SAM API (code included in ```Mask_Extraction.ipynb```) to extract the mask for regeneration. 

Everything is in the results/BC folder.

#### Future Steps ####
1. If we have enougth of time, we can continue training M1, M2 models from scratch.
2. When the input digital mask does not cover the entire medial mask, the exposed edge will affect the outcome, we tried to resize the generated digital mask however due to randomness sometimes the mask still won't be covered entirely. In the future we can try to improve this.


### Citations ###
MaskTheFace:
```
@misc{anwar2020masked,
title={Masked Face Recognition for Secure Authentication},
author={Aqeel Anwar and Arijit Raychowdhury},
year={2020},
eprint={2008.11104},
archivePrefix={arXiv},
primaryClass={cs.CV}
} 
```

TFill: 
```
@InProceedings{Zheng_2022_CVPR,
    author    = {Zheng, Chuanxia and Cham, Tat-Jen and Cai, Jianfei and Phung, Dinh},
    title     = {Bridging Global Context Interactions for High-Fidelity Image Completion},
    booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
    month     = {June},
    year      = {2022},
    pages     = {11512-11522}
}

@inproceedings{zheng2019pluralistic,
  title={Pluralistic Image Completion},
  author={Zheng, Chuanxia and Cham, Tat-Jen and Cai, Jianfei},
  booktitle={Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition},
  pages={1438--1447},
  year={2019}
}

@article{zheng2021pluralistic,
  title={Pluralistic Free-From Image Completion},
  author={Zheng, Chuanxia and Cham, Tat-Jen and Cai, Jianfei},
  journal={International Journal of Computer Vision},
  pages={1--20},
  year={2021},
  publisher={Springer}
}
```

SAM:
```
@article{kirillov2023segany,
  title={Segment Anything},
  author={Kirillov, Alexander and Mintun, Eric and Ravi, Nikhila and Mao, Hanzi and Rolland, Chloe and Gustafson, Laura and Xiao, Tete and Whitehead, Spencer and Berg, Alexander C. and Lo, Wan-Yen and Doll{\'a}r, Piotr and Girshick, Ross},
  journal={arXiv:2304.02643},
  year={2023}
}
```

### License ###
This project is licensed under the MIT License - see the LICENSE.md file for details
