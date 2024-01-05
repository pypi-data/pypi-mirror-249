import numpy as np
from scipy.ndimage import median_filter
from IPython.display import clear_output
import concurrent.futures as cf
import os
import cv2 as cv
import pkg_resources
from scipy.signal import savgol_filter
from natsort import natsorted
from scipy.signal import find_peaks
from scipy.interpolate import griddata


#Multiple of these functions takes an optional argument defining in which axis
#the function operates. If 's' is passed as an argument, the operation is performed
#along the spectral axis (across bands/variables). If the argument is 'b', the
#function operates on each band/variable individually

#Subtrats the mean from the data, either the mean of each spectrum (axis = 's')
#or the mean of each band (axis = 'b')
def mean_center(data_cube, axis = 's'):
    if axis == 's':
        return data_cube - np.nanmean(data_cube, axis = 2)[:,:,np.newaxis]
    elif axis == 'b':
        return data_cube - np.nanmean(data_cube, axis = (0,1))
    else:
        raise Exception("Invalid input argument. Axis input argument must be either 's' or 'b'")

#Subtracts mean and scales with STD - the old standardize function. Setting
#axis = 's' is the same as doing SNV (standard normal variate)
def autoscale(data_cube, axis = 's'):
    if axis == 's':
        std_cube = np.std(data_cube, axis = 2)[:,:,np.newaxis]
        std_cube[std_cube < 1e-6] = np.nan
        return (data_cube - np.mean(data_cube, axis = 2)[:,:,np.newaxis])/std_cube
    elif axis == 'b':
        return (data_cube - np.mean(data_cube, axis = (0,1)))/np.std(data_cube, axis = (0,1))
    else:
        raise Exception("Invalid input argument. Axis input argument must be either 's' or 'b'")

#Uses norm of given order for normalization. If axis = 's', then each spectrum is
#divided by its norm. If axis = 'b', then every band is divided by the norm of
#the entire band.
def norm_normalization(data_cube, order, axis = 's'):
    if axis == 's':
        return data_cube/np.linalg.norm(data_cube, ord = order, axis = 2)[:,:,np.newaxis]
    elif axis == 'b':
        return data_cube/np.linalg.norm(data_cube, ord = order, axis = (0,1))
    else:
        raise Exception("Invalid input argument. Axis input argument must be either 's' or 'b'")

#Apply multiplicative scatter correction to entire datacube. If no reference
#spectrum is supplied, the mean spectrum of the cube is used instead.
def msc(data_cube, ref_spec = None):
    if ref_spec == None:
        ref_spec = np.nanmean(data_cube, axis = (0,1))
        ref_spec_mean = np.nanmean(ref_spec)
        ref_spec = ref_spec - ref_spec_mean
    else:
        ref_spec_mean = np.nanmean(ref_spec)
        ref_spec - ref_spec_mean
    ref_spec = ref_spec[:,np.newaxis]
    X = mean_center(data_cube, 's')
    X = X.reshape([X.shape[0]*X.shape[1], X.shape[2]])
    X = np.rot90(X, 3)

    b = np.linalg.inv(ref_spec.T@ref_spec)@ref_spec.T@X
    b[b<1e-8] = np.nan
    X_new = X/b + ref_spec_mean
    X_new = np.rot90(X_new)
    X_new = X_new.reshape([data_cube.shape[0], data_cube.shape[1], data_cube.shape[2]])
    return X_new

#Setting axis = 's' is the same as normalizing each spectrum (pixel) to span from 0 to 1
#axis = 'b' normalizes each band individually
def normalize(data_cube, axis = 's'):
    if axis == 's':
        cube = data_cube - np.nanmin(data_cube, axis = 2)[:,:,np.newaxis]
        max_cube = np.nanmax(cube, axis = 2)[:,:,np.newaxis]
        return cube/max_cube
    elif axis == 'b':
        cube = data_cube - np.nanmin(data_cube, axis = (0,1))
        return cube/np.nanmax(cube, axis = (0,1))
    else:
        raise Exception("Invalid input argument. Axis input argument must be either 's' or 'b'")

#Normalizes the cube to span from 0 to 1
def normalize_cube(data_cube):
    cube = data_cube - np.nanmin(data_cube)
    return cube/np.nanmax(cube)

#Subtracts selected band from all layers in the cube
def subtract_band(data_cube, band):
    return data_cube - data_cube[:,:,band][:,:,np.newaxis]

