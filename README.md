# neural-zoom

Neural-Zoom works by cropping the output from a style transfer script, and then using the cropped output as either a content image, or an initialization image for the next frame. 

If you are looking for the old version of Neural-Zoom, it can be found [here](https://github.com/ProGamerGov/Neural-Zoom-Legacy). 


### Different Crop (Zoom) Values 

By changing the crop value, you can control the "speed" at which the zoom will be.

<div align="center">
<img src="https://raw.githubusercontent.com/ProGamerGov/Neural-Zoom/master/examples/inputs/ns_tubingen_starry_crop_64.gif" height="175px">
<img src="https://raw.githubusercontent.com/ProGamerGov/Neural-Zoom/master/examples/inputs/ns_tubingen_starry_crop_128.gif" height="175px">
<img src="https://raw.githubusercontent.com/ProGamerGov/Neural-Zoom/master/examples/inputs/ns_tubingen_starry_crop_256.gif" height="175px">
</div>

### Different X And Y Axis Crop Values 

You can control the "zoom" for the x axis and y axis separately.

From the left: "The Scream", and "The Starry Night" + "Picasso Self-Portrait"

<div align="center">
<img src="https://raw.githubusercontent.com/ProGamerGov/Neural-Zoom/master/examples/inputs/pt_tubingen_scream_crop_32-256.gif" height="250px">
<img src="https://raw.githubusercontent.com/ProGamerGov/Neural-Zoom/master/examples/inputs/ns_tubingen_starry_picasso_crop_16-128.gif" height="250px">
</div>

 
### Parameters:

In addition to all the parameters from your chosen style transfer script, neural-zoom has it's own parameters: 

**Basic Options**:
* `-script`: Path to the Lua or Python style transfer script. Currently [Neural-Style](https://github.com/jcjohnson/neural-style), [Fast-Neural-Style](https://github.com/jcjohnson/fast-neural-style), and [Neural-Style-PT](https://github.com/ProGamerGov/neural-style-pt) are supported. 
* `-num_frames`: The total number of frames to create. Default is `30`.

**Zoom Options**:
* `-crop`: How much to crop each frame from all sides. Default is `64`. If both the `-crop_height` and `-crop_width` parameters are greater than zero, this parameter will be ignored.
* `-crop_width`: How much to crop the left and right sides of each frame.
* `-crop_height`: How much to crop the top and bottom sides of each frame.

**Starting Options**:
* `-starting_image`: Optionally skip creating frame zero, and use your own image instead. 
* `-start_num`: The number to start counting from for frame names. Default is `0`.

**Output options**:
* `-num_zeros`: How many zeros to use for the number portion of each frame name. Default is `0000`.
* `-num_mode`: Whether to use trailing or leading numbers in frame names. If you set this to `0`, leading numbers will be used instead of trailing numbers.
* `-output_dir`: Name of the output image directory. Default is `output_dir`.
* `-verbose`: If this flag is present, then the full set of style transfer parameters used, will be printed for each frame.

## Setup

* Something to convert your frames into the desired media format, like FFMPEG, or Imagemagick.

* A supported style transfer project.  

You can download Neural-Zoom directly to a style transfer project directory, with: 

```
wget -c https://raw.githubusercontent.com/ProGamerGov/Neural-Zoom/master/neural_zoom.py
```

## Usage 

The Neural-Zoom specific parameters will remain the same with each style transfer script, but each script will have it's own different required parameters. 

Below are some basic examples of how to use Neural-Zoom (with either Python 2.7 or Python 3):

**Neural-Style:**

```
python neural_zoom.py -script neural_style.lua -style_image <image.jpg> -content_image <image.jpg> -model_file models/VGG_ILSVRC_19_layers.caffemodel -proto_file models/VGG_ILSVRC_19_layers_deploy.prototxt
```

**Fast-Neural-Style:**

```
neural_zoom.py -script fast_neural_style.lua -model <model.t7> -input_image <image.jpg>
```

**Neural-Style-PT:**

```
python neural_zoom.py -script neural_style.py -style_image <image.jpg> -content_image <image.jpg> -model_file models/models/vgg19-d01eb7cb.pth
```

From the left, the style transfer project used is Neural-Style, Fast-Neural-Style, and Neural-Style-PT.

<div align="center">
<img src="https://raw.githubusercontent.com/ProGamerGov/Neural-Zoom/master/examples/inputs/ns_tubingen_scream_seated_picasso.gif" height="175px">
<img src="https://raw.githubusercontent.com/ProGamerGov/Neural-Zoom/master/examples/inputs/fast_chicago_starry.gif" height="175px">
<img src="https://raw.githubusercontent.com/ProGamerGov/Neural-Zoom/master/examples/inputs/pt_tubingen_seated-nude.gif" height="175px">
</div>
