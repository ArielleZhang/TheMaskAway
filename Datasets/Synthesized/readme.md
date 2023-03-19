### Synthesized Masked Data ###

I gave up lol, the dataset it too big to upload. 

This dir contains the original dataset found at: https://www.kaggle.com/datasets/varump66/face-images-13233
Every person has multiple photos but with roughly same posture and angle.

Follow the MaskTheFace repo instruction to add masks: REMEMBER TO USE PYTHON3.6 FOR THE VENV!!! To make black inpainting, you can change the default ```--color``` to be ```#010101``` which is black, and choose ```cloth``` for ```--mask_type```.

Use the resize.py to resize all the photos. Default is 256 by 256. Remember to specify your input dir for ```--path```. ```/lanczos``` contains the better quality photos, ```/resized``` contains the meh ones, but the photos in these two dirs are the same.
