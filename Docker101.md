# Docker 101

A practical introduction to Docker: what it is, why it exists, how it works under the hood, and the everyday commands you need to get productive.

---

## Table of Contents

1. [Why do we need Docker?](#why-do-we-need-docker)
2. [How does Docker work?](#how-does-docker-work)
3. [Docker architecture](#docker-architecture)
4. [Images vs Containers](#images-vs-containers)
5. [Installing Docker](#installing-docker)
6. [Essential Docker commands](#essential-docker-commands)
7. [Image tags](#image-tags)
8. [Port mapping](#port-mapping)
9. [Volumes and bind mounts](#volumes-and-bind-mounts)
10. [Inspecting containers and reading logs](#inspecting-containers-and-reading-logs)
11. [Building your own image (Dockerfile)](#building-your-own-image-dockerfile)

---

## Why do we need Docker?

A typical application is made of several moving parts — a **frontend**, a **backend**, and a **database**. Each of these often needs its own runtime, library versions, and setup steps. Installing and maintaining all of that by hand on every developer laptop, test server, and production machine quickly leads to the classic problem:

> *"It works on my machine."*

Docker solves this by packaging an application **together with everything it needs to run** — a minimal OS userland, libraries, dependencies, configuration, and the start-up command — into a single portable unit. The only thing a machine needs is Docker itself. The same package then runs identically everywhere.

```mermaid
flowchart LR
    subgraph Without["❌ Without Docker"]
        direction TB
        D1[Developer laptop<br/>Node 18, Python 3.10, MySQL 8.0]
        D2[Test server<br/>Node 16, Python 3.8, MySQL 5.7]
        D3[Production<br/>Node 20, Python 3.11, MySQL 8.4]
    end

    subgraph With["✅ With Docker"]
        direction TB
        I[(Same Docker image)]
        I --> E1[Developer laptop]
        I --> E2[Test server]
        I --> E3[Production]
    end

    Without -. "version drift,<br/>manual setup" .-> With
```

**Key benefits**

- **Consistency** — identical environment from development to production.
- **Isolation** — each app runs in its own container with its own dependencies; no conflicts.
- **Speed** — containers start in seconds, far faster than virtual machines.
- **Portability** — run anywhere Docker is installed: laptop, on-prem server, or cloud.

---

## How does Docker work?

Unlike a virtual machine, a container does **not** bundle a full operating system with its own kernel. Instead, all containers on a host **share the host's OS kernel**, and each container only brings its own userland (filesystem, libraries, binaries).

This has two important consequences:

- On a **Linux** host, you can run containers based on any Linux distribution — Ubuntu, Fedora, Alpine, Debian, etc. — because they all use the Linux kernel.
- You **cannot** run a Windows container on a Linux kernel (and vice versa), because the kernel is different.

> **Note:** On macOS and Windows, Docker Desktop quietly runs a lightweight Linux VM in the background so that Linux containers can still share a Linux kernel.

### Containers vs Virtual Machines

```mermaid
flowchart TB
    subgraph VM["Virtual Machines"]
        direction TB
        VA["App A<br/>Libs / Bins"] --- VGA[Guest OS]
        VB["App B<br/>Libs / Bins"] --- VGB[Guest OS]
        VGA --- HV[Hypervisor]
        VGB --- HV
        HV --- VHOS[Host OS]
        VHOS --- VHW[Hardware]
    end

    subgraph CT["Containers"]
        direction TB
        CA["App A<br/>Libs / Bins"] --- DE[Docker Engine]
        CB["App B<br/>Libs / Bins"] --- DE
        DE --- CHOS["Host OS (shared kernel)"]
        CHOS --- CHW[Hardware]
    end
```

| | Virtual Machine | Container |
|---|---|---|
| Includes a full guest OS | Yes | No — shares host kernel |
| Typical size | Gigabytes | Megabytes |
| Start-up time | Minutes | Seconds |
| Isolation level | Strong (hardware-level) | Process-level |

---

## Docker architecture

Docker follows a **client–server** model:

- **Docker Client (CLI)** — the `docker` command you type. It sends requests to the daemon.
- **Docker Daemon (`dockerd`)** — the background service that actually builds images, runs containers, and manages networks and volumes.
- **Registry** — a remote store for images (e.g. Docker Hub, GitHub Container Registry, AWS ECR).

```mermaid
flowchart LR
    subgraph Client["Docker Client"]
        C1["docker build"]
        C2["docker pull"]
        C3["docker run"]
    end

    subgraph Host["Docker Host"]
        DM[["Docker Daemon<br/>(dockerd)"]]
        subgraph Images
            IM1[nginx]
            IM2[mysql]
            IM3[my-app]
        end
        subgraph Containers
            CT1((nginx))
            CT2((mysql))
            CT3((my-app))
        end
        DM --> Images
        Images --> Containers
    end

    subgraph Registry["Registry (Docker Hub / GHCR / ECR)"]
        R1[nginx]
        R2[mysql]
        R3[...]
    end

    C1 --> DM
    C2 --> DM
    C3 --> DM
    DM <-- "pull / push" --> Registry
```

### The layered stack

```mermaid
flowchart TB
    APP["Application<br/>(code + libraries + dependencies)"]
    DOCKER["Docker Engine"]
    OS["Host Operating System (kernel)"]
    HW["Hardware Infrastructure"]
    APP --> DOCKER --> OS --> HW
```

---

## Images vs Containers

| | Image | Container |
|---|---|---|
| What it is | A **read-only template** containing the app, its dependencies, and configuration | A **running (or stopped) instance** of an image |
| Analogy | A class / a recipe | An object / the cooked dish |
| Mutable? | No | Yes — has a thin writable layer on top |
| Created by | `docker build` or `docker pull` | `docker run` |

One image can be used to start **many** containers:

```mermaid
flowchart LR
    DF[Dockerfile] -- "docker build" --> IMG[(Image)]
    IMG -- "docker run" --> C1((Container 1))
    IMG -- "docker run" --> C2((Container 2))
    IMG -- "docker run" --> C3((Container 3))
    IMG -- "docker push" --> REG[(Registry)]
    REG -- "docker pull" --> IMG
```

---

## Installing Docker

Follow the official guide for your platform: **https://docs.docker.com/engine/install/**

Quick install on most Linux distributions (official convenience script):

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

Allow your user to run Docker without `sudo` (log out and back in afterwards):

```bash
sudo usermod -aG docker $USER
```

Verify the installation:

```bash
docker --version
docker run hello-world
```

### 🛠️ Planned: automated install script

A helper script will be added to this repository to make installation one step. It will:

1. Detect the operating system and distribution.
2. Detect the CPU architecture (`x86_64`, `arm64`, …).
3. Install the matching Docker version.
4. Verify that the Docker service is running.
5. Print a short list of commands to get started.

---

## Essential Docker commands

Replace values in `<angle brackets>` with your own.

### Run containers

Run a container in the foreground:

```bash
docker run nginx
```

Run a container in the background (detached) with a friendly name:

```bash
docker run -d --name my-nginx nginx
```

Run a container and open an interactive shell inside it:

```bash
docker run -it ubuntu bash
```

### List images and containers

List images stored locally:

```bash
docker images
```

List running containers:

```bash
docker ps
```

List all containers, including stopped ones:

```bash
docker ps -a
```

### Download images

```bash
docker pull nginx:1.27
```

### Interact with a running container

Run a command inside a running container (e.g. open a shell):

```bash
docker exec -it <container> sh
```

Attach your terminal to the container's main process:

```bash
docker attach <container>
```

### Stop and remove

Stop a running container:

```bash
docker stop <container>
```

Remove a stopped container:

```bash
docker rm <container>
```

Remove an image (no container may be using it):

```bash
docker rmi <image>
```

Clean up all stopped containers, unused networks, dangling images, and build cache:

```bash
docker system prune
```

### Quick reference

| Command | Purpose |
|---|---|
| `docker run` | Create and start a container |
| `docker run -d` | Run in the background (detached) |
| `docker images` | List local images |
| `docker ps` / `docker ps -a` | List running / all containers |
| `docker pull` | Download an image from a registry |
| `docker exec` | Run a command inside a running container |
| `docker attach` | Attach to a container's main process |
| `docker stop` | Stop a running container |
| `docker rm` | Remove a container |
| `docker rmi` | Remove an image |
| `docker inspect` | Show detailed configuration (JSON) |
| `docker logs` | Show container output |
| `docker system prune` | Remove unused data |

### Container lifecycle

```mermaid
stateDiagram-v2
    [*] --> Created: docker create
    [*] --> Running: docker run
    Created --> Running: docker start
    Running --> Paused: docker pause
    Paused --> Running: docker unpause
    Running --> Stopped: docker stop
    Stopped --> Running: docker start
    Stopped --> [*]: docker rm
```

---

## Image tags

A **tag** identifies a specific version of an image, written as `image:tag`. If you omit the tag, Docker uses `latest`.

Pull the `latest` tag (implicit):

```bash
docker pull mysql
```

Pull a specific, pinned version:

```bash
docker pull mysql:8.4
```

> ⚠️ **Avoid `latest` in production.** `latest` is convenient for experiments, but it is a moving target — the next time you redeploy, Docker may pull a newer version containing breaking changes. Always pin an explicit version tag in production so deployments are predictable and reproducible.

---

## Port mapping

Containers run on an isolated network. To reach an application inside a container from your machine (or the outside world), you **publish** a container port to a host port with `-p <host_port>:<container_port>`.

```mermaid
flowchart LR
    U[Browser / Client] -- "localhost:5000" --> HP["Host port 5000"]
    HP -- "maps to" --> CP["Container port 80"]
    subgraph C["Container: nginx"]
        CP --> APP[Web server]
    end

    U2[DB client] -- "localhost:3434" --> HP2["Host port 3434"]
    HP2 -- "maps to" --> CP2["Container port 3306"]
    subgraph D["Container: mysql"]
        CP2 --> DB[(MySQL)]
    end
```

Expose a web server running on port `80` inside the container at port `5000` on the host:

```bash
docker run -d -p 5000:80 nginx
```

Expose a MySQL database running on port `3306` inside the container at port `3434` on the host:

```bash
docker run -d -p 3434:3306 -e MYSQL_ROOT_PASSWORD=secret mysql:8.4
```

> **Note:** A host port can only be used by **one** container at a time. To run two web servers, map them to different host ports (e.g. `5000:80` and `5001:80`). The *container* ports can be the same, because each container has its own isolated network.

---

## Volumes and bind mounts

A container's filesystem is **ephemeral**: anything written inside it is lost when the container is removed. For data that must survive — databases, uploads, logs — store it **outside** the container and mount it in.

```mermaid
flowchart LR
    subgraph Host["Host machine"]
        HD["/opt/datadir"]
        VOL[("Docker volume<br/>mysql-data")]
    end
    subgraph C1["Container A (mysql)"]
        P1["/var/lib/mysql"]
    end
    subgraph C2["Container B (new mysql)"]
        P2["/var/lib/mysql"]
    end
    HD <-- "bind mount" --> P1
    HD <-. "reuse same data<br/>after A is removed" .-> P2
```

There are two main ways to persist data:

| Type | Where the data lives | Best for |
|---|---|---|
| **Bind mount** | A specific path you choose on the host | Local development, sharing source code or config |
| **Named volume** | Managed by Docker (`/var/lib/docker/volumes/...`) | Databases and production data |

### Using `-v` (short syntax)

Separate the host path and container path with a colon (`:`):

```bash
docker run -d -v /opt/datadir:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=secret mysql:8.4
```

### Using `--mount` (explicit syntax)

More verbose but clearer — each option is named:

```bash
docker run -d --mount type=bind,source=/opt/datadir,target=/var/lib/mysql -e MYSQL_ROOT_PASSWORD=secret mysql:8.4
```

### Using a named volume

Create a volume managed by Docker:

```bash
docker volume create mysql-data
```

Mount it into a container:

```bash
docker run -d -v mysql-data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=secret mysql:8.4
```

Because the data lives outside the container, you can remove the container and start a new one pointing at the same path or volume — your data is still there.

---

## Inspecting containers and reading logs

View the full configuration of a container (network, mounts, environment variables, state) as JSON:

```bash
docker inspect <container>
```

View a container's output (stdout/stderr):

```bash
docker logs <container>
```

Follow the logs live, like `tail -f`:

```bash
docker logs -f <container>
```

Show only the last 100 lines:

```bash
docker logs --tail 100 <container>
```

---

## Building your own image (Dockerfile)

Docker Hub (https://hub.docker.com) has ready-made images for most popular software. When no suitable image exists for your application, you build your own using a **Dockerfile** — a plain text file containing step-by-step instructions. Each instruction creates a new **layer** in the image, and layers are cached to make rebuilds fast.

### Common Dockerfile instructions

| Instruction | Purpose |
|---|---|
| `FROM` | Sets the base image (an OS like `ubuntu`, or a runtime like `python:3.12-slim`). **Every Dockerfile must start with `FROM`.** |
| `WORKDIR` | Sets the working directory for subsequent instructions. |
| `RUN` | Executes a command at build time (e.g. install packages). |
| `COPY` | Copies files from your machine (the build context) into the image. |
| `ENV` | Sets environment variables available inside the container. |
| `EXPOSE` | Documents which port the application listens on. |
| `ENTRYPOINT` / `CMD` | The command that runs when a container starts from the image. |

### Example Dockerfile

```dockerfile
# 1. Base image
FROM python:3.12-slim

# 2. Working directory inside the image
WORKDIR /app

# 3. Install dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the application source code
COPY . .

# 5. Environment variables
ENV APP_ENV=production

# 6. Port the app listens on
EXPOSE 8000

# 7. Command to run when the container starts
ENTRYPOINT ["python", "app.py"]
```

### Build → Run → Push workflow

```mermaid
flowchart LR
    A[Write Dockerfile] --> B["docker build"]
    B --> C[(Local image)]
    C --> D["docker run<br/>(test locally)"]
    C --> E["docker tag"]
    E --> F["docker push"]
    F --> G[(Registry<br/>Docker Hub / GHCR / ECR)]
    G --> H["docker pull<br/>on any server"]
```

Build the image from the Dockerfile in the current directory and give it a name and tag:

```bash
docker build -t my-app:1.0 .
```

Run it locally to test:

```bash
docker run -d -p 8000:8000 my-app:1.0
```

Log in to your registry (Docker Hub shown here):

```bash
docker login
```

Tag the image with your registry username/repository:

```bash
docker tag my-app:1.0 <your-username>/my-app:1.0
```

Push it to the registry:

```bash
docker push <your-username>/my-app:1.0
```

Anyone with access can now pull and run the exact same image on any machine with Docker installed.
