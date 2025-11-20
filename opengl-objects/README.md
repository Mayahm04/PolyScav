# OpenGL – Cube, Sphère, Prisme hexagonal 

Ce projet affiche **trois objets 3D** en OpenGL core 3.3 :

- 🟦 Un **cube**
- 🟠 Une **sphère**
- 🟩 Un **prisme à base hexagonale**

Le tout avec :

- Pipeline moderne : **VAO/VBO/EBO**, shaders GLSL
- Caméra **orbit** autour de la scène
- Transformations **MVP** (Model / View / Projection)
- Éclairage **Blinn-Phong** dans le fragment shader (diffuse + spéculaire)
- Source de lumière ponctuelle + couleur d’objet paramétrable

---

##  Tech stack

- **OpenGL 3.3 Core**
- **GLFW** (fenêtre + contexte OpenGL)
- **GLAD** (loader OpenGL)
- **GLM** (matrices & vecteurs)
- **CMake** (build)
- **C++17**

---

## Exécution via Docker

### 1. Construire l'image

Depuis le dossier `opengl-objects/` :

```bash
docker build -t opengl-objects .
