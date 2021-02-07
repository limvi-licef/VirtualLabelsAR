#version 330 core

in vec3 fNorm;

out vec4 FragColor;

void main() {

    float i = ( dot(normalize(fNorm), vec3(0,0,1)) + 1.0 ) / 2.0;
    FragColor = vec4(i);
}