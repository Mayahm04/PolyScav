extern "C" {
    #include <glad/glad.h>
}

//#include <glad/glad.h>
#include <GLFW/glfw3.h>

#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

#include <fstream>      // ← AJOUT OBLIGATOIRE
#include <sstream>      // ← AJOUT OBLIGATOIRE
#include <iostream>
#include <vector>
#include <cmath>



// === Util: chargement fichier texte ===
std::string loadFile(const std::string& path)
{
    std::ifstream f(path);
    if (!f) {
        std::cerr << "Impossible d'ouvrir " << path << std::endl;
        return "";
    }
    std::stringstream ss;
    ss << f.rdbuf();
    return ss.str();
}

GLuint createShaderProgram(const std::string& vsPath, const std::string& fsPath)
{
    std::string vsCode = loadFile(vsPath);
    std::string fsCode = loadFile(fsPath);
    const char* vsrc = vsCode.c_str();
    const char* fsrc = fsCode.c_str();

    GLuint vs = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(vs, 1, &vsrc, nullptr);
    glCompileShader(vs);

    GLint success;
    glGetShaderiv(vs, GL_COMPILE_STATUS, &success);
    if (!success) {
        char log[512];
        glGetShaderInfoLog(vs, 512, nullptr, log);
        std::cerr << "Erreur compilation vertex shader: " << log << std::endl;
    }

    GLuint fs = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(fs, 1, &fsrc, nullptr);
    glCompileShader(fs);
    glGetShaderiv(fs, GL_COMPILE_STATUS, &success);
    if (!success) {
        char log[512];
        glGetShaderInfoLog(fs, 512, nullptr, log);
        std::cerr << "Erreur compilation fragment shader: " << log << std::endl;
    }

    GLuint prog = glCreateProgram();
    glAttachShader(prog, vs);
    glAttachShader(prog, fs);
    glLinkProgram(prog);

    glGetProgramiv(prog, GL_LINK_STATUS, &success);
    if (!success) {
        char log[512];
        glGetProgramInfoLog(prog, 512, nullptr, log);
        std::cerr << "Erreur link program: " << log << std::endl;
    }

    glDeleteShader(vs);
    glDeleteShader(fs);
    return prog;
}

// === Mesh pour cube: positions + normales + indices ===
struct Mesh {
    GLuint vao = 0;
    GLuint vbo = 0;
    GLuint ebo = 0;
    GLsizei indexCount = 0;
};

Mesh createCube()
{
    // 8 sommets, mais ici on duplique par face pour avoir des normales par face
    float vertices[] = {
        // positions         // normales
        // face avant
        -0.5f, -0.5f,  0.5f,  0, 0, 1,
         0.5f, -0.5f,  0.5f,  0, 0, 1,
         0.5f,  0.5f,  0.5f,  0, 0, 1,
        -0.5f,  0.5f,  0.5f,  0, 0, 1,
        // face arrière
        -0.5f, -0.5f, -0.5f,  0, 0,-1,
         0.5f, -0.5f, -0.5f,  0, 0,-1,
         0.5f,  0.5f, -0.5f,  0, 0,-1,
        -0.5f,  0.5f, -0.5f,  0, 0,-1,
        // face gauche
        -0.5f, -0.5f, -0.5f, -1, 0, 0,
        -0.5f, -0.5f,  0.5f, -1, 0, 0,
        -0.5f,  0.5f,  0.5f, -1, 0, 0,
        -0.5f,  0.5f, -0.5f, -1, 0, 0,
        // face droite
         0.5f, -0.5f, -0.5f,  1, 0, 0,
         0.5f, -0.5f,  0.5f,  1, 0, 0,
         0.5f,  0.5f,  0.5f,  1, 0, 0,
         0.5f,  0.5f, -0.5f,  1, 0, 0,
        // face bas
        -0.5f, -0.5f, -0.5f,  0,-1, 0,
         0.5f, -0.5f, -0.5f,  0,-1, 0,
         0.5f, -0.5f,  0.5f,  0,-1, 0,
        -0.5f, -0.5f,  0.5f,  0,-1, 0,
        // face haut
        -0.5f,  0.5f, -0.5f,  0, 1, 0,
         0.5f,  0.5f, -0.5f,  0, 1, 0,
         0.5f,  0.5f,  0.5f,  0, 1, 0,
        -0.5f,  0.5f,  0.5f,  0, 1, 0
    };

    unsigned int indices[] = {
        0,1,2,  2,3,0,       // front
        4,5,6,  6,7,4,       // back
        8,9,10, 10,11,8,     // left
        12,13,14, 14,15,12,  // right
        16,17,18, 18,19,16,  // bottom
        20,21,22, 22,23,20   // top
    };

    Mesh mesh;
    glGenVertexArrays(1, &mesh.vao);
    glGenBuffers(1, &mesh.vbo);
    glGenBuffers(1, &mesh.ebo);

    glBindVertexArray(mesh.vao);

    glBindBuffer(GL_ARRAY_BUFFER, mesh.vbo);
    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, mesh.ebo);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);

    // position
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);
    // normal
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)(3 * sizeof(float)));
    glEnableVertexAttribArray(1);

    glBindVertexArray(0);

    mesh.indexCount = sizeof(indices)/sizeof(unsigned int);
    return mesh;
}

