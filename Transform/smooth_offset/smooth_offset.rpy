-'''
-
-Copyright 2026.6.16 Koji-Mio(kojimio@outlook.com)
-
-Licensed under the Apache License, Version 2.0 (the "License");
-you may not use this file except in compliance with the License.
-You may obtain a copy of the License at
-
-    http://www.apache.org/licenses/LICENSE-2.0
-
-Unless required by applicable law or agreed to in writing, software
-distributed under the License is distributed on an "AS IS" BASIS,
-WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-See the License for the specific language governing permissions and
-limitations under the License.
-
-'''

init python:
    renpy.register_shader("smooth_offset", variables="""
        uniform mat4 u_transform;
        attribute vec4 a_position;
        uniform vec2 u_virtual_size;
        uniform float u_animation;
        uniform vec2 u_pos;
    """, vertex_200="""
        gl_Position = u_transform * a_position + vec4(mix(vec2(0, 0), u_pos, u_animation)/u_virtual_size*2.0, 0, 0);
    """)

transform smooth_offset(time, offset):
    mesh True
    shader "smooth_offset"
    u_animation 0.0
    u_pos offset
    linear time u_animation 1.0
    shader None