#Flattens data cube into 2D array
def flatten(data_cube):
    return np.reshape(data_cube, [data_cube.shape[0]*data_cube.shape[1], data_cube.shape[2]])

#Reshapes flattened data cube back into 3 dimensions
def inflate(array_2D, n_rows, n_cols):
    return np.reshape(array_2D, [n_rows, n_cols, array_2D.shape[1]])

#Median filters each band in data cube
def median_filter_cube(data_cube, kernel_size):
    band_lst = []
    for i in range(data_cube.shape[2]):
        band_lst.append(data_cube[:,:,i])
    kernel_size_lst = np.ones(len(band_lst), dtype = int)*kernel_size
    with cf.ThreadPoolExecutor() as executor:
        results = executor.map(median_filter, band_lst, kernel_size_lst)
    filtered_cube = np.zeros_like(data_cube)
    for i, result in enumerate(results):
        filtered_cube[:,:,i] = result
    return filtered_cube

#Median filters a 2D array and only applies it to the locations marked as True
#in the px_idx array.
def targeted_median_filter(input_array, px_idx, kernel_size):
    if input_array.shape != px_idx.shape:
        print("Arrays must be the same shape. px_idx must be a true/false numpy array")
        return
    if type(input_array[0,0]) is not np.float64:
         input_array = input_array.astype(float)
    filtered_array = median_filter(input_array, size = kernel_size)
    input_array[px_idx] = filtered_array[px_idx]
    return input_array

#Imports cube based on directory argument
# def load_cube(directory):
#     if '.pam' in directory:
#         data = np.fromfile(directory,  dtype=np.uint8)   #importing filename to data
#         header = []
#         i = 0
#         while (header[i-8:i] != ['E','N','D','H','D','R','\r','\n']):
#             header.append(chr(data[i]))
#             i += 1
#         #Make header into a single string and split into list of strings whenever there is a space
#         string_lst = ''.join(header).replace('\r\n', ' ').split(' ') 
#         N_rows = int(string_lst[string_lst.index('WIDTH')+1])
#         N_wvls = int(string_lst[string_lst.index('HEIGHT')+1])
#         N_cols = int(string_lst[string_lst.index('DEPTH')+1])
#         cube = np.reshape(data[i:], [N_rows ,N_cols ,N_wvls], order = 'F')
#         cube = cube.astype(float)
#     elif '.npy' in directory:
#         cube = np.load(directory)
#         cube = cube.astype(float)
#     else:
#         file_list = [x for x in os.listdir(f'{directory}/images/capture') if ".ppm" and not "RGB" in x] 
#         file_list = natsorted(file_list)
#         cube = []
#         for file in file_list: #load bands into data structure
#             cube.append(np.rot90(cv.imread(f'{directory}/images/capture/{file}',cv.IMREAD_ANYDEPTH)))
#         cube = np.array(cube, dtype = 'float64')
#         cube = np.moveaxis(cube, 0, 2) #Rearranges the array to required shape
#     return cube

#Calculates hottelings T^2 statistic for matrix X, where the variables are
#represented by each column and the samples by the rows
#https://learnche.org/pid/latent-variable-modelling/principal-component-analysis/hotellings-t2-statistic
def hottelings(X):
    return np.nansum((X/np.nanstd(X, axis=0))**2, axis=1)

#Calculates the upper and lower 95% confidence limits of the mean of input vector, x
def conf95lim(x):
    conf = []
    mean = np.nanmean(x)
    std = np.nanstd(x)
    conf.append(mean-2*std)
    conf.append(mean+2*std)
    return conf

#Select three layers (either as a list or numpy vector) and use these three as the
#channels of an rgb image. The first layer is the red channel, the second layer
#the green channel and the third layer is the blue channel.
def array2rgb(data_cube, three_layers):
    three_layer_cube = np.zeros([data_cube.shape[0], data_cube.shape[1], 3])
    three_layer_cube[:,:,0] = data_cube[:,:,three_layers[0]] - np.nanmin(data_cube[:,:,three_layers[0]])
    three_layer_cube[:,:,0] = three_layer_cube[:,:,0]/np.nanmax(three_layer_cube[:,:,0])
    three_layer_cube[:,:,1] = data_cube[:,:,three_layers[1]] - np.nanmin(data_cube[:,:,three_layers[1]])
    three_layer_cube[:,:,1] = three_layer_cube[:,:,1]/np.nanmax(three_layer_cube[:,:,1])
    three_layer_cube[:,:,2] = data_cube[:,:,three_layers[2]] - np.nanmin(data_cube[:,:,three_layers[2]])
    three_layer_cube[:,:,2] = three_layer_cube[:,:,2]/np.nanmax(three_layer_cube[:,:,2])
    return three_layer_cube

