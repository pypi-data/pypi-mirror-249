import typer
import torch
import data_setup
import engine
import model_builder
import utils
from torchvision import transforms

app = typer.Typer()

@app.command()
def train(num_epochs : int = 10,
          batch_size: int = 32,
          hidden_units: int = 10,
          learning_rate: float = 0.001,
          train_dir: str = "data/pizza_steak_sushi/train",
          test_dir: str = "data/pizza_steak_sushi/test"
          ):
    
    device = "cuda" if torch.cuda.is_available() else "cpu"

    print('[INFO]')
    print(f'  \
          - EPOCHS : {num_epochs}\n  \
          - BATCH SIZE : {batch_size}\n  \
          - HIDDEN UNITS : {hidden_units}\n  \
          - LEARNING RATE : {learning_rate}\n  \
          - DEVICE : {device}'
          )

if __name__ == "__main__":
    app()
    # typer.run(train)
