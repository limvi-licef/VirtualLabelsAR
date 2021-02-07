#version 330 core

in vec4 aPos;
in vec3 aNorm;

uniform mat4 uProjection;
uniform mat4 uModelview;

uniform mat4 uVertexTransform;
uniform mat4 uNormalTransform;

out vec3 fNorm;

void main() {

    vec4 pos = uVertexTransform * (aPos / aPos.w);
    gl_Position = uProjection * uModelview * pos;
    fNorm = mat3(uModelview) * (uNormalTransform * vec4(normalize(aNorm), 1.0)).xyz;
}