// TODO: générer une sphère (latitude/longitude) => même idée : positions, normales, indices.
Mesh createSphere(unsigned int X_SEGMENTS = 32, unsigned int Y_SEGMENTS = 16)
{
    std::vector<float> vertices;
    std::vector<unsigned int> indices;

    for (unsigned int y = 0; y <= Y_SEGMENTS; ++y) {
        for (unsigned int x = 0; x <= X_SEGMENTS; ++x) {
            float xSegment = (float)x / (float)X_SEGMENTS;
            float ySegment = (float)y / (float)Y_SEGMENTS;
            float xPos = std::cos(xSegment * 2.0f * M_PI) * std::sin(ySegment * M_PI);
            float yPos = std::cos(ySegment * M_PI);
            float zPos = std::sin(xSegment * 2.0f * M_PI) * std::sin(ySegment * M_PI);

            // position + normale (pour une sphère unité, normale = position normalisée)
            vertices.push_back(xPos);
            vertices.push_back(yPos);
            vertices.push_back(zPos);
            vertices.push_back(xPos);
            vertices.push_back(yPos);
            vertices.push_back(zPos);
        }
    }

    bool oddRow = false;
    for (unsigned int y = 0; y < Y_SEGMENTS; ++y) {
        for (unsigned int x = 0; x < X_SEGMENTS; ++x) {
            unsigned int i0 = y * (X_SEGMENTS + 1) + x;
            unsigned int i1 = i0 + X_SEGMENTS + 1;
            indices.push_back(i0);
            indices.push_back(i1);
            indices.push_back(i0 + 1);
            indices.push_back(i1);
            indices.push_back(i1 + 1);
            indices.push_back(i0 + 1);
        }
    }

    Mesh mesh;
    glGenVertexArrays(1, &mesh.vao);
    glGenBuffers(1, &mesh.vbo);
    glGenBuffers(1, &mesh.ebo);

    glBindVertexArray(mesh.vao);

    glBindBuffer(GL_ARRAY_BUFFER, mesh.vbo);
    glBufferData(GL_ARRAY_BUFFER, vertices.size()*sizeof(float), vertices.data(), GL_STATIC_DRAW);

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, mesh.ebo);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.size()*sizeof(unsigned int), indices.data(), GL_STATIC_DRAW);

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)(3 * sizeof(float)));
    glEnableVertexAttribArray(1);

    glBindVertexArray(0);
    mesh.indexCount = indices.size();
    return mesh;
}