#This function calculates and applies a NUC to the entire datacube. The NUC is
#dependent on the sensor temperature and the GSK settings of the camera. The
#NUC is calculated from camera specific calibration files from the accompanying NUC directory
def apply_NUC_cube(cube, sensor_temp, GSK, camera_ID = '10_10_200_191'):

    resource_package = __name__
    resource_path_offset = '/'.join(('HSTI_data_files-main', f"NUC/{camera_ID}/offset_coefs_1st_order.npy"))  # Do not use os.path.join()
    resource_path_slope = '/'.join(('HSTI_data_files-main', f"NUC/{camera_ID}/slope_coefs_1st_order.npy"))  # Do not use os.path.join()
    path_offset = pkg_resources.resource_stream(resource_package, resource_path_offset)
    path_slope = pkg_resources.resource_stream(resource_package, resource_path_slope)
    offset_coefs = np.load(path_offset, allow_pickle = True)
    slope_coefs = np.load(path_slope, allow_pickle = True)

    M = np.array([[GSK, sensor_temp, 1]]).T

    offsets = offset_coefs@M
    slopes = slope_coefs@M

    mean_offset = np.nanmean(offsets)
    mean_slopes = np.nanmean(slopes)

    offset_correction = - mean_slopes*offsets/slopes + mean_offset
    slope_correction = (mean_slopes - slopes)/slopes

    offset_matrix = offset_correction.reshape([cube.shape[0], cube.shape[1]], order = 'C')
    slope_matrix = slope_correction.reshape([cube.shape[0], cube.shape[1]], order = 'C')

    temp_cube = np.copy(cube)
    for i in range(temp_cube.shape[2]):
        temp_cube[:,:,i] = temp_cube[:,:,i] + temp_cube[:,:,i]*slope_matrix + offset_matrix
    return temp_cube

#This function calculates and applies a NUC to a single image. The NUC is dependent
#on the sensor temperature and the GSK settings of the camera. The NUC is
#calculated from camera specific calibration files from the accompanying NUC directory.
def apply_NUC_image(image, sensor_temp, GSK, camera_ID = '10_10_200_191'):

    resource_package = __name__
    resource_path_offset = '/'.join(('HSTI_data_files-main', f"NUC/{camera_ID}/offset_coefs_1st_order.npy"))  # Do not use os.path.join()
    resource_path_slope = '/'.join(('HSTI_data_files-main', f"NUC/{camera_ID}/slope_coefs_1st_order.npy"))  # Do not use os.path.join()
    path_offset = pkg_resources.resource_stream(resource_package, resource_path_offset)
    path_slope = pkg_resources.resource_stream(resource_package, resource_path_slope)
    offset_coefs = np.load(path_offset, allow_pickle = True)
    slope_coefs = np.load(path_slope, allow_pickle = True)


    M = np.array([[GSK, sensor_temp, 1]]).T

    offsets = offset_coefs@M
    slopes = slope_coefs@M

    mean_offset = np.nanmean(offsets)
    mean_slopes = np.nanmean(slopes)

    offset_correction = - mean_slopes*offsets/slopes + mean_offset
    slope_correction = (mean_slopes - slopes)/slopes

    offset_matrix = offset_correction.reshape([image.shape[0], image.shape[1]], order = 'C')
    slope_matrix = slope_correction.reshape([image.shape[0], image.shape[1]], order = 'C')

    return image  + image*slope_matrix + offset_matrix

