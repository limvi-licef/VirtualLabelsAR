#version 330 core

in vec4 aCoords;

out vec2 fTex;

void main() {

    vec2 pos = vec2(aCoords.x, aCoords.y);
    vec2 tex = vec2(aCoords.z, aCoords.w);

    gl_Position = vec4(pos.x, pos.y, 0.0, 0.5);
    fTex = tex;
}