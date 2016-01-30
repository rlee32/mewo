// Global parameters.
tube_radius = 0.5;
joint_distance_factor = 4;
Geometry.Tolerance = 1e-10;

// Include "shapes/cloth_and_tube.geo";
Include "shapes/cloth_and_tube_and_string.geo";
Include "physical_inputs.geo";

// Convert physical input values.
For k In {0:#element_aoas[]-1}
  element_aoas[k] *= Pi/180;
EndFor
For k In {0:#cloth_span_angles[]-1}
  cloth_span_angles[k] *= Pi/180;
EndFor
tube_radius *= 0.0254;
cloth_thickness_factor = 0.05;  
cloth_thickness = cloth_thickness_factor*tube_radius;  
joint_distance = joint_distance_factor*tube_radius;  

Include "numerical_inputs.geo";

current_entity = 0;
leading_edge[] = {0,0,0};

Call draw_wing;
Translate {-quarter_chord[0], -quarter_chord[1], 0} { Line{wing_outlines[]}; }

boundary_min_y = global_trailing_edge[1] - boundary_distance;
boundary_max_x = global_trailing_edge[0] + boundary_distance;
boundary_max_y = global_leading_edge[1] + boundary_distance;
boundary_min_x = global_leading_edge[0] - boundary_distance;

points[] = {};
Point(current_entity++) = {boundary_max_x, boundary_max_y, 0}; 
  points[] += current_entity;
Point(current_entity++) = {boundary_min_x, boundary_max_y, 0};
  points[] += current_entity;
Point(current_entity++) = {boundary_min_x, boundary_min_y, 0};
  points[] += current_entity;
Point(current_entity++) = {boundary_max_x, boundary_min_y, 0};
  points[] += current_entity;

lines[] = {};
Line(current_entity++) = {points[0], points[1]};
  lines[] += current_entity;
Line(current_entity++) = {points[1], points[2]};
  lines[] += current_entity;
Line(current_entity++) = {points[2], points[3]};
  lines[] += current_entity;
Line(current_entity++) = {points[3], points[0]};
  lines[] += current_entity;

Characteristic Length { points[] } = boundary_grid;
Line Loop(current_entity++) = lines[]; boundary_loop = current_entity;

wing_points[] = Boundary{ Line{ wing_outlines[] }; };
Characteristic Length { wing_points[] } = wing_grid;
Characteristic Length { wing_inner_points[] } = inner_wing_grid;
wing_loops[] = {};
outlines_per_element = #wing_outlines[] / #element_aoas[];
For k In {0:#element_aoas[]-1}
  Line Loop(current_entity++) 
    = wing_outlines[{(k*outlines_per_element):((k+1)*outlines_per_element-1)}];
  wing_loops[k] = current_entity;
EndFor
// Line Loop(current_entity++) = wing_outlines[]; wing_loops = current_entity;

Plane Surface(current_entity++) = { boundary_loop, wing_loops[] };
main_surface = current_entity;

new_entities[] = Extrude {0, 0, cell_depth} 
{
    Surface{main_surface};
    Layers{1};
    Recombine;
};

// Physical Surface("freestream") = {new_entities[{2:5}]};
Physical Surface("inlet") = {new_entities[{3}]};
Physical Surface("outlet") = {new_entities[{5}]};
Physical Surface("tunnel") = {new_entities[{2,4}]};
Physical Surface("wing") = {new_entities[{6:(#wing_outlines[]+6-1)}]};
Physical Surface("front_and_back") = {main_surface,new_entities[0]};
Physical Volume("volume") = {new_entities[1]};



