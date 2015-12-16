

Function rotate_lines
  // In: rotation_center[]={};rotation_lines[]=;rotation_angle=;
  Rotate
  { 
    { 0,0,1 }, 
    { rotation_center[0], rotation_center[1], rotation_center[2] }, 
    rotation_angle
  } 
  { 
    Line{rotation_lines[]}; 
  }
Return
Function rotate_points
  // In: rotation_center[]={};rotation_points[]=;rotation_angle=;
  Rotate
  { 
    { 0,0,1 }, 
    { rotation_center[0], rotation_center[1], rotation_center[2] }, 
    rotation_angle
  } 
  { 
    Point{rotation_points[]}; 
  }
Return

Function draw_wrap
  // Global: current_entity, wing_inner_points[]+=;
  // In: tube_center[]={};tube_radius=;joint_distance=;
  //     cloth_thickness=;wrap_rotation_angle=;  
  // Out: wrap_outlines[];

  // Calculate geometry.
  alpha = Asin(tube_radius / joint_distance);
  delta = cloth_thickness / 2 / Cos(alpha);

  // Make points.
  Point(current_entity++) = {tube_center[0],tube_center[1],tube_center[2]}; 
    center_point = current_entity;
  Point(current_entity++) = {tube_center[0]-tube_radius,tube_center[1],
    tube_center[2]}; front_point = current_entity;
  Point(current_entity++) = {tube_center[0],tube_center[1]+tube_radius,
    tube_center[2]}; top_point = current_entity;
  Point(current_entity++) = {tube_center[0],tube_center[1]-tube_radius,
    tube_center[2]}; bottom_point = current_entity;
  Point(current_entity++) = {
    tube_center[0] + joint_distance - delta,
    tube_center[1] + cloth_thickness / 2,
    tube_center[2]}; top_joint_point = current_entity;
  Point(current_entity++) = {
    tube_center[0] + joint_distance - delta,
    tube_center[1] - cloth_thickness / 2,
    tube_center[2]}; bottom_joint_point = current_entity;
  wing_inner_points[]+=top_joint_point;
  wing_inner_points[]+=bottom_joint_point;

  // Transform points.
  rotation_center[]=tube_center[];rotation_points[]={top_point};
  rotation_angle=-alpha;
  Call rotate_points;
  rotation_center[]=tube_center[];rotation_points[]={bottom_point};
  rotation_angle=alpha;
  Call rotate_points;

  // Make lines.
  wrap_outlines[]={};
  Line(current_entity++) = {top_joint_point, top_point};
    wrap_outlines[] += current_entity;
  Circle(current_entity++) = {top_point, center_point, front_point}; 
    wrap_outlines[] += current_entity;
  Circle(current_entity++) = {front_point, center_point, bottom_point}; 
    wrap_outlines[] += current_entity;
  Line(current_entity++) = {bottom_point, bottom_joint_point};
    wrap_outlines[] += current_entity;

  //Transform lines.
  rotation_center[] = tube_center[]; rotation_lines[] = wrap_outlines[];
  rotation_angle = wrap_rotation_angle;
  Call rotate_lines;
Return

Function draw_te
  // Global: current_entity, wing_inner_points[]+=;
  // In: tube_center[]={};joint_distance=;
  //     cloth_thickness=;wrap_rotation_angle=;  
  // Out: wrap_outlines[];

  // Calculate geometry.
  alpha = Asin(tube_radius / joint_distance);
  delta = cloth_thickness / 2 / Cos(alpha);

  // Make points.
  Point(current_entity++) = {tube_center[0],tube_center[1],tube_center[2]}; 
    center_point = current_entity;
  // Point(current_entity++) = {tube_center[0]-tube_radius,tube_center[1],
  //   tube_center[2]}; front_point = current_entity;
  // Point(current_entity++) = {tube_center[0],tube_center[1]+tube_radius,
  //   tube_center[2]}; top_point = current_entity;
  // Point(current_entity++) = {tube_center[0],tube_center[1]-tube_radius,
  //   tube_center[2]}; bottom_point = current_entity;
  Point(current_entity++) = {
    tube_center[0] + joint_distance - delta,
    tube_center[1] + cloth_thickness / 2,
    tube_center[2]}; top_joint_point = current_entity;
  Point(current_entity++) = {
    tube_center[0] + joint_distance - delta,
    tube_center[1] - cloth_thickness / 2,
    tube_center[2]}; bottom_joint_point = current_entity;
  wing_inner_points[]+=top_joint_point;
  wing_inner_points[]+=bottom_joint_point;

  // Make lines.
  wrap_outlines[]={};
  Line(current_entity++) = {top_joint_point, center_point};
    wrap_outlines[] += current_entity;
  Line(current_entity++) = {center_point, bottom_joint_point};
    wrap_outlines[] += current_entity;

  //Transform lines.
  rotation_center[] = tube_center[]; rotation_lines[] = wrap_outlines[];
  rotation_angle = wrap_rotation_angle;
  Call rotate_lines;
Return

