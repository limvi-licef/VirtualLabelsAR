#version 330 core

in vec2 fTex;

uniform sampler2D uTexture;

out vec4 FragColor;

void main() {

    FragColor = 1.0-texture(uTexture, fTex);
}