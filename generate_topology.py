# ==============================================================================
# Procedural 3D Network Topology HUD Builder for TouchDesigner
# ==============================================================================
# This script automates the creation of a high-fidelity interactive visualizer
# inside TouchDesigner, implementing a 3D Hierarchical Node-Link Diagram.
#
# Interaction Logic:
# - Displays only the current parent node (cyan) and its children (monochromatic).
# - Selects the nearest child node to the index finger (draws a bounding box).
# - SPREAD gesture (thumb and index spread wide) zooms into the selected node.
# - PINCH gesture (thumb and index pinch close) zooms out to the parent's parent.
# - Monochromatic theme, grayscale webcam background feed.
# - Fallback: Mouse movement for pointing, scroll wheel/keys for zoom in/out.
#
# How to run:
# 1. Open TouchDesigner.
# 2. Press Alt+T to open the Text Port, or create a Text DAT.
# 3. Paste this script into the Text Port or Text DAT.
# 4. Run the script (Ctrl+R).
# 5. Look at '/project1/NetworkTopology/out_final' to view the final result!
# ==============================================================================

import json

def build_network_topology():
    project_path = '/project1'
    comp_name = 'NetworkTopology'
    comp_path = f'{project_path}/{comp_name}'
    
    # 1. Clean up existing COMP
    existing = op(comp_path)
    if existing:
        print(f"[NetworkTopology] Destroying existing {comp_path}...")
        existing.destroy()
        
    parent_comp = op(project_path) or op('/')
    if not parent_comp:
        print("[ERROR] Could not find /project1 or root path.")
        return
        
    # 2. Create Container COMP (720x1280 vertical format)
    hud = parent_comp.create(containerCOMP, comp_name)
    hud.nodeX = 200
    hud.nodeY = 200
    hud.par.w = 720
    hud.par.h = 1280
    print(f"[NetworkTopology] Created Container COMP: {hud.path}")
    
    # 3. Create Panel CHOP (for mouse fallback)
    panel = hud.create(panelCHOP, 'panel1')
    panel.nodeX = 100
    panel.nodeY = 100
    panel.par.select = 'u v select'
    
    # 4. Create Select CHOP for MediaPipe Hand Tracking
    select_hand = hud.create(selectCHOP, 'select_hand')
    select_hand.nodeX = 100
    select_hand.nodeY = 220
    
    # Search for an existing MediaPipe CHOP in the workspace
    mp_chop = None
    for c in op('/').findChildren(type=chopOP):
        if ('hand_0' in c.name or 'hand_tracking' in c.path) and not c.path.startswith(hud.path):
            mp_chop = c
            break
            
    if mp_chop:
        print(f"[NetworkTopology] Found MediaPipe hand tracker: {mp_chop.path}")
        select_hand.par.chops = mp_chop.path
        select_hand.par.chans = "hand_0/joint_* hand_1/joint_* hand_0/left_right hand_1/left_right hand_0/side hand_1/side hand_0/handedness hand_1/handedness"
    else:
        print("[NetworkTopology] MediaPipe hand tracker not found. Running with mouse pointer fallback.")
        
    # 5. Create Text DAT storing the JSON hierarchy
    tree_data_dat = hud.create(textDAT, 'tree_data')
    tree_data_dat.nodeX = 100
    tree_data_dat.nodeY = 400
    
    hierarchy = {
        "name": "Thoughts Matrix",
        "desc": "Root level coordinates of the cognitive database. Tracks connections between AI, human expression, and information tools.",
        "children": [
            {
                "name": "Artificial Intelligence",
                "desc": "Computational models simulating human cognition, pattern matching, neural processing, and dimensional representation.",
                "children": [
                    {
                        "name": "Neural Networks",
                        "desc": "Hierarchical interconnected artificial neurons optimizing high-dimensional mathematical functions via backpropagation.",
                        "children": [
                            {"name": "Perceptrons", "desc": "The foundational single-layer binary classifiers proposed by Frank Rosenblatt in 1957."},
                            {"name": "Embeddings", "desc": "Low-dimensional vector representations mapping semantic properties of complex symbols."},
                            {"name": "Transformers", "desc": "Attention-based sequence transduction architectures revolutionizing NLP and deep learning."}
                        ]
                    },
                    {
                        "name": "Computer Vision",
                        "desc": "Algorithmic extraction of structural, volumetric, and semantic context from raster image data fields.",
                        "children": [
                            {"name": "ConvNets", "desc": "Translation-invariant spatial feature extraction pipelines using mathematical convolutions."},
                            {"name": "NeRFs", "desc": "Neural Radiance Fields representing continuous 3D scenes via neural network volume rendering."},
                            {"name": "Gaussian Splatting", "desc": "Real-time 3D reconstruction using rasterization of anisotropic 3D Gaussians."}
                        ]
                    },
                    {
                        "name": "Cognitive Science",
                        "desc": "Interdisciplinary study of mind, intelligence, learning, and systemic mental structures.",
                        "children": [
                            {"name": "Mental Models", "desc": "Internal cognitive representations of external realities used to make decisions."},
                            {"name": "Synaptic Plasticity", "desc": "The biochemical capacity of neural connections to strengthen or weaken over time."},
                            {"name": "Neural Darwinism", "desc": "Selectionist theory of brain development mapping neural group selections."}
                        ]
                    },
                    {
                        "name": "Natural Language",
                        "desc": "Processing and generation of human-readable symbols, syntactic grammar, and semantic vectors.",
                        "children": [
                            {"name": "Tokenization", "desc": "Deconstructing text streams into discrete semantic sub-word units."},
                            {"name": "Vector Space", "desc": "High-dimensional coordinate structures where distance models semantic similarity."}
                        ]
                    }
                ]
            },
            {
                "name": "Human Expression",
                "desc": "Systemic methods by which humans encode, transmit, and record subjective experience, movement, and aesthetic language.",
                "children": [
                    {
                        "name": "Notation Systems",
                        "desc": "Symbolic spatial geometries designed to preserve temporal kinetic and sonic performance.",
                        "children": [
                            {"name": "Dance Writing", "desc": "Formal graphic notation systems encoding bodily kinetics, posture, and spatial pathways."},
                            {"name": "Sheet Music", "desc": "Five-line staff system representing pitch, duration, and dynamics of acoustic sound."},
                            {"name": "Labanotation", "desc": "Rudolf Laban's detailed abstract taxonomy mapping human motion parameters."}
                        ]
                    },
                    {
                        "name": "Generative Art",
                        "desc": "Autonomous, rule-based systems producing aesthetic outcomes with varying degrees of systemic entropy.",
                        "children": [
                            {"name": "L-Systems", "desc": "Parallel string-rewriting grammars modeling biological growth patterns and fractals."},
                            {"name": "Fractals", "desc": "Infinite self-similar mathematical topologies exhibiting fractional Hausdorff dimensions."},
                            {"name": "Cellular Automata", "desc": "Discrete computational cells evolving on grids based on local neighborhood states."}
                        ]
                    },
                    {
                        "name": "Media Theory",
                        "desc": "Historical and philosophical analysis of technological extension channels and their cognitive impacts.",
                        "children": [
                            {"name": "Understanding Media", "desc": "Marshall McLuhan's study mapping the psychological changes caused by technological mediums."},
                            {"name": "Gutenberg Galaxy", "desc": "Analyzing how movable print type restructured human sensory ratios and typographic culture."},
                            {"name": "Medium is Massage", "desc": "Highlighting how the sensory format of a medium shapes human association patterns."}
                        ]
                    }
                ]
            },
            {
                "name": "Information Systems",
                "desc": "Technological infrastructures designed to store, retrieve, link, and display knowledge structures asynchronously.",
                "children": [
                    {
                        "name": "Hypermedia Vision",
                        "desc": "Pioneering concepts of non-linear text architectures, associative search, and global document indices.",
                        "children": [
                            {"name": "Memex", "desc": "Vannevar Bush's conceptual desktop machine linking microfilms via associative trails."},
                            {"name": "Project Xanadu", "desc": "Ted Nelson's vision of two-way linked parallel documents with transclusion support."},
                            {"name": "World Wide Web", "desc": "Tim Berners-Lee's global decentralized hypertext platform built on HTTP and HTML."}
                        ]
                    },
                    {
                        "name": "Personal Computing",
                        "desc": "Empowering individual agency via interactive graphic environments and local object-oriented architectures.",
                        "children": [
                            {"name": "Dynabook", "desc": "Alan Kay's concept of a portable, interactive educational computer for children."},
                            {"name": "Alto GUI", "desc": "Xerox PARC's desktop metaphor integrating overlapping windows, icons, and mouse pointer."},
                            {"name": "Smalltalk", "desc": "Pioneering dynamic object-oriented programming language and graphical environment."}
                        ]
                    },
                    {
                        "name": "Cybernetics",
                        "desc": "The study of control, feedback, communications, and regulation loops in complex systems.",
                        "children": [
                            {"name": "Feedback Loops", "desc": "Causal loops where system output is fed back to regulate subsequent system behavior."},
                            {"name": "Homeostasis", "desc": "Dynamic equilibrium maintained by regulatory feedback systems within live systems."},
                            {"name": "System Dynamics", "desc": "Methodology mapping stocks, flows, and feedback loops to study complex industrial systems."}
                        ]
                    }
                ]
            },
            {
                "name": "Quantum Computation",
                "desc": "Harnessing quantum mechanics to process information in high-dimensional computational spaces.",
                "children": [
                    {"name": "Superposition", "desc": "Quantum states existing in multiple configurations simultaneously."},
                    {"name": "Entanglement", "desc": "Non-local physical correlations between distant quantum particle states."},
                    {"name": "Bloch Sphere", "desc": "Geometrical representation of the pure state space of a two-level quantum mechanical system."}
                ]
            },
            {
                "name": "Biological Hardware",
                "desc": "Organic neural tissue, cellular networks, and bio-silicon interfaces for analog cognitive processing."
            },
            {
                "name": "Entropy & Cosmology",
                "desc": "Thermodynamic and cosmological vectors mapping order, information decay, and universal structures.",
                "children": [
                    {"name": "Thermal Decay", "desc": "The dissipation of organized energy patterns into uniform ambient entropy."},
                    {"name": "Hawking Radiation", "desc": "Quantum effects causing black holes to slowly emit thermal energy."}
                ]
            }
        ]
    }
    tree_data_dat.text = json.dumps(hierarchy, indent=4)
    
    # 6. Create Table DATs for tracking active state and children details
    nav_state = hud.create(tableDAT, 'navigation_state')
    nav_state.nodeX = 300
    nav_state.nodeY = 400
    nav_state.setSize(5, 2)
    nav_state[0, 0] = 'path'
    nav_state[0, 1] = 'Thoughts Matrix'
    nav_state[1, 0] = 'selectedChildIndex'
    nav_state[1, 1] = '-1'
    nav_state[2, 0] = 'lastZoomTime'
    nav_state[2, 1] = '0.0'
    nav_state[3, 0] = 'leftGestureLocked'
    nav_state[3, 1] = '0'
    nav_state[4, 0] = 'rightGestureLocked'
    nav_state[4, 1] = '0'
    
    children_data = hud.create(tableDAT, 'children_data')
    children_data.nodeX = 500
    children_data.nodeY = 400
    children_data.setSize(1, 4)
    children_data[0, 0] = 'index'
    children_data[0, 1] = 'name'
    children_data[0, 2] = 'desc'
    children_data[0, 3] = 'hasChildren'

    # 7. Create Navigation Controller Script DAT to manage tree movement
    nav_controller = hud.create(scriptDAT, 'navigation_controller')
    nav_controller.nodeX = 300
    nav_controller.nodeY = 300
    
    nav_controller_code = """import json

def onCook(scriptOP):
	scriptOP.clear()
	
	# Load tree
	tree_data = op('tree_data')
	if not tree_data:
		return
	tree = json.loads(tree_data.text)
	
	# Get path
	nav_state = op('navigation_state')
	path_str = nav_state['path', 1].val
	path_list = [p.strip() for p in path_str.split(',') if p.strip()]
	
	# Traverse tree
	curr = tree
	found_valid = True
	for name in path_list[1:]:
		found = False
		for child in curr.get('children', []):
			if child['name'] == name:
				curr = child
				found = True
				break
		if not found:
			found_valid = False
			break
			
	# If path became corrupted, reset to root
	if not found_valid:
		path_list = [tree['name']]
		curr = tree
		nav_state['path', 1] = tree['name']
		
	# Populate children_data table
	children_table = op('children_data')
	children_table.setSize(1, 4)
	children_table[0, 0] = 'index'
	children_table[0, 1] = 'name'
	children_table[0, 2] = 'desc'
	children_table[0, 3] = 'hasChildren'
	
	kids = curr.get('children', [])
	for idx, kid in enumerate(kids):
		row = children_table.numRows
		children_table.appendRow([
			str(idx),
			kid['name'],
			kid.get('desc', ''),
			'1' if 'children' in kid else '0'
		])

def zoomIn():
	nav_state = op('navigation_state')
	sel_idx = int(nav_state['selectedChildIndex', 1].val)
	if sel_idx < 0:
		return
		
	# Get children names from table
	children_table = op('children_data')
	if sel_idx + 1 >= children_table.numRows:
		return
		
	kid_name = children_table[sel_idx + 1, 'name'].val
	has_kids = children_table[sel_idx + 1, 'hasChildren'].val == '1'
	
	if not has_kids:
		# Cannot zoom into leaf
		return
		
	path_str = nav_state['path', 1].val
	new_path = path_str + ',' + kid_name
	
	nav_state['path', 1] = new_path
	nav_state['selectedChildIndex', 1] = '-1'
	nav_state['lastZoomTime', 1] = str(absTime.seconds)
	
	op('navigation_controller').cook(force=True)

def zoomOut():
	nav_state = op('navigation_state')
	path_str = nav_state['path', 1].val
	path_list = [p.strip() for p in path_str.split(',') if p.strip()]
	
	if len(path_list) <= 1:
		# Already at root
		return
		
	popped_name = path_list.pop()
	new_path = ",".join(path_list)
	
	nav_state['path', 1] = new_path
	
	# Find exited child index in parent
	op('navigation_controller').cook(force=True)
	children_table = op('children_data')
	exited_idx = -1
	for r in range(1, children_table.numRows):
		if children_table[r, 'name'].val == popped_name:
			exited_idx = r - 1
			break
			
	nav_state['selectedChildIndex', 1] = str(exited_idx)
	nav_state['lastZoomTime', 1] = str(absTime.seconds)
"""
    nav_controller_code_dat = hud.create(textDAT, 'nav_controller_code')
    nav_controller_code_dat.text = nav_controller_code
    nav_controller.par.script = nav_controller_code_dat.path
    
    # 8. Create Interaction Logic Script CHOP
    interaction_logic = hud.create(scriptCHOP, 'interaction_logic')
    interaction_logic.nodeX = 300
    interaction_logic.nodeY = 160
    
    interaction_code = """import math

def get_hand_side(select_hand, hand_idx):
	for chan_suffix in ['left_right', 'side', 'handedness']:
		chan = select_hand.chan(f'hand_{hand_idx}/{chan_suffix}')
		if chan is not None:
			val = chan[0]
			if isinstance(val, str):
				return "Left" if "left" in val.lower() else "Right"
			else:
				return "Left" if val < 0.5 else "Right"
	return "Right" if hand_idx == 0 else "Left"

def count_extended_fingers(select_hand, hand_idx):
	count = 0
	
	def get_val(name):
		c = select_hand.chan(f'hand_{hand_idx}/{name}')
		return c[0] if c is not None else 0.0
		
	wx = get_val('joint_0_x')
	wy = get_val('joint_0_y')
	
	if abs(wx) < 0.0001 and abs(wy) < 0.0001:
		return 0
		
	def is_extended(tip, joint):
		tx = get_val(f'joint_{tip}_x')
		ty = get_val(f'joint_{tip}_y')
		jx = get_val(f'joint_{joint}_x')
		jy = get_val(f'joint_{joint}_y')
		d_tip = math.sqrt((tx - wx)**2 + (ty - wy)**2)
		d_joint = math.sqrt((jx - wx)**2 + (jy - wy)**2)
		return d_tip > d_joint * 1.12
		
	if is_extended(8, 6): count += 1
	if is_extended(12, 10): count += 1
	if is_extended(16, 14): count += 1
	if is_extended(20, 18): count += 1
	
	ttx = get_val('joint_4_x')
	tty = get_val('joint_4_y')
	tipx = get_val('joint_3_x')
	tipy = get_val('joint_3_y')
	d_tt = math.sqrt((ttx - wx)**2 + (tty - wy)**2)
	d_ti = math.sqrt((tipx - wx)**2 + (tipy - wy)**2)
	if d_tt > d_ti * 1.05:
		count += 1
		
	return count

def is_5finger_pinch(select_hand, hand_idx):
	def get_val(name):
		c = select_hand.chan(f'hand_{hand_idx}/{name}')
		return c[0] if c is not None else 0.0
		
	wx = get_val('joint_0_x')
	wy = get_val('joint_0_y')
	if abs(wx) < 0.0001 and abs(wy) < 0.0001:
		return False
		
	mx = get_val('joint_9_x')
	my = get_val('joint_9_y')
	
	hand_size = math.sqrt((wx - mx)**2 + (wy - my)**2)
	if hand_size < 0.01: hand_size = 0.01
	
	tips_x = []
	tips_y = []
	for tip in [4, 8, 12, 16, 20]:
		tx = get_val(f'joint_{tip}_x')
		ty = get_val(f'joint_{tip}_y')
		tips_x.append(tx)
		tips_y.append(ty)
		
	cx = sum(tips_x) / 5.0
	cy = sum(tips_y) / 5.0
	
	total_dist = 0.0
	for i in range(5):
		total_dist += math.sqrt((tips_x[i] - cx)**2 + (tips_y[i] - cy)**2)
		
	avg_dist = total_dist / 5.0
	spread_ratio = avg_dist / hand_size
	
	extended_count = count_extended_fingers(select_hand, hand_idx)
	
	return (spread_ratio < 0.45 or extended_count == 0)

def onCook(scriptOP):
	scriptOP.clear()
	
	c_x = scriptOP.appendChan('cursor_x')
	c_y = scriptOP.appendChan('cursor_y')
	c_rx = scriptOP.appendChan('rx')
	c_ry = scriptOP.appendChan('ry')
	c_lpinch = scriptOP.appendChan('left_pinch')
	c_rpinch = scriptOP.appendChan('right_pinch')
	c_sel = scriptOP.appendChan('selected_index')
	c_zin = scriptOP.appendChan('zoom_in_trigger')
	c_zout = scriptOP.appendChan('zoom_out_trigger')
	c_track = scriptOP.appendChan('hand_tracking')
	
	nav_state = op('navigation_state')
	last_zoom = float(nav_state['lastZoomTime', 1].val)
	
	select_hand = op('select_hand')
	
	# Track hands
	hand_data = {}
	has_hand = False
	
	if select_hand and select_hand.numChans > 0:
		for hand_idx in [0, 1]:
			wx_chan = select_hand.chan(f'hand_{hand_idx}/joint_0_x')
			if wx_chan is not None and abs(wx_chan[0]) > 0.0001:
				has_hand = True
				side = get_hand_side(select_hand, hand_idx)
				
				def get_pt(name):
					cx = select_hand.chan(f'hand_{hand_idx}/{name}_x')
					cy = select_hand.chan(f'hand_{hand_idx}/{name}_y')
					return cx[0] if cx else 0.0, cy[0] if cy else 0.0
					
				hx, hy = get_pt('joint_8')
				tx, ty = get_pt('joint_4')
				wx, wy = get_pt('joint_0')
				mx, my = get_pt('joint_9')
				
				hand_size = math.sqrt((wx - mx)**2 + (wy - my)**2)
				if hand_size < 0.01: hand_size = 0.01
				
				dist = math.sqrt((hx - tx)**2 + (hy - ty)**2)
				ratio = dist / hand_size
				
				is_pinch = is_5finger_pinch(select_hand, hand_idx)
				
				hand_data[side] = {
					'hx': hx, 'hy': hy,
					'ratio': ratio,
					'is_pinch': is_pinch
				}
				
	c_track[0] = 1.0 if has_hand else 0.0
	
	# Determine rotation active (either hand performing 5-finger pinch)
	rotation_side = None
	for side in ['Left', 'Right']:
		if side in hand_data and hand_data[side]['is_pinch']:
			rotation_side = side
			break
			
	pointer_x, pointer_y = 0.5, 0.5
	is_rotating = rotation_side is not None
	has_selector = False
	if is_rotating:
		rd = hand_data[rotation_side]
		pointer_x = 1.0 - rd['hx']
		pointer_y = rd['hy']
		ry = (pointer_x - 0.5) * 302.5
		rx = (pointer_y - 0.5) * -150.0
	else:
		# Pointer strictly follows the Right Hand if present
		if 'Right' in hand_data:
			rd = hand_data['Right']
			pointer_x = 1.0 - rd['hx']
			pointer_y = rd['hy']
			has_selector = True
		
		# Ambient rotation
		ry = (absTime.seconds * 4.5) % 360.0
		rx = 14.0 + 5.0 * math.sin(absTime.seconds * 0.3)
		
	c_x[0] = pointer_x
	c_y[0] = pointer_y
	c_rx[0] = rx
	c_ry[0] = ry
	
	l_ratio = hand_data['Left']['ratio'] if 'Left' in hand_data else 1.0
	r_ratio = hand_data['Right']['ratio'] if 'Right' in hand_data else 1.0
	c_lpinch[0] = l_ratio
	c_rpinch[0] = r_ratio
	
	# Node selection (Projected nearest)
	children_table = op('children_data')
	num_kids = children_table.numRows - 1
	nearest_idx = -1
	min_dist = 9999.0
	
	# Node selection ONLY runs if Right Hand is present (has_selector is True) and we are not rotating
	if has_selector and not is_rotating and num_kids > 0:
		R = 2.0
		cosY = math.cos(math.radians(ry))
		sinY = math.sin(math.radians(ry))
		cosX = math.cos(math.radians(rx))
		sinX = math.sin(math.radians(rx))
		
		pointer_sx = pointer_x - 0.5
		pointer_sy = pointer_y - 0.5
		
		for idx in range(num_kids):
			angle = (idx * 2 * math.pi) / num_kids
			kx = R * math.cos(angle)
			ky = R * math.sin(angle)
			kz = 0.35 * math.sin(idx * 1.7)
			
			x1 = kx * cosY - kz * sinY
			z1 = kx * sinY + kz * cosY
			y2 = ky * cosX + z1 * sinX
			z2 = -ky * sinX + z1 * cosX
			
			scale = 5.0 / (5.0 + z2)
			proj_x = x1 * scale * 0.2
			proj_y = y2 * scale * 0.2
			
			dx = proj_x - pointer_sx
			dy = proj_y - pointer_sy
			dist = math.sqrt(dx*dx + dy*dy)
			
			if dist < min_dist and dist < 0.15:
				min_dist = dist
				nearest_idx = idx
				
	c_sel[0] = nearest_idx
	nav_state['selectedChildIndex', 1] = str(nearest_idx)
	
	# Reset locks in neutral zone
	left_locked = nav_state['leftGestureLocked', 1].val == '1'
	right_locked = nav_state['rightGestureLocked', 1].val == '1'
	
	if 'Left' in hand_data:
		l_r = hand_data['Left']['ratio']
		if l_r > 0.65 and l_r < 1.35:
			left_locked = False
			nav_state['leftGestureLocked', 1] = '0'
	if 'Right' in hand_data:
		r_r = hand_data['Right']['ratio']
		if r_r > 0.65 and r_r < 1.35:
			right_locked = False
			nav_state['rightGestureLocked', 1] = '0'
			
	# Triggers (Zoom blocked if rotation is active)
	zin_trig = 0.0
	zout_trig = 0.0
	cooldown = (absTime.seconds - last_zoom) > 1.3 and not is_rotating
	
	if cooldown:
		if 'Left' in hand_data and not left_locked:
			if hand_data['Left']['ratio'] < 0.42:
				zout_trig = 1.0
				nav_state['leftGestureLocked', 1] = '1'
				
		if 'Right' in hand_data and not right_locked and nearest_idx != -1:
			if hand_data['Right']['ratio'] < 0.42:
				zin_trig = 1.0
				nav_state['rightGestureLocked', 1] = '1'
				
	c_zin[0] = zin_trig
	c_zout[0] = zout_trig
"""
    interaction_code_dat = hud.create(textDAT, 'interaction_code')
    interaction_code_dat.text = interaction_code
    interaction_logic.par.script = interaction_code_dat.path
    
    # 9. Create CHOP Execute DAT to execute navigations on CHOP pulses
    chop_exec = hud.create(chopexecuteDAT, 'chop_execute')
    chop_exec.nodeX = 300
    chop_exec.nodeY = 50
    chop_exec.par.chop = interaction_logic.path
    chop_exec.par.valchange = True
    
    chop_exec_code = """def onValueChange(channel, sampleIndex, val, prev):
	if val > 0.5 and prev <= 0.5:
		if channel.name == 'zoom_in_trigger':
			op('navigation_controller').zoomIn()
		elif channel.name == 'zoom_out_trigger':
			op('navigation_controller').zoomOut()
"""
    chop_exec_code_dat = hud.create(textDAT, 'chop_exec_code')
    chop_exec_code_dat.text = chop_exec_code
    chop_exec.par.script = chop_exec_code_dat.path
    
    # 10. Create Script SOP to draw the 3D Network Topology
    script_geometry = hud.create(scriptSOP, 'script_geometry')
    script_geometry.nodeX = 550
    script_geometry.nodeY = 200
    
    sop_geometry_code = """import math

def draw_dashed_box(scriptOp, center, size, color):
	# Draw targeting bracket corner lines
	l = size * 0.4
	
	# Top-Left
	p_tl1 = center + tdu.Vector(-size, size - l, 0)
	p_tl2 = center + tdu.Vector(-size, size, 0)
	p_tl3 = center + tdu.Vector(-size + l, size, 0)
	draw_line_strip(scriptOp, [p_tl1, p_tl2, p_tl3], color)
	
	# Top-Right
	p_tr1 = center + tdu.Vector(size - l, size, 0)
	p_tr2 = center + tdu.Vector(size, size, 0)
	p_tr3 = center + tdu.Vector(size, size - l, 0)
	draw_line_strip(scriptOp, [p_tr1, p_tr2, p_tr3], color)
	
	# Bottom-Left
	p_bl1 = center + tdu.Vector(-size, -size + l, 0)
	p_bl2 = center + tdu.Vector(-size, -size, 0)
	p_bl3 = center + tdu.Vector(-size + l, -size, 0)
	draw_line_strip(scriptOp, [p_bl1, p_bl2, p_bl3], color)
	
	# Bottom-Right
	p_br1 = center + tdu.Vector(size - l, -size, 0)
	p_br2 = center + tdu.Vector(size, -size, 0)
	p_br3 = center + tdu.Vector(size, -size + l, 0)
	draw_line_strip(scriptOp, [p_br1, p_br2, p_br3], color)

def draw_circle(scriptOp, center, radius, color):
	segments = 12
	poly = scriptOp.appendPoly(segments, closed=True)
	for i in range(segments):
		theta = (i / segments) * 2.0 * math.pi
		pt = scriptOp.appendPoint()
		pt.x = center.x + radius * math.cos(theta)
		pt.y = center.y + radius * math.sin(theta)
		pt.z = center.z
		pt.attribData['Cd'] = color
		poly[i].point = pt

def draw_line_strip(scriptOp, points, color):
	poly = scriptOp.appendPoly(len(points), closed=False)
	for i, p in enumerate(points):
		pt = scriptOp.appendPoint()
		pt.x, pt.y, pt.z = p.x, p.y, p.z
		pt.attribData['Cd'] = color
		poly[i].point = pt

def onCook(scriptOp):
	scriptOp.clear()
	
	# Add point colors attribute
	cd_attr = scriptOp.createPointAttrib('Cd', 4, float)
	
	# Read children positions
	children_table = op('children_data')
	num_kids = children_table.numRows - 1
	
	nav_state = op('navigation_state')
	selected_idx = int(nav_state['selectedChildIndex', 1].val)
	
	# 1. Parent Node (Center, cyan color)
	parent_pt = scriptOp.appendPoint()
	parent_pt.x, parent_pt.y, parent_pt.z = 0.0, 0.0, 0.0
	parent_pt.attribData['Cd'] = [0.0, 1.0, 1.0, 1.0] # Cyan parent
	draw_circle(scriptOp, tdu.Vector(0,0,0), 0.22, color=[0.0, 1.0, 1.0, 0.8])
	
	# 2. Children Nodes (Circular orbit, monochromatic white)
	if num_kids > 0:
		R = 2.0
		child_pts = []
		for idx in range(num_kids):
			angle = (idx * 2 * math.pi) / num_kids
			x = R * math.cos(angle)
			y = R * math.sin(angle)
			z = 0.35 * math.sin(idx * 1.7)
			
			pt = scriptOp.appendPoint()
			pt.x, pt.y, pt.z = x, y, z
			pt.attribData['Cd'] = [1.0, 1.0, 1.0, 1.0] # Monochromatic white
			child_pts.append(pt)
			
			# Draw node circle
			draw_circle(scriptOp, tdu.Vector(x, y, z), 0.12, color=[1.0, 1.0, 1.0, 0.6])
			
			# Draw edge connecting parent to kid (monochromatic link)
			link_poly = scriptOp.appendPoly(2, closed=False)
			link_poly[0].point = parent_pt
			link_poly[1].point = pt
			# Cyan-tinted parent center, fading to white child
			parent_pt_edge = scriptOp.appendPoint()
			parent_pt_edge.x, parent_pt_edge.y, parent_pt_edge.z = 0, 0, 0
			parent_pt_edge.attribData['Cd'] = [1.0, 1.0, 1.0, 0.25]
			
			pt_edge = scriptOp.appendPoint()
			pt_edge.x, pt_edge.y, pt_edge.z = x, y, z
			pt_edge.attribData['Cd'] = [1.0, 1.0, 1.0, 0.25]
			
			edge_poly = scriptOp.appendPoly(2, closed=False)
			edge_poly[0].point = parent_pt_edge
			edge_poly[1].point = pt_edge
			
			# If child is selected, draw targeting box (monochromatic white)
			if idx == selected_idx:
				draw_dashed_box(scriptOp, tdu.Vector(x, y, z), 0.24, color=[1.0, 1.0, 1.0, 0.95])
"""
    sop_geometry_code_dat = hud.create(textDAT, 'sop_geometry_code')
    sop_geometry_code_dat.text = sop_geometry_code
    script_geometry.par.script = sop_geometry_code_dat.path
    
    # 11. Create Merge SOP and Text SOPs for labeling nodes dynamically
    merge_sop = hud.create(mergeSOP, 'merge_geom')
    merge_sop.nodeX = 750
    merge_sop.nodeY = 200
    merge_sop.inputConnectors[0].connect(script_geometry)
    
    # Label parent node
    parent_label = hud.create(textSOP, 'parent_label')
    parent_label.nodeX = 550
    parent_label.nodeY = 0
    parent_label.par.text.expr = "op('navigation_state')['path', 1].val.split(',')[-1].upper()"
    parent_label.par.font = 'Arial'
    parent_label.par.bold = True
    parent_label.par.alignx = 1 # Center
    parent_label.par.aligny = 1
    parent_label.par.size = 0.075
    parent_label.par.ty = 0.35
    merge_sop.inputConnectors[merge_sop.numInputs].connect(parent_label)
    
    # Dynamic labels for kids (up to 8 slots)
    for idx in range(8):
        txt = hud.create(textSOP, f'text_kid_{idx}')
        txt.nodeX = 550
        txt.nodeY = -100 - (idx * 60)
        
        # Only render text if children index exists
        txt.par.text.expr = f"op('children_data')[{idx+1}, 'name'].val.upper() if op('children_data').numRows > {idx+1} else ''"
        txt.par.font = 'Arial'
        txt.par.alignx = 1
        txt.par.aligny = 1
        txt.par.size = 0.05
        
        # Place label above the child node point
        txt.par.tx.expr = f"op('script_geometry').points[{idx+1}].x if len(op('script_geometry').points) > {idx+1} else 0.0"
        txt.par.ty.expr = f"(op('script_geometry').points[{idx+1}].y + 0.22) if len(op('script_geometry').points) > {idx+1} else 0.0"
        txt.par.tz.expr = f"op('script_geometry').points[{idx+1}].z if len(op('script_geometry').points) > {idx+1} else 0.0"
        
        merge_sop.inputConnectors[merge_sop.numInputs].connect(txt)
        
    # 12. Create Constant MAT (with point colors enabled)
    mat = hud.create(constantMAT, 'hud_material')
    mat.nodeX = 750
    mat.nodeY = 400
    mat.par.colorr = 1.0
    mat.par.colorg = 1.0
    mat.par.colorb = 1.0
    mat.par.pointcolor = True  # Crucial to respect parent vs children colors
    
    # 13. Create Geometry COMP
    geo = hud.create(geoCOMP, 'geo_scene')
    geo.nodeX = 950
    geo.nodeY = 200
    geo.par.sopPath = merge_sop.path
    geo.par.material = mat.path
    geo.par.ry.expr = "op('interaction_logic')['ry'][0]"
    geo.par.rx.expr = "op('interaction_logic')['rx'][0]"
    
    # 14. Create Camera and Light COMPs
    cam = hud.create(cameraCOMP, 'camera1')
    cam.nodeX = 950
    cam.nodeY = 320
    cam.par.tx = 0.0
    cam.par.ty = 0.0
    cam.par.tz = 5.0
    
    # 15. Create Render TOP (720x1280 vertical resolution)
    render = hud.create(renderTOP, 'render_scene')
    render.nodeX = 1150
    render.nodeY = 200
    render.par.camera = cam.path
    render.par.geometry = geo.path
    render.par.resolutionw = 720
    render.par.resolutionh = 1280
    
    # 16. Create Glow (Blur + Add Composite)
    blur = hud.create(blurTOP, 'render_blur')
    blur.nodeX = 1300
    blur.nodeY = 250
    blur.inputConnectors[0].connect(render)
    blur.par.size = 10
    
    glow_composite = hud.create(compositeTOP, 'glow_composite')
    glow_composite.nodeX = 1450
    glow_composite.nodeY = 200
    glow_composite.par.operand = 0 # Add
    glow_composite.inputConnectors[0].connect(render)
    glow_composite.inputConnectors[1].connect(blur)
    
    # 17. Create Grayscale Video Background (webcam level)
    webcam = hud.create(videodeviceinTOP, 'webcam_feed')
    webcam.nodeX = 1150
    webcam.nodeY = 0
    
    webcam_level = hud.create(levelTOP, 'webcam_level')
    webcam_level.nodeX = 1300
    webcam_level.nodeY = 0
    webcam_level.inputConnectors[0].connect(webcam)
    webcam_level.par.opacity = 0.2 # Grayscale webcam feed
    webcam_level.par.saturation = 0.0
    webcam_level.par.contrast = 1.2
    
    # 18. Overlay Rendered scene on Webcam
    comp_base = hud.create(overTOP, 'comp_base_webcam')
    comp_base.nodeX = 1600
    comp_base.nodeY = 150
    comp_base.inputConnectors[0].connect(glow_composite) # Foreground
    comp_base.inputConnectors[1].connect(webcam_level) # Background
    
    # 19.5 Fingertip / Pointer cursor overlay
    cursor_circle = hud.create(circleTOP, 'cursor_circle')
    cursor_circle.nodeX = 1450
    cursor_circle.nodeY = 320
    cursor_circle.par.radiusx = 0.015
    cursor_circle.par.radiusy = 0.015
    cursor_circle.par.fillcolora = 0.0 # Outline only
    
    # Color expression: cyan if hand tracking, white if mouse fallback
    cursor_circle.par.bordercolorr.expr = "1.0 if op('interaction_logic')['hand_tracking'][0] > 0.5 else 1.0"
    cursor_circle.par.bordercolorg.expr = "1.0 if op('interaction_logic')['hand_tracking'][0] > 0.5 else 1.0"
    cursor_circle.par.bordercolorb.expr = "1.0 if op('interaction_logic')['hand_tracking'][0] > 0.5 else 1.0"
    cursor_circle.par.bordercolora = 0.7
    cursor_circle.par.borderw = 1.2
    
    cursor_trans = hud.create(transformTOP, 'cursor_trans')
    cursor_trans.nodeX = 1600
    cursor_trans.nodeY = 320
    cursor_trans.inputConnectors[0].connect(cursor_circle)
    cursor_trans.par.translatex.expr = "op('interaction_logic')['cursor_x'][0] - 0.5"
    cursor_trans.par.translatey.expr = "op('interaction_logic')['cursor_y'][0] - 0.5"

    # Compositing chain
    comp_cursor = hud.create(overTOP, 'comp_cursor')
    comp_cursor.nodeX = 1800
    comp_cursor.nodeY = 150
    comp_cursor.inputConnectors[0].connect(cursor_trans)
    comp_cursor.inputConnectors[1].connect(comp_base)
    
    out1 = hud.create(outTOP, 'out_final')
    out1.nodeX = 1950
    out1.nodeY = 150
    out1.inputConnectors[0].connect(comp_cursor)
    
    # Cook everything to trigger internal scripts
    nav_controller.cook(force=True)
    interaction_logic.cook(force=True)
    script_geometry.cook(force=True)
    
    print("[NetworkTopology] Completed build automation setup successfully!")

# Run construction if executed inside TouchDesigner
if __name__ == '__main__':
    build_network_topology()