Function draw_element
  // In: element_aoa=;element_chord=;leading_edge[]={};cloth_span_angle=;
  //     cloth_thickness=;joint_distance=;
  // Out: element_outlines[];

  // We restrict cloth_span_angle < 180 degrees.

  element_outlines[]={};

  // Make end parts.
  tube_center[]=leading_edge[]; wrap_rotation_angle = cloth_span_angle / 2;
  Call draw_wrap; 
  
  top_second_point = top_joint_point;
  bottom_first_point = bottom_joint_point;
    front_wrap_outlines[] = wrap_outlines[];
  
  tube_center[]={leading_edge[0]+element_chord, leading_edge[1], 
    leading_edge[2]}; 
  wrap_rotation_angle = Pi - cloth_span_angle / 2;
  // Call draw_wrap; 
  Call draw_te;

  top_first_point = bottom_joint_point;
  bottom_second_point = top_joint_point;
  trailing_center_point = center_point;
  back_wrap_outlines[] = wrap_outlines[];

  // Draw innner foil.
  gamma2 = cloth_span_angle / 2;
  // h = (element_chord / 2 - Cos(gamma2)*joint_distance)*Cos(Pi/2 - gamma2);
  circle_chord_half = element_chord / 2 - Cos(gamma2)*joint_distance;
  center_distance = circle_chord_half / Tan(gamma2);
  // circle_radius = circle_chord_half / Sin(gamma2);
  // thickness = circle_radius - center_distance + Sin(gamma2) * joint_distance;
  // Printf( "Normalized thickness: %f", thickness / element_chord );
  Point(current_entity++) = { leading_edge[0]+element_chord/2, 
    leading_edge[1]-center_distance, 
    leading_edge[2] };
  center_point = current_entity;
  Circle(current_entity++) = { bottom_first_point, center_point, 
    bottom_second_point };
  bottom_line = current_entity;
  Circle(current_entity++) = { top_first_point, center_point, 
    top_second_point };
  top_line = current_entity;

  // Consolidate lines.
  element_outlines[] = { front_wrap_outlines[], bottom_line, 
    back_wrap_outlines[], top_line };

  // Transform element.
  rotation_center[] = leading_edge[]; rotation_lines[] = element_outlines[];
  rotation_angle = -element_aoa;
  Call rotate_lines;
Return

Function draw_wing
  // In: element_aoas[]={};element_chords[]={};
  //     leading_edge[]={};cloth_span_angles[]={};
  //     gap_x[]={};gap_y[]={};
  //     cloth_thickness=;joint_distance=;tube_radius=;
  // Out: wing_outlines[];
  
  wing_outlines[]={};
  wing_inner_points[]={};

  global_leading_edge[] = leading_edge[];

  number_of_elements = #element_chords[];
  current_leading_edge[] = leading_edge[];
  For k In {0:number_of_elements-1}
    If (k > 0)
      current_leading_edge[0] += Cos(element_aoas[k-1])*element_chords[k-1]
        - gap_x[k]*Cos(element_aoas[k-1]) 
        + gap_y[k]*Sin(element_aoas[k-1]);
      current_leading_edge[1] -= Sin(element_aoas[k-1])*element_chords[k-1]
        - gap_y[k]*Cos(element_aoas[k-1])
        - gap_x[k]*Sin(element_aoas[k-1]);
    EndIf
  
    element_aoa = element_aoas[k]; 
    element_chord = element_chords[k]; 
    leading_edge[] = current_leading_edge[];
    cloth_span_angle = cloth_span_angles[k];
    Call draw_element;

    wing_outlines[] += element_outlines[];
  EndFor

  // Calculate and output the global chord.
  current_leading_edge[0] += Cos(element_aoas[number_of_elements-1])
    *element_chords[number_of_elements-1];
  current_leading_edge[1] -= Sin(element_aoas[number_of_elements-1])
    *element_chords[number_of_elements-1];
  global_trailing_edge[] = current_leading_edge[];
  global_chord = Sqrt(
    (global_leading_edge[0] - global_trailing_edge[0])^2
    + (global_leading_edge[1] - global_trailing_edge[1])^2
    + (global_leading_edge[2] - global_trailing_edge[2])^2
    );
  Printf("%f", global_chord) > "../geometry.dat";
  Printf("%f", cell_depth) >> "../geometry.dat";
  quarter_chord[] = {0, 0, 0};
  quarter_chord[0] = global_leading_edge[0] 
    + (global_trailing_edge[0] - global_leading_edge[0]) / 4;
  quarter_chord[1] = global_leading_edge[1] 
    + (global_trailing_edge[1] - global_leading_edge[1]) / 4;
  // Point(ce++) = {quarter_chord[0], quarter_chord[1], quarter_chord[2]};
Return

// current_entity = 0;
// Include "../physical_inputs.geo";
// // Convert physical input values.
// For k In {0:#element_aoas[]-1}
//   element_aoas[k] *= Pi/180;
// EndFor
// For k In {0:#cloth_span_angles[]-1}
//   cloth_span_angles[k] *= Pi/180;
// EndFor
// tube_radius *= 0.0254;
// cloth_thickness_factor = 0.05;  
// cloth_thickness = cloth_thickness_factor*tube_radius;  
// joint_distance = joint_distance_factor*tube_radius;  

// element_aoa=5*Pi/180;element_chord=1;leading_edge[]={0,0,0};
// cloth_span_angle=45*Pi/180;
// tube_radius = 0.5*0.0254;
// cloth_thickness=0.02*tube_radius;joint_distance=4*tube_radius;
// Call draw_wing;