def naive_temperature_image(image, sensor_temp, GSK, camera_ID = '10_10_200_191'):
    resource_package = __name__
    resource_path_offset = '/'.join(('HSTI_data_files-main', f"Temperature_conversions/{camera_ID}/temp_offset_coefs_1st_order.npy"))  # Do not use os.path.join()
    resource_path_slope = '/'.join(('HSTI_data_files-main', f"Temperature_conversions/{camera_ID}/temp_slope_coefs_1st_order.npy"))  # Do not use os.path.join()
    path_offset = pkg_resources.resource_stream(resource_package, resource_path_offset)
    path_slope = pkg_resources.resource_stream(resource_package, resource_path_slope)
    offset_coefs = np.load(path_offset, allow_pickle = True)
    slope_coefs = np.load(path_slope, allow_pickle = True)

    a = slope_coefs[:,0]*GSK + slope_coefs[:,1]*sensor_temp + slope_coefs[:,2]
    b = offset_coefs[:,0]*GSK + offset_coefs[:,1]*sensor_temp + offset_coefs[:,2]

    flat_img = np.reshape(image, image.size)
    flat_img = flat_img*a + b
    return np.reshape(flat_img, [image.shape[0], image.shape[1]])

def naive_temperature_cube(data_cube, sensor_temp, GSK, camera_ID = '10_10_200_191'):
    resource_package = __name__
    resource_path_offset = '/'.join(('HSTI_data_files-main', f"Temperature_conversions/{camera_ID}/temp_offset_coefs_1st_order.npy"))  # Do not use os.path.join()
    resource_path_slope = '/'.join(('HSTI_data_files-main', f"Temperature_conversions/{camera_ID}/temp_slope_coefs_1st_order.npy"))  # Do not use os.path.join()
    path_offset = pkg_resources.resource_stream(resource_package, resource_path_offset)
    path_slope = pkg_resources.resource_stream(resource_package, resource_path_slope)
    offset_coefs = np.load(path_offset, allow_pickle = True)
    slope_coefs = np.load(path_slope, allow_pickle = True)

    a = slope_coefs[:,0]*GSK + slope_coefs[:,1]*sensor_temp + slope_coefs[:,2]
    b = offset_coefs[:,0]*GSK + offset_coefs[:,1]*sensor_temp + offset_coefs[:,2]

    flat_cube = np.reshape(data_cube, [data_cube.shape[0]*data_cube.shape[1], data_cube.shape[2]])
    flat_cube = flat_cube*a[:,np.newaxis] + b[:,np.newaxis]
    return np.reshape(flat_cube, [data_cube.shape[0], data_cube.shape[1], data_cube.shape[2]])

def rsvd(input_matrix, rank, power_iter = 3): #https://towardsdatascience.com/intuitive-understanding-of-randomized-singular-value-decomposition-9389e27cb9de
    Omega = np.random.randn(input_matrix.shape[1], rank)
    Y = input_matrix @ Omega
    for q in range(power_iter):
        Y = input_matrix @ (input_matrix.T @ Y)
    Q, _ = np.linalg.qr(Y)
    B = Q.T @ input_matrix
    u_tilde, s, v = np.linalg.svd(B, full_matrices = False)
    u = Q @ u_tilde
    return u, s, v 