// Prisme hexagonal simple: 12 sommets (haut+bas), indices pour faces.
Mesh createHexPrism()
{
    float radius = 0.6f;
    float halfHeight = 0.5f;

    std::vector<float> vertices;      // position + normal
    std::vector<unsigned int> indices;

    // 6 sommets haut + 6 sommets bas = 12 sommets
    // Normal des faces latérales : pointent vers l’extérieur
    for (int i = 0; i < 6; i++)
    {
        float angle = i * M_PI / 3.0f;  // 60° increments

        float x = radius * std::cos(angle);
        float z = radius * std::sin(angle);

        // normale pour face latérale = direction (x,0,z) normalisée
        glm::vec3 normal = glm::normalize(glm::vec3(x, 0.0f, z));

        // sommet du haut
        vertices.push_back(x);
        vertices.push_back(+halfHeight);
        vertices.push_back(z);
        vertices.push_back(normal.x);
        vertices.push_back(normal.y);
        vertices.push_back(normal.z);

        // sommet du bas
        vertices.push_back(x);
        vertices.push_back(-halfHeight);
        vertices.push_back(z);
        vertices.push_back(normal.x);
        vertices.push_back(normal.y);
        vertices.push_back(normal.z);
    }

    // === Indices pour les faces latérales ===
    // On connecte (haut_i, bas_i) à (haut_{i+1}, bas_{i+1})
    for (int i = 0; i < 6; i++)
    {
        int top_i = 2 * i;
        int bot_i = 2 * i + 1;
        int top_next = 2 * ((i + 1) % 6);
        int bot_next = 2 * ((i + 1) % 6) + 1;

        // quad composé de 2 triangles
        indices.push_back(top_i);
        indices.push_back(bot_i);
        indices.push_back(top_next);

        indices.push_back(bot_i);
        indices.push_back(bot_next);
        indices.push_back(top_next);
    }

    // === Sommets du dessus + dessous (centre + 6 points) ===

    // Ajout centre haut
    int centerTopIndex = vertices.size() / 6;
    vertices.push_back(0.0f);
    vertices.push_back(+halfHeight);
    vertices.push_back(0.0f);
    vertices.push_back(0.0f);
    vertices.push_back(1.0f);
    vertices.push_back(0.0f);

    // Ajout centre bas
    int centerBottomIndex = vertices.size() / 6;
    vertices.push_back(0.0f);
    vertices.push_back(-halfHeight);
    vertices.push_back(0.0f);
    vertices.push_back(0.0f);
    vertices.push_back(-1.0f);
    vertices.push_back(0.0f);

    // === Indices : face supérieure ===
    for (int i = 0; i < 6; i++)
    {
        int top_i = 2 * i;
        int top_next = 2 * ((i + 1) % 6);

        indices.push_back(centerTopIndex);
        indices.push_back(top_i);
        indices.push_back(top_next);
    }

    // === Indices : face inférieure ===
    for (int i = 0; i < 6; i++)
    {
        int bot_i = 2 * i + 1;
        int bot_next = 2 * ((i + 1) % 6) + 1;

        indices.push_back(centerBottomIndex);
        indices.push_back(bot_next);    // inversé pour garder winding CCW
        indices.push_back(bot_i);
    }

    // === Construction du mesh OpenGL ===
    Mesh mesh;
    glGenVertexArrays(1, &mesh.vao);
    glGenBuffers(1, &mesh.vbo);
    glGenBuffers(1, &mesh.ebo);

    glBindVertexArray(mesh.vao);

    glBindBuffer(GL_ARRAY_BUFFER, mesh.vbo);
    glBufferData(GL_ARRAY_BUFFER, vertices.size() * sizeof(float),
                 vertices.data(), GL_STATIC_DRAW);

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, mesh.ebo);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.size() * sizeof(unsigned int),
                 indices.data(), GL_STATIC_DRAW);

    // positions
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);

    // normales
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float),
                          (void*)(3 * sizeof(float)));
    glEnableVertexAttribArray(1);

    glBindVertexArray(0);

    mesh.indexCount = indices.size();
    return mesh;
}


// === Callbacks ===
void framebuffer_size_callback(GLFWwindow* window, int width, int height)
{
    glViewport(0, 0, width, height);
}

