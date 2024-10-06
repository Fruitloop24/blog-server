import azure.functions as func
import logging
import subprocess

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="run_main")
def run_main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Run main.py
        subprocess.run(["python3", "main.py"], check=True)
        return func.HttpResponse(
            "main.py executed successfully!",
            status_code=200
        )
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running main.py: {e}")
        return func.HttpResponse(
            f"Failed to execute main.py. Error: {e}",
            status_code=500
        )
