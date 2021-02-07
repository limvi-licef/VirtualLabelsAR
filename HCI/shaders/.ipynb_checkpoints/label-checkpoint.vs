#version 330 core

in vec3 aPos;

uniform mat4 uProjection;
uniform mat4 uModelview;

void main() {

    gl_Position = uProjection * uModelview * vec4(aPos, 1.0);
}