// === MAIN ===
int main()
{
    if (!glfwInit()) {
        std::cerr << "Erreur init GLFW\n";
        return -1;
    }

    // OpenGL 3.3 core
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow* window = glfwCreateWindow(800, 600, "OpenGL Objects", nullptr, nullptr);
    if (!window) {
        std::cerr << "Erreur création fenêtre\n";
        glfwTerminate();
        return -1;
    }
    glfwMakeContextCurrent(window);
    glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);

    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress)) {
        std::cerr << "Erreur init GLAD\n";
        return -1;
    }

    glEnable(GL_DEPTH_TEST);

    GLuint program = createShaderProgram("../shaders/basic.vert", "../shaders/basic.frag");

    Mesh cube   = createCube();
    Mesh sphere = createSphere();
    Mesh prism  = createHexPrism(); // à compléter

    // Matrices de base (caméra orbit autour de l’origine)
    float angle = 0.0f;

    while (!glfwWindowShouldClose(window)) {
        glfwPollEvents();

        angle += 0.5f * 0.01f; // caméra tourne doucement

        glClearColor(0.02f, 0.02f, 0.05f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        glUseProgram(program);

        // Caméra orbit
        glm::vec3 camPos = glm::vec3(3.0f * std::sin(angle), 1.5f, 3.0f * std::cos(angle));
        glm::mat4 view = glm::lookAt(camPos, glm::vec3(0.0f), glm::vec3(0,1,0));
        glm::mat4 proj = glm::perspective(glm::radians(45.0f), 800.f/600.f, 0.1f, 100.0f);

        GLint locModel = glGetUniformLocation(program, "uModel");
        GLint locView  = glGetUniformLocation(program, "uView");
        GLint locProj  = glGetUniformLocation(program, "uProj");
        GLint locLightPos = glGetUniformLocation(program, "uLightPos");
        GLint locViewPos  = glGetUniformLocation(program, "uViewPos");
        GLint locObjCol   = glGetUniformLocation(program, "uObjectColor");
        GLint locLightCol = glGetUniformLocation(program, "uLightColor");

        glUniformMatrix4fv(locView, 1, GL_FALSE, glm::value_ptr(view));
        glUniformMatrix4fv(locProj, 1, GL_FALSE, glm::value_ptr(proj));
        glUniform3f(locLightPos, 2.0f, 3.0f, 2.0f);
        glUniform3fv(locViewPos, 1, glm::value_ptr(camPos));
        glUniform3f(locLightCol, 1.0f, 1.0f, 1.0f);

        // === Dessiner le cube ===
        {
            glm::mat4 model = glm::translate(glm::mat4(1.0f), glm::vec3(-1.5f, 0.0f, 0.0f));
            glUniformMatrix4fv(locModel, 1, GL_FALSE, glm::value_ptr(model));
            glUniform3f(locObjCol, 0.2f, 0.7f, 1.0f);

            glBindVertexArray(cube.vao);
            glDrawElements(GL_TRIANGLES, cube.indexCount, GL_UNSIGNED_INT, 0);
        }

        // === Dessiner la sphère ===
        {
            glm::mat4 model = glm::mat4(1.0f);
            glUniformMatrix4fv(locModel, 1, GL_FALSE, glm::value_ptr(model));
            glUniform3f(locObjCol, 0.8f, 0.4f, 0.2f);

            glBindVertexArray(sphere.vao);
            glDrawElements(GL_TRIANGLES, sphere.indexCount, GL_UNSIGNED_INT, 0);
        }

        // === Dessiner le prisme hexagonal (quand tu l’auras implémenté) ===
        {
            glm::mat4 model = glm::translate(glm::mat4(1.0f), glm::vec3(1.5f, 0.0f, 0.0f));
            glUniformMatrix4fv(locModel, 1, GL_FALSE, glm::value_ptr(model));
            glUniform3f(locObjCol, 0.4f, 1.0f, 0.5f);

            glBindVertexArray(prism.vao);
            if (prism.indexCount > 0)
                glDrawElements(GL_TRIANGLES, prism.indexCount, GL_UNSIGNED_INT, 0);
        }

        glfwSwapBuffers(window);
    }

    glfwTerminate();
    return 0;
}
