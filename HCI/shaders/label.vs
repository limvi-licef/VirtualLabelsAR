#version 330 core

in vec4 aCoords;

uniform mat4 uProjection;
uniform mat4 uModelview;
uniform mat4 uPosition;

out vec2 fTex;

void main() {

    gl_Position = uProjection * uModelview * uPosition * vec4(aCoords.x, aCoords.y, 0.0, 1.0);
    fTex = vec2(aCoords.z, aCoords.w);
}