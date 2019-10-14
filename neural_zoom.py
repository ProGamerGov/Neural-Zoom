import os
from PIL import Image
import subprocess


import argparse
parser = argparse.ArgumentParser()
# Neural-Zoom Options
parser.add_argument("-script", help="the style transfer script", type=str, default='')
parser.add_argument("-num_frames", help="number of frames to produce", type=int, default=30)

parser.add_argument("-crop", type=int, default=64)
parser.add_argument("-crop_width", type=int, default=0)
parser.add_argument("-crop_height", type=int, default=0)

parser.add_argument("-starting_image", help="Image to start zooming into", type=str, default='')
parser.add_argument("-start_num", help="Number to start naming from", type=int, default=0)

parser.add_argument("-num_zeros", help="Number of zeros", type=str, default='0000')
parser.add_argument("-num_mode", help="Whether to use trailing or leading numbers in output image names", type=int, choices=[0, 1], default=1)
parser.add_argument("-output_dir", default='output_dir')
parser.add_argument("-verbose", action='store_true')

# Basic options
parser.add_argument("-style_image", help="Style target image", default='')
parser.add_argument("-style_blend_weights", default=None) 
parser.add_argument("-content_image", help="Content target image", default='')
parser.add_argument("-image_size", help="Maximum height / width of generated image", type=int, default=512)
parser.add_argument("-gpu", help="Zero-indexed ID of the GPU to use; for CPU mode set -gpu = -1 (neural-style) or 'c' for neural-style-pt", default=0)
parser.add_argument("-multigpu_strategy", help="Index of layers to split the network across GPUs", default='')
parser.add_argument("-multidevice_strategy", help="Index of layers to split the network across devices", default='')

# Optimization options
parser.add_argument("-content_weight", type=float, default=5e0) 
parser.add_argument("-style_weight", type=float, default=1e2)
parser.add_argument("-tv_weight", type=float, default=1e-3)
parser.add_argument("-num_iterations", type=int, default=1000)
parser.add_argument("-normalize_gradients", action='store_true') 
parser.add_argument("-init", choices=['random', 'image'], default='random')
parser.add_argument("-init_image", default=None)
parser.add_argument("-optimizer", choices=['lbfgs', 'adam'], default='lbfgs')
parser.add_argument("-learning_rate", type=float, default=1e0)
parser.add_argument("-lbfgs_num_correction", type=int, default=0)

# Output options      
parser.add_argument("-print_iter", type=int, default=50)
parser.add_argument("-save_iter", type=int, default=0)
parser.add_argument("-output_image", default='out.png')

# Other options
parser.add_argument("-style_scale", type=float, default=1.0)
parser.add_argument("-original_colors", type=int, default=0)
parser.add_argument("-pooling", choices=['avg', 'max'], default='max')
parser.add_argument("-model_file", type=str, default='models/vgg19-d01eb7cb.pth')
parser.add_argument("-proto_file", type=str, default='')
parser.add_argument("-disable_check", action='store_true')
parser.add_argument("-backend", choices=['nn', 'cuda', 'cudnn', 'clnn', 'mkl', 'cudnn,mkl', 'mkl,cudnn'], default='nn')
parser.add_argument("-cudnn_autotune", action='store_true')
parser.add_argument("-seed", type=int, default=-1)

parser.add_argument("-content_layers", help="layers for content", default='relu4_2')
parser.add_argument("-style_layers", help="layers for style", default='relu1_1,relu2_1,relu3_1,relu4_1,relu5_1')

# Fast-Neural-Style options
parser.add_argument("-model", type=str, default='')
parser.add_argument("-median_filter", type=str, default=3)
parser.add_argument("-timing", type=str, default=0)
parser.add_argument("-input_image", type=str, default=1)
parser.add_argument("-use_cudnn", type=str, default=0)
parser.add_argument("-cudnn_benchmark", type=int, default=0)

params = parser.parse_args()


Image.MAX_IMAGE_PIXELS = 1000000000 # Support gigapixel images


