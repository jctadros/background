import numpy as np
import cv2
import time, math
import matplotlib.pyplot as plt

class Interpol(object):
    DEFAULT_HALF_PATCH_WIDTH=4
    MODE_ADDITION=0
    MODE_MULTIPLICATION=1
    ERROR_INPUT_MAT_INVALID_TYPE=0
    ERROR_INPUT_MASK_INVALID_TYPE=1
    ERROR_MASK_INPUT_SIZE_MISMATCH=2
    ERROR_HALF_PATCH_WIDTH_ZERO=3
    CHECK_VALID=4
    inputImage = None
    mask = updatedMask = None
    result = None
    workImage = None
    sourceRegion = None
    targetRegion = None
    originalSourceRegion = None
    gradientX = None
    gradientY = None
    confidence = None
    data = None
    LAPLACIAN_KERNEL = NORMAL_KERNELX = NORMAL_KERNELY = None
    bestMatchUpperLeft = bestMatchLowerRight = None
    patchHeight = patchWidth = 0
    fillFront = []
    normals = []
    sourcePatchULList = []
    targetPatchSList = []
    targetPatchTList = []
    mode = None
    halfPatchWidth = None
    targetIndex = None

    def __init__(self, inputImage, mask, halfPatchWidth):
        self.inputImage = inputImage
        self.mask = np.copy(np.uint8(mask))
        self.updatedMask = np.copy(self.mask)
        self.workImage = np.copy(np.uint16(np.round(((2**16 - 1)*(inputImage-np.nanmin(inputImage)))/(np.nanmax(inputImage)-np.nanmin(inputImage)))))
        self.result = np.ndarray(shape=inputImage.shape, dtype=inputImage.dtype)
        self.halfPatchWidth = halfPatchWidth
        self.passImage = np.copy(self.inputImage)

    def Linear(self, file_name, output_path):
        global k
        self.initializeMats()
        self.calculateGradients()
        stay = True
        k = 0
        while stay:
            k += 1
            start = time.time()
            self.computeFillFront()
            self.interpol()
            stay = self.checkEnd()
            end  = time.time()
            cv2.imwrite(output_path+'/updatedMask/updatedMask_%.2d.png'%k, self.updatedMask)
            cv2.imwrite(output_path+'/iterations/inpaintedImage_%.2d.png'%k, self.workImage)
            print 'Iteration '+str(k)+' -- '+str(np.round(end-start,2))+' sec'

        self.result = np.copy(self.workImage)

    def initializeMats(self):
        _, self.confidence = cv2.threshold(self.mask, 10, 255, cv2.THRESH_BINARY)
        _, self.confidence = cv2.threshold(self.confidence, 2, 1, cv2.THRESH_BINARY_INV)
        self.sourceRegion  = np.copy(self.confidence)
        self.originalSourceRegion = np.copy(self.sourceRegion)
        self.confidence = np.float32(self.confidence)
        _, self.targetRegion = cv2.threshold(self.mask, 10 , 255, cv2.THRESH_BINARY)
        _, self.targetRegion = cv2.threshold(self.targetRegion, 2, 1, cv2.THRESH_BINARY)
        self.data = np.ndarray(shape=self.inputImage.shape[:2], dtype=np.float32)
        self.LAPLACIAN_KERNEL = np.ones((3, 3), dtype = np.float32)
        self.LAPLACIAN_KERNEL[1, 1] = -8
        self.NORMAL_KERNELX = np.zeros((3, 3), dtype = np.float32)
        self.NORMAL_KERNELX[1, 0] = -1
        self.NORMAL_KERNELX[1, 2] = 1
        self.NORMAL_KERNELY = cv2.transpose(self.NORMAL_KERNELX)

    def calculateGradients(self):
        srcGray = self.workImage
        self.gradientX = cv2.Scharr(srcGray, cv2.CV_32F, 1, 0)
        self.gradientX = cv2.convertScaleAbs(self.gradientX)
        self.gradientX = np.float32(self.gradientX)
        self.gradientY = cv2.Scharr(srcGray, cv2.CV_32F, 0, 1)
        self.gradientY = cv2.convertScaleAbs(self.gradientY)
        self.gradientY = np.float32(self.gradientY)

        height, width = self.sourceRegion.shape
        for y in range(height):
            for x in range(width):
                if self.sourceRegion[y, x] == 0:
                    self.gradientX[y, x] = 0
                    self.gradientY[y, x] = 0

        self.gradientX /= 2**16-1
        self.gradientY /= 2**16-1

    def computeFillFront(self):
        boundryMat = cv2.filter2D(self.targetRegion, cv2.CV_32F, self.LAPLACIAN_KERNEL)
        sourceGradientX = cv2.filter2D(self.sourceRegion, cv2.CV_32F, self.NORMAL_KERNELX)
        sourceGradientY = cv2.filter2D(self.sourceRegion, cv2.CV_32F, self.NORMAL_KERNELY)
        del self.fillFront[:]
        del self.normals[:]
        height, width = boundryMat.shape[:2]
        for y in range(height):
            for x in range(width):
                if boundryMat[y, x] > 0:
                    self.fillFront.append((x, y))
                    dx = sourceGradientX[y, x]
                    dy = sourceGradientY[y, x]
                    normalX, normalY = dy, - dx
                    tempF = math.sqrt(pow(normalX, 2) + pow(normalY, 2))
                    if not tempF == 0:
                        normalX /= tempF
                        normalY /= tempF
                    self.normals.append((normalX, normalY))

    def getPatch(self, point):
        centerX, centerY = point
        height, width = self.workImage.shape[:2]
        minX = max(centerX - 1, 0)
        maxX = min(centerX + 1, width - 1)
        minY = max(centerY - 1, 0)
        maxY = min(centerY + 1, height - 1)
        upperLeft = (minX, minY)
        lowerRight = (maxX, maxY)
        return upperLeft, lowerRight

    def interpol(self):
        inside = []
        for p in self.fillFront:
            (aX, aY), (bX, bY) = self.getPatch(p)
            for idx_y, y in enumerate(range(aY, bY + 1)):
                for idx_x, x in enumerate(range(aX, bX + 1)):
                    if self.targetRegion[y, x] == 1 and (self.targetRegion[y+1, x] == 0 or self.targetRegion[y-1, x] == 0 or self.targetRegion[y, x+1] == 0 or self.targetRegion[y, x-1] == 0):
                        inside.append((x,y))

        for pp in inside:
            (aX, aY), (bX, bY) = self.getPatch(pp)
            dict, s, c = {}, [], 1
            for idx_y, y in enumerate(range(aY, bY + 1)):
                for idx_x, x in enumerate(range(aX, bX + 1)):
                    dict[c] = [y, x]
                    if c==2 or c==4 or c==6 or c==8 :
                        s.append(self.passImage[y,x])
                    c+=1

            val_f = np.nanmean(s)
            val_8 = np.uint16(np.round(((2**16 - 1)*(val_f - np.nanmin(self.inputImage)))/(np.nanmax(self.inputImage)-np.nanmin(self.inputImage))))
            self.workImage[dict[5][0], dict[5][1]] = val_8
            self.passImage[dict[5][0], dict[5][1]] = val_f
            self.sourceRegion[dict[5][0], dict[5][1]] = 1
            self.targetRegion[dict[5][0], dict[5][1]] = 0
            self.updatedMask[dict[5][0], dict[5][1]]  = 0

    def checkEnd(self):
        height, width = self.sourceRegion.shape[:2]
        for y in range(height):
            for x in range(width):
                if self.sourceRegion[y, x] == 0:
                    return True
        return False
