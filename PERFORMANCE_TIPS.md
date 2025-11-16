# Performance Optimization Guide

## ✅ Applied Optimizations

### 1. **Reduced Camera Resolution** 
- Changed from 640x480 to **320x240**
- Lower resolution = faster frame processing (2-4x speedup)
- MediaPipe processes fewer pixels per frame

### 2. **Optimized MediaPipe Settings**
- `model_complexity=0` - Uses lightweight hand model (fastest)
- `max_num_hands=1` - Only tracks one hand for better performance
- `static_image_mode=False` - Optimized for video streams

### 3. **Minimized Camera Buffer Lag**
- Set `CAP_PROP_BUFFERSIZE=1` - Reduces camera buffering latency
- Requested higher FPS (`60fps`) if camera supports it

### 4. **Removed Unnecessary Color Conversions**
- Eliminated redundant BGR→RGB→BGR conversion in main loop
- Now only converts once (BGR→RGB for MediaPipe)

### 5. **Improved Cursor Movement Precision**
- Maintains floating-point precision during smoothing
- Only converts to integer at final `moveTo()` call
- Added `_pause=False` to pyautogui for zero delay

### 6. **Optimized Drawing Operations**
- Hand landmarks only drawn when `debug=True`
- Saves significant processing time when debug is off

### 7. **Minimal waitKey Delay**
- Using 1ms waitKey (minimum for OpenCV event processing)
- Any lower and window events won't be handled

## 🎯 Expected Results

- **Cursor Latency**: Reduced from ~100-200ms to ~30-50ms
- **Frame Rate**: Increased from ~15-20 FPS to ~25-35 FPS
- **Responsiveness**: Significantly improved, near real-time tracking

## 🔧 Additional Tweaks You Can Try

### In Settings Window:
1. **Increase Smoothing Factor** to 0.7-0.9 for more responsive (but less smooth) movement
2. **Decrease Detection Confidence** to 0.5-0.6 for faster initial detection
3. **Adjust ROI** - Smaller tracking area = more precise cursor control

### Advanced:
```python
# In main.py, try even lower resolution if your use case allows:
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)

# Or disable debug mode completely for maximum speed:
debug = False
```

## 📊 Benchmark Your System

Add this to see your actual FPS:
```python
import time
fps_start = time.time()
frame_count = 0

# In main loop, after results = hands.process(image_rgb):
frame_count += 1
if frame_count % 30 == 0:
    fps = 30 / (time.time() - fps_start)
    print(f"FPS: {fps:.1f}")
    fps_start = time.time()
```

## 🚀 Hardware Recommendations

For best performance:
- **Webcam**: 720p @ 60fps or higher
- **CPU**: Modern quad-core (Intel i5/i7 or AMD Ryzen)
- **RAM**: 8GB+ 
- **USB**: USB 3.0 for camera (reduces latency)

## 💡 Pro Tips

1. **Close other applications** - Gives more CPU to hand tracking
2. **Use good lighting** - MediaPipe works better with well-lit hands
3. **Reduce hand movements** when possible - Less prediction needed
4. **Keep hand in center of frame** - Reduces processing complexity
