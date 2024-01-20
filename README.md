# ecommerce-api-task
# Running the project

## With Docker

1. Build the docker image with the following command
   ```bash
   sudo docker build -t ecommerce-api-task .
   ```
2. Run the docker image
   ```bash
   sudo docker run -dit --rm -p 5000:80 ecommerce-api-task 
   ```
3. The service will be live on `http://127.0.0.1:5000`

## Without Docker
1. Setup the virtual environment
   ```bash
   python -m venv .venv
   ```
2. Activate the virtual environment
   ```bash
   source /.venv/bin/activate
   ```
3. Install all the dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Start the application
   ```bash
   flask run
   ```
5. The application will be live on `http://127.0.0.1:5000`
6. If you encounter any error, try using Python 3.10.0