def main(): 
    global params_string, tmp_dir
    params_string = parameters()

    try:
        os.makedirs(params.output_dir)
    except OSError: 
        pass
    try:
        os.makedirs(params.output_dir + '/tmp')
    except OSError: 
        pass
    tmp_dir = params.output_dir + '/tmp/'

    filename = params.output_image
    run = howto_run()
      
    h, w = get_dim()

    # Maybe crop the same relative amount from each side
    if params.crop_width == 0 or params.crop_height == 0:
       if w != h:
           s_size = float(min(h, w)) / float(max(h, w))
           s_size = int(s_size * float(params.crop))
           if h > w:
               crop_w, crop_h = s_size, params.crop
           elif w > h:
               crop_w, crop_h = params.crop, s_size
       else: 
         crop_w, crop_h = params.crop, params.crop
    else: 
       crop_w, crop_h = params.crop_width, params.crop_height

    first_run(run, params.output_image)
    
    # Process the frames one by one
    num = params.start_num + 1
    for i in range(params.num_frames - 1):
        print('Creating frame number ' + str(num))
        new_image = Image.open(params.output_dir + '/' + zeros(num-1, filename))
        new_image = crop(new_image, w - crop_w, h - crop_h)
        new_image.save(tmp_dir + zeros(num-1, filename))
        stylize(run, tmp_dir + zeros(num-1, filename), params.output_dir + '/' + zeros(num, filename)) 
        os.remove(tmp_dir + zeros(num-1, filename))
        num +=1

    # Final clean up and and correct frame zero
    os.rmdir(tmp_dir)
    if params.starting_image == '':
        image_zero = Image.open(params.output_dir + '/' + zeros(params.start_num, filename))
        image_one = Image.open(params.output_dir + '/' + zeros(params.start_num+1, filename))
        image_zero = image_zero.resize(image_one.size)
        os.remove(params.output_dir + '/' + zeros(params.start_num, filename))
        image_zero.save(params.output_dir + '/' + zeros(params.start_num, filename))

# Get target image dimensions        
def get_dim(): 
    image = Image.open(params.content_image).convert('RGB')
    return [int((float(params.image_size) / max(image.size))*x) for x in (image.height, image.width)]

# Maybe create the first frame
def first_run(run, output):
    if params.starting_image != '':
        first_image = Image.open(params.starting_image).convert('RGB')
        first_image.save(tmp_dir + zeros(params.start_num -1, output)) 
    else: 
        stylize(run, params.content_image, params.output_dir + '/' + zeros(params.start_num, output))
        first_image = Image.open(params.output_dir + '/' + zeros(params.start_num, output))
        first_image.save(tmp_dir + zeros(params.start_num, output)) 
     
# Run style transfer
def stylize(run, input, output): 
    if params.init_image != None: 
        content_param = ' -content_image ' + params.content_image + ' -init_image ' + input
    elif params.script == 'fast_neural_style.lua':
        content_param = ' -input_image ' + input
    else:
        content_param = ' -content_image ' + input
    cmd = run + content_param + ' -output_image ' + output + params_string
    if params.verbose:
        print(cmd)
    p = subprocess.Popen(cmd, shell=True)
    p.wait()
    return 

# Add zeros to output image name
def zeros(num, filename):
    if params.num_mode == 0: 
        filename = params.num_zeros[:-len(str(num))] + str(num) + "_" + filename
    elif params.num_mode == 1: 
        filename, ext = os.path.splitext(filename)
        filename = filename + "_" + params.num_zeros[:-len(str(num))] + str(num) + ext
    return filename 
 
# Crop the image based on specified values 
def crop(image, crop_w, crop_h):
    w, h = image.size 
    crop_dim = (w//2 - crop_w//2, h//2 - crop_h//2, w//2 + crop_w//2, h//2 + crop_h//2)
    return image.crop(crop_dim)

# Figure out how to run the specified style transfer script
def howto_run():
    scriptname, script_ext = os.path.splitext(params.script)
    if script_ext == '.py': 
        from sys import version_info
        if version_info[0] < 3:
            run = 'python '
        else:  
            run = 'python3 '
    elif script_ext == '.lua':
        run = 'th '
    return run  + params.script

# Remove neural-zoom parameters and ensure that the appropriate style transfer parameters are used
def parameters(): 
    fast_ns_list = ['model', 'median_filter', 'timing', 'use_cudnn', 'cudnn_benchmark']
    remove_list = ['output_dir', 'num_zeros', 'num_frames', 'script', 'crop', 'crop_width', 'crop_height', 'content_image', 'init_image', 'output_image', 'starting_image', 'start_num', 'num_mode', 'input_image', 'verbose']
    if not params.normalize_gradients:
       remove_list.append('normalize_gradients')
    if not params.normalize_gradients:
       remove_list.append('cudnn_autotune')
    if params.multigpu_strategy == '':
       remove_list.append('multigpu_strategy')
    if params.multidevice_strategy == '':
       remove_list.append('multidevice_strategy')
    if params.proto_file == '':
       remove_list.append('proto_file')
    if params.original_colors == 0:
       remove_list.append('original_colors')
    if not params.disable_check:
       remove_list.append('disable_check')
    params_dict = dict(vars(params))
    new_string = ''

    if params.script != 'fast_neural_style.lua':
        for arg, value in params_dict.items():
            if arg not in remove_list and arg not in fast_ns_list and value != None:
                new_string = new_string + str("-" + arg) + " " + str(value) + " " 
    elif params.script == 'fast_neural_style.lua': 
        params.content_image = params.input_image
        for arg, value in params_dict.items():
            if arg in fast_ns_list and arg not in remove_list:
                if value != None or value !=0:
                    new_string = new_string + str("-" + arg) + " " + str(value) + " " 
    return ' ' + new_string


if __name__ == "__main__":
    main()
