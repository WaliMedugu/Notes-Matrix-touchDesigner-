# 3D Network Topology HUD - Gesture Controlled Hierarchy

This project implements an interactive **3D Network Topology HUD / Node-Link Diagram** that lets you navigate through hierarchical knowledge layers using real-time **MediaPipe Hand-Gesture Tracking**.

The system is configured to only render the **current parent node** and its **immediate children (kids)**. To explore further, you select a child and physically "zoom in" to open it. Exiting to the parent layer requires a "zoom out" gesture.

---

## 🎨 Design Systems & Aesthetic Rules
- **Monochromatic Theme**: All child nodes, connection links, HUD labels, text indicators, camera background overlays, and secondary fingers are rendered in a sleek monochromatic spectrum (whites, grays, and blacks).
- **Cyan Highlights Accent**:
  - The **current parent node** at the center of the hierarchy is colored in glowing **Cyan** (`#00f0ff`).
  - The **command fingers** (Index finger tip and Thumb tip) used to trigger gestures are highlighted in glowing **Cyan**.
- **Background**: Integrated desaturated grayscale camera feed, centered and layered behind the HUD geometry.

---

## 🖐️ Hand Gesture & Navigation Controls
The application maps mirrored coordinates from your webcam in real-time.

1. **Pointing / Selection (Right Hand Only)**: 
   - Move your **Right Hand** Index Finger near any of the orbiting child nodes.
   - The system automatically selects the nearest node to your right index fingertip and projects a targeting box on it. Node selection is strictly mapped to the right hand.
2. **Zoom In / Enter Node (Right Hand Pinch)**:
   - Select a node by pointing at it with your right hand, then **pinch your right thumb and index finger together** (pinch ratio < 0.42).
   - This hides the parent, moves the selected node to the center (becoming the new parent), and expands its children.
3. **Zoom Out / Exit Node (Left Hand Pinch)**:
   - **Pinch your left thumb and index finger together** (pinch ratio < 0.42).
   - This exits the current level (acting as a Back button), bringing the previous parent node back to the center of the viewport.
4. **3D Rotation (5-Finger Pinch / Fist)**:
   - **Pinch all 5 fingers together** (make a fist) on **either hand** to unlock and rotate the 3D spherical space.
   - This gesture overrides all zoom controls and locks the selector until the fist is released (fingers opened), preventing accidental triggers.

### 🎨 Special Node Outlines
* **Leaf Nodes**: Sibling nodes that have no children (e.g. `Biological Hardware` or terminal sub-leaves) are rendered with a **glowing Cyan outline and transparent fill** instead of white, indicating they are terminal path points.

### 🔒 Scale-Invariant Ratio Engine & Gesture Lockout
* **Hand-Scale Normalization**: To prevent depth issues (where moving your hand closer or further from the camera triggers actions falsely), the gesture parser computes the ratio of thumb-to-index distance divided by the physical hand scale (distance from the wrist to the middle finger base).
* **Double-Trigger Prevention**: Once a zoom action is triggered, it is locked out until that hand returns to a **neutral pointing shape** (ratio between `0.65` and `1.35`). This prevents continuous zooming when holding a gesture.

### 🚫 Interactive Input Block
* Mouse clicks, mouse dragging to rotate, double clicks, scroll wheel events, and keyboard fallbacks are fully disabled in the HUD to guarantee pure gesture-driven operation.

---

## 📁 Directory Structure
```
thoughts matrix v2/
│
├── index.html             # High-performance 2D Canvas Web View (MediaPipe + Custom 3D Projection)
├── generate_topology.py   # Python script to build the entire network in TouchDesigner
├── serve.py               # Local Python web server (adds CORS headers on port 8001)
├── run.bat                # Launcher script to boot serve.py and launch index.html on port 8001
└── README.md              # Documentation and guide
```

---

## 🛠️ Step-by-Step Execution Guide

### Option A: Running the Web View (Recommended for Instant Testing)
1. Double-click the **`run.bat`** file in `c:\Code\Visuals\thoughts matrix v2\`.
2. A terminal window will open to start the local Python web server on port `8001`.
3. Your default web browser will automatically open to `http://localhost:8001/`.
4. Grant camera permissions. The system will load the MediaPipe tracking libraries from CDN and start immediately!

### Option B: Running inside TouchDesigner
1. Open TouchDesigner.
2. Press **`Alt + T`** to open the Text Port (or create a new **Text DAT** in the workspace).
3. Open the file **`generate_topology.py`** and copy its entire contents.
4. Paste the script into the TouchDesigner Text Port or Text DAT.
5. Right-click the Text DAT and select **Run Script** (or press **`Ctrl + R`** in the Text Port).
6. The script will automatically create a Container COMP called `/project1/NetworkTopology` containing the entire node hierarchy layout, webcam device reader, scripts, and compositing chains.
7. Open the output node `/project1/NetworkTopology/out_final` or display the container's panel to interact!