def relative_mirror_separation(directory):

    temp = []
    with open(f'{directory}/output.txt', 'r') as file:
        lines = file.readlines()
        df = np.zeros([len(lines),len(lines[-1].split())])*np.nan
        for i in range(len(lines)):
            splits = lines[i].split()
            for j in range(len(splits)):
                df[i,j] = splits[j]
        section_last_idx = np.where(np.diff(df[:,0])<0)
        sections = [df[0:section_last_idx[0][0]+1]]
        for i in range(len(section_last_idx[0])-1):
            sections.append(df[section_last_idx[0][i]+1:section_last_idx[0][i+1]+1])
        sections.append(df[section_last_idx[0][-1]+1:])

    diode = sections
    I0 = savgol_filter(diode[-1][:,3], 5, 2, 0)
    I0 = I0-np.min(I0)
    I0 = I0/np.max(I0)
    I1 = savgol_filter(diode[-1][:,4], 5, 2, 0)
    I1 = I1-np.min(I1)
    I1 = I1/np.max(I1)
    I2 = savgol_filter(diode[-1][:,5], 5, 2, 0)
    I2 = I2-np.min(I2)
    I2 = I2/np.max(I2) 

    steps = np.arange(len(I0))
    peaks_I0_idx, _ = find_peaks(I0, prominence=1e-1)
    troughs_I0_idx, _ = find_peaks(-I0, prominence=1e-1)
    peaks_I1_idx, _ = find_peaks(I1, prominence=1e-1)
    troughs_I1_idx, _ = find_peaks(-I1, prominence=1e-1)
    peaks_I2_idx, _ = find_peaks(I2, prominence=1e-1)
    troughs_I2_idx, _ = find_peaks(-I2, prominence=1e-1)

    idx0 = np.sort(np.concatenate((peaks_I0_idx, troughs_I0_idx)))
    idx1 = np.sort(np.concatenate((peaks_I1_idx, troughs_I1_idx)))
    idx2 = np.sort(np.concatenate((peaks_I2_idx, troughs_I2_idx)))

    window_len = 10
    all_idx_in_range = np.array([])
    counter = 0
    while len(all_idx_in_range) < 3:
        idx0_in_range = idx0[(idx0>=steps[counter]) & (idx0 < steps[counter+window_len])]
        idx1_in_range = idx1[(idx1>=steps[counter]) & (idx1 < steps[counter+window_len])]
        idx2_in_range = idx2[(idx2>=steps[counter]) & (idx2 < steps[counter+window_len])]
        all_idx_in_range = np.concatenate((idx0_in_range, idx1_in_range, idx2_in_range))
        counter += 1
    idx0 = idx0[idx0 >= all_idx_in_range[0]]
    idx1 = idx1[idx1 >= all_idx_in_range[1]]
    idx2 = idx2[idx2 >= all_idx_in_range[2]]

    dx = 686e-9/4 #dx = (lam/cos(theta))/4 - found using bandpass filters

    x0 = np.arange(len(idx0))*dx
    x1 = np.arange(len(idx1))*dx
    x2 = np.arange(len(idx2))*dx

    p0 = np.poly1d(np.polyfit(idx0, x0, 3))
    p1 = np.poly1d(np.polyfit(idx1, x1, 3))
    p2 = np.poly1d(np.polyfit(idx2, x2, 3))

    R_sqr0 = 1 - np.sum((x0 - p0(idx0))**2)/np.sum((x0 - np.mean(p0(idx0)))**2)
    R_sqr1 = 1 - np.sum((x1 - p1(idx1))**2)/np.sum((x1 - np.mean(p1(idx1)))**2)
    R_sqr2 = 1 - np.sum((x2 - p2(idx2))**2)/np.sum((x2 - np.mean(p2(idx2)))**2)

    p_comb = np.poly1d(np.polyfit(idx2, x2, 3))
    p_comb.coef[0] = (p0.coef[0]+p1.coef[0]+p2.coef[0])/3
    p_comb.coef[1] = (p0.coef[1]+p1.coef[1]+p2.coef[1])/3
    p_comb.coef[2] = (p0.coef[2]+p1.coef[2]+p2.coef[2])/3
    p_comb.coef[3] = (p0.coef[3]+p1.coef[3]+p2.coef[3])/3

    x_comb = np.concatenate((x0,x1,x2))
    idx_comb = np.concatenate((idx0,idx1,idx2))
    R_sqr_cmb = 1 - np.sum((x_comb - p_comb(idx_comb))**2)/np.sum((x_comb - np.mean(p_comb(idx_comb)))**2)

    file_list = [x for x in os.listdir(f'{directory}/images/capture') if ".ppm" and not "RGB" in x] 
    file_list = natsorted(file_list)
    cube_steps = [int(s.split('step')[1].split('.ppm')[0]) for s in file_list]

    return p_comb(cube_steps)


def correct_laser_pixels(img_cube):
    mask = np.zeros([10, 10], dtype = bool)
    mask[2,4:7] = True
    mask[3,3:8] = True
    mask[4:7,2:8] = True
    mask[7,3:7] = True
    xx, yy = np.meshgrid(np.arange(0, 10), np.arange(0, 10))
    bad_x = xx[~mask]
    bad_y = yy[~mask]
    for i in range(img_cube.shape[2]):
        temp = img_cube[471:481,381:391,i]
        img_cube[471:481,381:391,i] = griddata((bad_x, bad_y), temp[~mask].ravel(), (xx, yy), method = 'linear')
    return img_cube

def correct_laser_pixels_large(img_cube):
    mask = np.zeros([16, 16], dtype = bool)
    mask[2:-2,2:-2] = True
    xx, yy = np.meshgrid(np.arange(0, 16), np.arange(0, 16))
    bad_x = xx[~mask]
    bad_y = yy[~mask]
    for i in range(img_cube.shape[2]):
        temp = img_cube[468:484,378:394,i]
        img_cube[468:484,378:394,i] = griddata((bad_x, bad_y), temp[~mask].ravel(), (xx, yy), method = 'linear')
    return img_cube