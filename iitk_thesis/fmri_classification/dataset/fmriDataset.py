import sklearn
import numpy as np
import scipy.io as sio
#from sklearn.model_selection import KFold
#import matplotlib.pyplot as plt
#import matplotlib as mpl

# fMRI CMU dataset class
class fmriDataset:
    
    def __init__(self, multiDimention):
        # Download the dataset to data folder fetch the file names
        self.__filename = 'dataset/data-science-P1.mat'
        self.__X = None
        self.__Y = None

        # Parsing the data
        self.parseData(multiDimention)

    ### Converting flat fmri images to 3D
    def __convert3D(self, flatFMRI, converter3D):
        image3D = np.array(converter3D, dtype=float)

        # converting flat fmri to 3D fmri image
        for i in range(converter3D.shape[0]):
            for j in range(converter3D.shape[1]):
                for k in range(converter3D.shape[2]):
                    index = converter3D[i][j][k]
                    if index != 0:
                        image3D[i][j][k] = flatFMRI[index-1]

        return np.array(image3D)

    ### Getting the Data
    def getData(self):
        if len(self.__X) == 0:
            print("fMRI data not parsed")

        return self.__X, self.__Y

    ### Function to parse the data
    def parseData(self, multiDimention=False, categoryRequired=False, shuffle=False, normalize=True):
        matContents = sio.loadmat(self.__filename, squeeze_me=True)

        # fetching the label details
        info = matContents['info']

        category, label, epoch = [], [], []
        for item in info:
            category.append(item[0])
            label.append(item[2])
            epoch.append(item[4])

        if categoryRequired:
            Y = np.array(category)
        else:
            Y = np.array(label)

        x = matContents['data']
        x = np.array([list(i) for i in x])

        if normalize:
            xmax, xmin = x.max(), x.min()
            X = (x - xmin)/(xmax - xmin)
        else:
            X = x

        # fetching the fmri data
        if multiDimention:
            converter3D = sio.loadmat(self.__filename)
            converter3D = converter3D['meta']['coordToCol'][0][0]

            images3D = []
            for i in range(X.shape[0]):
                flat_img = X[i]
                full_img = self.__convert3D(flat_img, converter3D)
                images3D.append(full_img)

            X = images3D

        self.__X = np.array(X)
        self.__Y = np.array(Y)

    ### Display fMRI images
    def displayImage(self, rgbImage):
        fig = plt.figure(figsize=(8, 8))
        columns = 4
        rows = 5
        j = 2
        for i in range(1, columns*rows +1):
            fig.add_subplot(rows, columns, i)
            plt.imshow(rgbImage[:,:, i])

    ### Convert medical images to RGB
    def __convert_RGB(self, image):
        max_val = np.max(image)
        min_val = np.min(image)

        img = (image - min_val) / (max_val - min_val)
        return img*255

#kf = KFold(n_splits=6)
#for train_index, test_index in kf.split(range(6)):
#    print(train_index, test_index)

