## Code for calling the other sctripts

from pipeline import ingest, transform, serve
import os

def main(ID):
    data_path = os.path.join(
        '/home',
        'gabriel',
        'code',
        'aim-training-data',
        'data',
        ID
    )

    # Define the source address
    source_path = os.path.join(
        data_path,
        'source'
    )

    # Define the ingested data adress
    ingested_path = os.path.join(
        data_path,
        'ingested'
    )

    ingest(
        input_folder = source_path,
        output_folder = ingested_path
    )

    # Define the transformed data adress
    transformed_path = os.path.join(
        data_path,
        'transformed'
    )

    transform(
        input_folder = ingested_path,
        output_folder = transformed_path
    )

    # Define the served data adress
    served_path = os.path.join(
        data_path,
        'served'
    )

    serve(
        input_folder = transformed_path,
        output_folder = served_path
    )

if __name__ == "__main__":
    ID = '1'

    main(ID)
    