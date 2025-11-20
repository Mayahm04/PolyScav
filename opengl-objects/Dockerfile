FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Dépendances pour build + OpenGL + GLFW + GLM
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    pkg-config \
    libgl1-mesa-dev \
    libx11-dev \
    libxrandr-dev \
    libxi-dev \
    libxinerama-dev \
    libxxf86vm-dev \
    libglfw3-dev \
    libglm-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier le projet dans l'image
WORKDIR /app
COPY . .

# Build CMake
RUN mkdir -p build && cd build && cmake .. && make -j4

# Lancer le binaire (le rendu OpenGL)
WORKDIR /app/build
CMD ["./opengl_objects"]
