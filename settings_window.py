import tkinter as tk
from tkinter import ttk
import threading

class SettingsWindow:
    def __init__(self):
        self.window = None
        self.thread = None
        
        # Default settings - these will be accessible from main.py
        self.smoothing_factor = 0.2
        self.fist_cooldown = 1.0
        self.pinch_threshold = 0.05
        self.min_detection_confidence = 0.7
        self.min_tracking_confidence = 0.5
        self.roi_x_min = 0.5
        self.roi_x_max = 0.9
        self.roi_y_min = 0.5
        self.roi_y_max = 0.9
        self.scroll_speed = 3
        
        # Callbacks for when settings change
        self.on_settings_changed = None
        
    def create_window(self):
        """Create the settings window in a separate thread."""
        self.thread = threading.Thread(target=self._run_window, daemon=True)
        self.thread.start()
    
    def _run_window(self):
        """Run the tkinter window in a separate thread."""
        self.window = tk.Tk()
        self.window.title("Gesture Control Settings")
        self.window.geometry("650x1050")
        self.window.resizable(False, False)
        
        # Make window stay on top
        self.window.attributes('-topmost', True)
        
        # Create main frame with padding
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        row = 0
        
        # Title
        title = ttk.Label(main_frame, text="Gesture Control Settings", 
                         font=('Arial', 14, 'bold'))
        title.grid(row=row, column=0, columnspan=2, pady=(0, 15))
        row += 1
        
        # === CURSOR SETTINGS ===
        ttk.Separator(main_frame, orient='horizontal').grid(row=row, column=0, 
                                                            columnspan=2, sticky='ew', pady=5)
        row += 1
        
        cursor_label = ttk.Label(main_frame, text="Cursor Settings", 
                                font=('Arial', 11, 'bold'))
        cursor_label.grid(row=row, column=0, columnspan=2, pady=(5, 10))
        row += 1
        
        # Smoothing Factor
        self._create_slider(main_frame, row, "Smoothing Factor:", 
                           self.smoothing_factor, 0.0, 1.0, 0.01,
                           lambda v: setattr(self, 'smoothing_factor', v),
                           "Higher = more responsive, Lower = smoother")
        row += 2
        
        # ROI X Min
        self._create_slider(main_frame, row, "ROI X Min:", 
                           self.roi_x_min, 0.0, 0.8, 0.05,
                           lambda v: setattr(self, 'roi_x_min', v),
                           "Left edge of tracking area")
        row += 2
        
        # ROI X Max
        self._create_slider(main_frame, row, "ROI X Max:", 
                           self.roi_x_max, 0.2, 1.0, 0.05,
                           lambda v: setattr(self, 'roi_x_max', v),
                           "Right edge of tracking area")
        row += 2
        
        # ROI Y Min
        self._create_slider(main_frame, row, "ROI Y Min:", 
                           self.roi_y_min, 0.0, 0.8, 0.05,
                           lambda v: setattr(self, 'roi_y_min', v),
                           "Top edge of tracking area")
        row += 2
        
        # ROI Y Max
        self._create_slider(main_frame, row, "ROI Y Max:", 
                           self.roi_y_max, 0.2, 1.0, 0.05,
                           lambda v: setattr(self, 'roi_y_max', v),
                           "Bottom edge of tracking area")
        row += 2
        
        # === GESTURE SETTINGS ===
        ttk.Separator(main_frame, orient='horizontal').grid(row=row, column=0, 
                                                            columnspan=2, sticky='ew', pady=5)
        row += 1
        
        gesture_label = ttk.Label(main_frame, text="Gesture Settings", 
                                 font=('Arial', 11, 'bold'))
        gesture_label.grid(row=row, column=0, columnspan=2, pady=(5, 10))
        row += 1
        
        # Pinch Threshold
        self._create_slider(main_frame, row, "Pinch Threshold:", 
                           self.pinch_threshold, 0.01, 0.15, 0.01,
                           lambda v: setattr(self, 'pinch_threshold', v),
                           "Distance to trigger pinch (left click)")
        row += 2
        
        # Fist Cooldown
        self._create_slider(main_frame, row, "Fist Cooldown (s):", 
                           self.fist_cooldown, 0.1, 3.0, 0.1,
                           lambda v: setattr(self, 'fist_cooldown', v),
                           "Time between right-click actions")
        row += 2
        
        # Scroll Speed
        self._create_slider(main_frame, row, "Scroll Speed:", 
                           self.scroll_speed, 1, 10, 1,
                           lambda v: setattr(self, 'scroll_speed', int(v)),
                           "Speed of scroll gestures")
        row += 2
        
        # === DETECTION SETTINGS ===
        ttk.Separator(main_frame, orient='horizontal').grid(row=row, column=0, 
                                                            columnspan=2, sticky='ew', pady=5)
        row += 1
        
        detection_label = ttk.Label(main_frame, text="Hand Detection", 
                                   font=('Arial', 11, 'bold'))
        detection_label.grid(row=row, column=0, columnspan=2, pady=(5, 10))
        row += 1
        
        # Min Detection Confidence
        self._create_slider(main_frame, row, "Detection Confidence:", 
                           self.min_detection_confidence, 0.3, 1.0, 0.05,
                           lambda v: setattr(self, 'min_detection_confidence', v),
                           "Confidence to detect hand initially")
        row += 2
        
        # Min Tracking Confidence
        self._create_slider(main_frame, row, "Tracking Confidence:", 
                           self.min_tracking_confidence, 0.3, 1.0, 0.05,
                           lambda v: setattr(self, 'min_tracking_confidence', v),
                           "Confidence to track hand continuously")
        row += 2
        
        # === BUTTONS ===
        ttk.Separator(main_frame, orient='horizontal').grid(row=row, column=0, 
                                                            columnspan=2, sticky='ew', pady=10)
        row += 1
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=10)
        
        reset_btn = ttk.Button(button_frame, text="Reset to Defaults", 
                              command=self._reset_defaults)
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        # Start the GUI loop
        self.window.mainloop()
    
    def _create_slider(self, parent, row, label_text, default_value, 
                      min_val, max_val, resolution, callback, description=""):
        """Helper to create a labeled slider with value display."""
        # Label
        label = ttk.Label(parent, text=label_text)
        label.grid(row=row, column=0, sticky=tk.W, pady=(5, 0))
        
        # Value display
        value_var = tk.StringVar(value=f"{default_value:.2f}")
        value_label = ttk.Label(parent, textvariable=value_var, 
                               font=('Arial', 9, 'bold'))
        value_label.grid(row=row, column=1, sticky=tk.E, pady=(5, 0))
        
        # Slider
        slider = ttk.Scale(parent, from_=min_val, to=max_val, 
                          orient=tk.HORIZONTAL, length=400)
        slider.set(default_value)
        slider.grid(row=row+1, column=0, columnspan=2, sticky=(tk.W, tk.E), 
                   pady=(0, 2))
        
        def on_change(val):
            float_val = float(val)
            # Round to resolution
            rounded_val = round(float_val / resolution) * resolution
            value_var.set(f"{rounded_val:.2f}" if resolution < 1 else f"{int(rounded_val)}")
            callback(rounded_val)
            if self.on_settings_changed:
                self.on_settings_changed()
        
        slider.configure(command=on_change)
        
        # Description
        if description:
            desc_label = ttk.Label(parent, text=description, 
                                  font=('Arial', 8), foreground='gray')
            desc_label.grid(row=row+2, column=0, columnspan=2, 
                           sticky=tk.W, pady=(0, 5))
        
        return slider
    
    def _reset_defaults(self):
        """Reset all settings to default values."""
        self.smoothing_factor = 0.2
        self.fist_cooldown = 1.0
        self.pinch_threshold = 0.05
        self.min_detection_confidence = 0.7
        self.min_tracking_confidence = 0.5
        self.roi_x_min = 0.5
        self.roi_x_max = 0.9
        self.roi_y_min = 0.5
        self.roi_y_max = 0.9
        self.scroll_speed = 3
        
        # Recreate window to show default values
        if self.window:
            self.window.destroy()
        self.create_window()
        
        if self.on_settings_changed:
            self.on_settings_changed()
    
    def get_settings(self):
        """Return a dictionary of current settings."""
        return {
            'smoothing_factor': self.smoothing_factor,
            'fist_cooldown': self.fist_cooldown,
            'pinch_threshold': self.pinch_threshold,
            'min_detection_confidence': self.min_detection_confidence,
            'min_tracking_confidence': self.min_tracking_confidence,
            'roi_x_min': self.roi_x_min,
            'roi_x_max': self.roi_x_max,
            'roi_y_min': self.roi_y_min,
            'roi_y_max': self.roi_y_max,
            'scroll_speed': self.scroll_speed,
        }
