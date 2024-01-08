# metaonnx

metaonnx部署通用框架

## 1、安装最新版 meta-cv

    pip install meta-cv

## 2、安装最新版 meta-onnx

    pip install meta-onnx

## 3、目标检测示例（参考[detection_demo.py](detection_demo.py)代码）

    import platform, cv2
    import metaonnx as mo

    Detection = mo.DetectionOnnx

    y = Detection(model_path='models/yolov8m.onnx',
                  input_width=640,
                  input_height=480,
                  confidence_thresh=0.5,
                  nms_thresh=0.3,
                  class_names=classnames)

    img = cv2.imread('models/bus.jpg')
    _dets, _scores, _labels = y.predict(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), use_preprocess=True)
    
    # 显示
    y.show(img, _dets, _scores, _labels)
    cv2.imwrite("models/bus.png", img)

## 4、实例分割示例（参考[segment_demo.py](segment_demo.py)代码）

    import platform, cv2
    import metaonnx as mo
    
    Segment = mo.SegmentOnnx

    y = Segment(model_path='models/yolov8m-seg.rknn',
                input_width=640,
                input_height=480,
                confidence_thresh=0.5,
                nms_thresh=0.3,
                class_names=classnames)
    
    img = cv2.imread('models/bus.jpg')
    _dets, _scores, _labels = y.predict(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), use_preprocess=True)
    
    # 显示
    y.show(img, _dets, _scores, _labels)
    cv2.imwrite("models/bus.png", img)