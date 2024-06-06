# Hands-up API

This is a FastAPI demo application that detects if a person on the given image has 
thier hands above their head. 

## Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your machine.
- [Git](https://git-scm.com/) installed on your machine.

# Using the script

### Script was tested on Ubuntu, but it should also work on MacOS

To get started, you can download the script using one of this methods:

```
wget https://github.com/Aca-F/Hands-up-api/blob/main/startup_script.sh
```

```
curl -O https://github.com/Aca-F/Hands-up-api/blob/main/startup_script.sh
```
Or manually from this [link](https://github.com/Aca-F/Hands-up-api/blob/main/startup_script.sh).


## Running the Application

Before running the application, you need to build the Docker image and run the container. Use the provided script to automate these steps.

1. Make the script executable:

```
chmod +x startup_script.sh
```

2. Run the script:

```
./startup_script.sh
```

When you run the script, you will be asked for the confirmation to download clone
the repository and buld a Docker image. Afterwards you will see the following menu options:

1. **Run tests**: This option will execute the tests using `pytest`.
2. **Run application**: This option will run the application in a Docker container. The application will be available at `http://localhost:8000`.
3. **Quit**: This option will exit the script.

Choose the appropriate option by entering the corresponding number.



> **_NOTE:_**  The script will delete the cloned files, docker container and docker image when it is closed.
---

# Running the Application Manually

If you prefer to run the application manually, follow these steps to run the app:

1. **Clone the repository**:

```
git clone https://github.com/Aca-F/Hands-up-api.git
cd Hands-up-api
```

2. **Build the Docker image**:

```
docker build -t aleksandar-hands-up .
```

3. **Run the Docker container**:

```
docker run --name aleksandar-hands-up-container -d -p 8000:8000 aleksandar-hands-up
```

The application will be available at `http://localhost:8000`.

## Running Tests

To run the tests manually use the following commands:

1. **Clone the repository**:

```
git clone https://github.com/Aca-F/Hands-up-api.git
cd Hands-up-api
```

2. **Build the Docker image**:

```
docker build -t aleksandar-hands-up .
```

3. **Run the tests**:

```
docker run --rm aleksandar-hands-up pytest -v
```

### Cleanup


1. **Stop and remove the Docker container**:

```
docker stop aleksandar-hands-up-container
docker rm aleksandar-hands-up-container
```

2. **Remove the Docker image**:

```
docker rmi aleksandar-hands-up
```
