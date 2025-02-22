
<!--
waggle_topic=/plugins_and_code
-->

## Cloud Coverage Estimator

The cloud coverage estimator plugin reports percentage of cloud coverage over an image that the top camera in the waggle node produces. It reports the cloud coverage in percentage every 5 minutes. With the percentage of cloud coverage estimation result, the sampled images and processed binary images (cloud: true, sky: false) are sent when its configuration requires to sample the results.

This approach benchmarked a paper of [Dev et al.] (https://github.com/waggle-sensor/summer2019/tree/master/Goeum-Cha/segmentation/v1#references). The research proposed a robust method to segment cloud in the given image using statistical methods. In this plugin, two datasets are used: Hybrid Thresholding Algorithm (HYTA) Database and SWIMSEG. The datasets provide real sky images and ground truth images (cloud: white, sky: black).

There are adjustable parameters when desired,
* `detection_interval` to control estimation interval in second, default is 300 (60x5) seconds
* `sampling_interval` to control if the sampled images need to be sent or not; if the value is negative, it does not sample image -- default is `-1`, which is false

## Architecture and Example Results
Detail of the cloud coverage estimator architecture is described in [here](https://github.com/waggle-sensor/summer2019/tree/master/Goeum-Cha/segmentation/v1#architecture), and example results are shown in [here](https://github.com/waggle-sensor/summer2019/tree/master/Goeum-Cha/segmentation/v1#re-evaluated-result).

### Sensor values
The values are packed into a string, so it will look like this:
```
data time, node id, controlling device, sensor name, parameter name, raw data, human readable (converted) data
2019/06/11 16:49:45,001e06117b41,nc,image,cloud_coverage,NA,"35.45"
```

### Calculation Time and Memory Usage:
#### XU4:
```
feature generator elapsed in 5.446307
predictor elapsed in 7.075058
soft threshold elapsed in 88.255956
threshold elapsed in 0.288857


Doing nothing:
Mem[413M/1.95G]

Running cloud coverage estimator:
Mem[1.18G/1.95G]
```

#### TX2:
```
feature generator elapsed 0.810745
prediction elasped 1.059503
soft threshold elapsed 17.324739
estimation elapsed 0.032877


Doing nothing:
Mem[611M/7.68G]

Runnung cloud coverage estimator:
Mem[1.38G/7.68G]
```


### Log

#### Jul 11, 2019
#### sensor_id: 0x3002 (12290)
cloud_coverage version 1: don't know what will be the sensor id, so I just put the next number of image-detector(0x3000) and spl(0x3001).
