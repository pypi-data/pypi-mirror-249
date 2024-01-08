# metarknn

metarknn部署通用框架

## 1、安装最新版 meta-cv

    pip install meta-cv

## 2、安装最新版 meta-rknn

    pip install meta-rknn

## 3、目标检测示例（参考[detection_demo.py](detection_demo.py)代码）

    import platform, cv2
    import metarknn as mr

    Detection = mr.DetectionRKNN

    y = Detection(model_path='models/yolov8m.rknn',
                  input_width=640,
                  input_height=480,
                  confidence_thresh=0.5,
                  nms_thresh=0.3,
                  class_names=classnames,
                  device_id=0)

    # 如需本地运行，需调用下面一句进行模型转换并加载，板端无需运行
    if platform.machine() == 'x86_64':
        y.convert_and_load(quantize=False,  # 是否int8量化
                           dataset='dataset.txt',  # 量化使用图片路径文件
                           is_hybrid=True)  # 是否进行混合量化
    
    img = cv2.imread('models/bus.jpg')
    _dets, _scores, _labels = y.predict(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), use_preprocess=True)
    
    # 显示
    y.show(img, _dets, _scores, _labels)
    cv2.imwrite("models/bus.png", img)

## 4、实例分割示例（参考[segment_demo.py](segment_demo.py)代码）

    import platform, cv2
    import metarknn as mr

    Segment = mr.SegmentRKNN

    y = Segment(model_path='models/yolov8m-seg.rknn',
                input_width=640,
                input_height=480,
                confidence_thresh=0.5,
                nms_thresh=0.3,
                class_names=classnames,
                device_id=0)

    # 如需本地运行，需调用下面一句进行模型转换并加载，板端无需运行
    if platform.machine() == 'x86_64':
        y.convert_and_load(quantize=False,  # 是否int8量化
                           dataset='dataset.txt',  # 量化使用图片路径文件
                           is_hybrid=True)  # 是否进行混合量化
    
    img = cv2.imread('models/bus.jpg')
    _dets, _scores, _labels = y.predict(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), use_preprocess=True)
    
    # 显示
    y.show(img, _dets, _scores, _labels)
    cv2.imwrite("models/bus.png", img)

## 5、模型转换与量化（本地运行）

    import metarknn as mr
    from mr.quantization import Quantization

    q = Quantization(model_path，    # onnx模型路径
                     dataset,   # dataset文件路径
                     output_names=["output0", "output1"])   # 定义模型输出层
    if is_hybrid:   # 是否混合量化
        self.model = q.hybrid_convert()
    else:   # 非混合量化（是否int8量化）
        self.model = q.convert(quantize)
