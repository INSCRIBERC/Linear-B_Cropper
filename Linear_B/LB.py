# Sources
# https://stackoverflow.com/questions/28327020/opencv-detect-mouse-position-clicking-over-a-picture
# https://stackoverflow.com/questions/48301186/cropping-concave-polygon-from-image-using-opencv-python

import cv2
import numpy as np
from copy import copy
from copy import deepcopy
import os, glob
from argparse import ArgumentParser 

def get_args():
    parser = ArgumentParser(description = "Filename", add_help = True)
    parser.add_argument('-dir', '--root_directory', type = str, help = 'Root directory', dest = 'PATH', default = os.getcwd())
    parser.add_argument('-n', '--name', type = str, help = 'File name of the tablet', dest = 'tab', default = None)
    parser.add_argument('-l', '--line', type = int, help = 'Starting line', dest = 'LINE', default = 1)
    parser.add_argument('-s', '--sign', type = int, help = 'Starting sign at line "LINE"', dest = 'SIGN', default = 1)
    return parser.parse_args()

def onMouse(event, x, y, flags, param):
   global posList
   if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img,(x,y),10,(255,0,0),-1)
        posList.append((x, y))

if __name__ == '__main__':
    
    args = get_args()
    root_dir = args.PATH
    tab = args.tab
    LINE = args.LINE
    STARTING_SIGN = args.SIGN

    tab_filename = os.path.basename(glob.glob(os.path.join(root_dir, tab + '.*'))[0])
    lines = []
    num_signs_per_line = []
    with open(root_dir + os.sep + 'LB.txt', 'r') as f:
        z = f.readlines()
        for i in z:
            TAB, signs = i.split(';;')
            if tab in TAB:
                SIGNS = signs.split(',')
                lines.append(SIGNS)
                num_signs_per_line.append(len(SIGNS))

    tab_path = root_dir + tab_filename
    path_mask1 = args.PATH + os.sep + 'Mask1'
    path_mask2 = args.PATH + os.sep + 'Mask2'
    path_mask3 = args.PATH + os.sep + 'Mask3'
    path_cropped = args.PATH + os.sep + 'Cropped'
    path_completed = args.PATH + os.sep + 'Completed'

    new_directories = [path_mask1,
                  path_mask2,
                  path_mask3,
                  path_cropped, 
                  path_completed]

    for new_directory in new_directories:
        try:
            os.mkdir(new_directory)
        except:
            pass

    img = cv2.imread(tab_path)
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', 600, 600)
    finish = False
    while not finish:
        cv2.imshow('image',img)
        key = cv2.waitKey(0)
        if key == ord('y'):
            readable = 'y'
            finish = True
        elif key == ord('n'):
            readable = 'n'
            finish = True
    
    cv2.destroyAllWindows()    

    if readable == 'y':
    	break_out_flag = False
    	for i in range(len(num_signs_per_line))[LINE-1:]:

    		if i == (LINE - 1):
    			signs_to_crop = range(len(lines[i]))[STARTING_SIGN-1:]
    		else:
    			signs_to_crop = range(len(lines[i]))

    		for j in signs_to_crop:
    			posList = []
    			img = cv2.imread(tab_path)
    			in_img = deepcopy(img)
    			cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    			cv2.setMouseCallback('image', onMouse)


    			while(1):
    				cv2.resizeWindow('image', 1000, 1000)
    				cv2.imshow('image',img)
    				k = cv2.waitKey(20) & 0xFF
    				if k == 27:
    					break
    				elif k == ord('b'):
    					break_out_flag = True
    			cv2.destroyAllWindows()

    			if break_out_flag == True:
    				cv2.destroyAllWindows()
    				break

    			posNp = np.array(posList)

    			try:
    				## (1) Crop the bounding rect
    				rect = cv2.boundingRect(posNp)
    				x,y,w,h = rect
    				cropped = in_img[y:y+h, x:x+w].copy()

    				## (2) make mask
    				posNp = posNp - posNp.min(axis=0)

    				mask = np.zeros(cropped.shape[:2], np.uint8)
    				cv2.drawContours(mask, [posNp], -1, (255, 255, 255), -1, cv2.LINE_AA)

    				## (3) do bit-op
    				dst = cv2.bitwise_and(cropped, cropped, mask=mask)

    				## (4) add the white background
    				bg = np.ones_like(cropped, np.uint8)*255
    				cv2.bitwise_not(bg,bg, mask=mask)
    				dst2 = bg + dst

    				sign_name = tab + '_' + str(i + 1) + '_' + str(j + 1) + '_' + lines[i][j].replace(' ', '').replace('\n', '') + '.png'

    				print(sign_name)

    				cv2.imwrite(path_mask1 + os.sep + sign_name, cropped)
    				cv2.imwrite(path_mask2 + os.sep + sign_name, mask)
    				cv2.imwrite(path_mask3 + os.sep + sign_name, dst)
    				cv2.imwrite(path_cropped + os.sep + sign_name, dst2)
    			except:
    				continue

    		if break_out_flag == True:
     			break

    else:
    	readme_name = path_cropped + os.sep + tab + '.txt'
    	with open(readme_name, 'w') as f:
    		f.write("I cannot read and/or detect some signs.")

    if break_out_flag == False:
        os.rename(root_dir + tab_filename, path_completed + os.sep + tab_filename)