```py
# Demo - train the DenseFuse network & use it to generate an image

from __future__ import print_function
import tensorflow as tf
#from train_recons import train_recons
from train import train
from generate import generate
from utils import list_images
import os
import time

# True for training phase
#IS_TRAINING = True
IS_TRAINING = False     #是否训练
# True for video sequences(frames)
IS_VIDEO = False   #是否是视频
# True for RGB images
#IS_RGB = False是否是彩色图像
IS_RGB = True
# True - 1000 images for validation
# This is a very time-consuming operation when TRUE
IS_Validation = False  #是否进行检验

BATCH_SIZE = 2
EPOCHES = 4  #迭代多少次

SSIM_WEIGHTS = [1, 10, 100, 1000]  #ssim损失函数权重
MODEL_SAVE_PATHS = [   #模型保存路径
    './models/densefuse_gray/densefuse_model_bs2_epoch4_all_weight_1e0.ckpt',
    './models/densefuse_gray/densefuse_model_bs2_epoch4_all_weight_1e1.ckpt',
    './models/densefuse_gray/densefuse_model_bs2_epoch4_all_weight_1e2.ckpt',
    './models/densefuse_gray/densefuse_model_bs2_epoch4_all_weight_1e3.ckpt',
]
model_pre_path = None

def main():
	if IS_TRAINING:  #如果是训练,训练路径和测试路径
		original_imgs_path = list_images('./train/')
		validatioin_imgs_path = list_images('./validation/')
         #遍历SSIM_WEIGHTS, MODEL_SAVE_PATHS给ssim_weight, model_save_path
		for ssim_weight, model_save_path in zip(SSIM_WEIGHTS, MODEL_SAVE_PATHS):
			print('\nBegin to train the network ...\n')
			train(original_imgs_path, validatioin_imgs_path, model_save_path, model_pre_path, ssim_weight, EPOCHES, BATCH_SIZE, IS_Validation, debug=True)

			print('\nSuccessfully! Done training...\n')
	else:
		if IS_VIDEO:   #如果是视频，损失函数权重取1
			ssim_weight = SSIM_WEIGHTS[0]
			model_path = MODEL_SAVE_PATHS[0]

			IR_path = list_images('video/1_IR/')
			VIS_path = list_images('video/1_VIS/')
			output_save_path = 'video/fused'+ str(ssim_weight) +'/'
			generate(IR_path, VIS_path, model_path, model_pre_path,
			         ssim_weight, 0, IS_VIDEO, 'addition', output_path=output_save_path)
		else:
			ssim_weight = SSIM_WEIGHTS[2]
			model_path = MODEL_SAVE_PATHS[2]
			print('\nBegin to generate pictures ...\n')
			#path1 = './pet_mri/MR/'原代码
			# path1='./pet_mri/mri/'
			# path2 = './pet_mri/Y/'
			path1 = './pet_mri/mri/'
			path2 = './pet_mri/pet/'
			for i in range(1,30):
				index = i 
				# RGB images修改
				infrared = path1 + str(index) + '_mri' + '.bmp'
				#visible = path2+ str(index ) + '_pet'+ '.bmp'
				#修改
				visible = path2 + str(index) + '_pet' + '.bmp'
				# choose fusion layer生成融合图片
				fusion_type = 'addition'
				output_save_path = 'pet_mri/fusion_Y/addition'
				generate(infrared, visible, model_path, model_pre_path,
						 ssim_weight, index, IS_VIDEO, IS_RGB, type = fusion_type, output_path = output_save_path)
			
if __name__ == '__main__':
    main()
	




```

