import numpy as np
import cv2
import kernel
import param as pr

def preprocess(src):
	h, w = src.shape
	mImg = None
	src_pyrdown = None
	tmp = None
	thresholed = None
	mini_thresh = None
	dst = np.zeros((h / 2, w / 2), np.uint8);

	src_pyrdown = cv2.pyrDown(src)
	mImg = cv2.morphologyEx(src_pyrdown, cv2.MORPH_BLACKHAT, kernel.S2)
	#mImg = cv2.normalize(mImg, 0, 255, cv2.NORM_MINMAX)
	_, thresholed = cv2.threshold(mImg, int(10 * cv2.mean(mImg)[0]), 255, cv2.THRESH_BINARY)
	mini_thresh = np.copy(thresholed)

	mh, mw = mini_thresh.shape

	for i in xrange(0, mw - 32, 4):
		for j in xrange(0, mh - 16, 4):
			rect = mini_thresh[i: i + 16, j: j + 8]
			noneZero1 = cv2.countNonZero(rect)
			
			rect = mini_thresh[i: i + 16, j + 8: j + 16]
			noneZero2 = cv2.countNonZero(rect)
			
			rect = mini_thresh[i + 16: i + 32, j: j + 8]
			noneZero3 = cv2.countNonZero(rect)
			
			rect = mini_thresh[i + 16: i + 32, j + 8: j + 16]
			noneZero4 = cv2.countNonZero(rect)

			cnt = 0
			if noneZero1 > pr.NONEZERO_PARAM:
				cnt = cnt + 1
			if noneZero2 > pr.NONEZERO_PARAM:
				cnt = cnt + 1
			if noneZero3 > pr.NONEZERO_PARAM:
				cnt = cnt + 1
			if noneZero4 > pr.NONEZERO_PARAM:
				cnt = cnt + 1
			if cnt > 2:
				rect = mini_thresh[i: i + 32, j: j + 16]
				dst[i: i + 32, j: j + 16] = rect

	dst_clone = np.copy(dst)
	cv2.waitKey(0)
	dst = cv2.dilate(dst, kernel.S1, iterations=pr.DILATE_ERODE_ITER_PARAM)
	cv2.imshow("dst", dst)
	cv2.waitKey(0)
	dst = cv2.erode(dst, kernel.S1, iterations=pr.DILATE_ERODE_ITER_PARAM)
	cv2.imshow("dst", dst)
	cv2.waitKey(0)
	dst = cv2.pyrUp(dst);
	if pr.DEBUG == True:
		cv2.imshow("src", src)
		cv2.imshow("src_pyrdown", src_pyrdown)
		cv2.imshow("mImg", mImg)
		cv2.imshow("thresholed", thresholed)
		cv2.imshow("dst_clone", dst_clone)
		cv2.imshow("dst", dst)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
	return dst