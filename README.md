# Receipt Processor API

This is a receipt processor built with FastAPI. It processes receipts and returns the points awarded for each receipt.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- [Docker](https://www.docker.com/get-started) (for running the container)
- [Git](https://git-scm.com/) (for cloning the repository)

## Clone the Repository

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/vrajendr-official/receipt-processor.git
   cd receipt-processor
   
2. Building the Docker Image:
In the root directory of the repository, where the Dockerfile is located, run the following command to build the Docker image:
   ```bash
   docker build -t receipt-processor .
   
3. Running the Application in Docker
	1.	Run the Docker Container:
After building the image, run the following command to start the container. This command will expose port 8000 (for FastAPI) inside the container and map it to port 8000 on your local machine:
   ```bash
   docker run -d -p 8000:8000 receipt-processor
   
4. 	Accessing the API:
After the container starts, you can access the FastAPI application in your browser or via curl:
	
API Documentation (Swagger UI):
Visit the following URL in your browser:
    http://localhost:8000/docs

ReDoc Documentation:
You can also view the API documentation in ReDoc format here:
http://localhost:8000/redoc
6. Running Automated Tests Inside Docker Container:
```bash
   docker run --rm receipt-processor pytest test/
   ```
   
7. Running Tests Locally (Optional):
If you have pytest installed locally, you can run the tests directly from your local machine using:
```bash
       pytest test/
```
8. Stopping the container

```bash 
docker stop receipt-processor
```

