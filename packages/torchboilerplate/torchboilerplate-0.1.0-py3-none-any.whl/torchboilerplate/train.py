import os, argparse
import torch
import data_setup, engine, model_builder, utils

from torchvision import transforms

def train():
  # Get an arg for num_epochs
  parser = argparse.ArgumentParser(description="Get some hyperparameters.")
  parser.add_argument("--num_epochs", 
                      default=10, 
                      type=int, 
                      help="the number of epochs to train for")

  # Get an arg for batch_size
  parser.add_argument("--batch_size",
                      default=32,
                      type=int,
                      help="number of samples per batch")

  # Get an arg for hidden_units
  parser.add_argument("--hidden_units",
                      default=10,
                      type=int,
                      help="number of hidden units in hidden layers")

  # Get an arg for learning_rate
  parser.add_argument("--learning_rate",
                      default=0.001,
                      type=float,
                      help="learning rate to use for model")

  # Create an arg for training directory 
  parser.add_argument("--train_dir",
                      default="data/pizza_steak_sushi/train",
                      type=str,
                      help="directory file path to training data in standard image classification format")

  # Create an arg for test directory 
  parser.add_argument("--test_dir",
                      default="data/pizza_steak_sushi/test",
                      type=str,
                      help="directory file path to testing data in standard image classification format")
  
  args = parser.parse_args()
  
  NUM_EPOCHS = args.num_epochs
  BATCH_SIZE = args.batch_size
  HIDDEN_UNITS = args.hidden_units
  LEARNING_RATE = args.learning_rate
  train_dir = args.train_dir
  test_dir = args.test_dir
  device = "cuda" if torch.cuda.is_available() else "cpu"
  
  print('[INFO]')
  print(f'  \
        - EPOCHS : {NUM_EPOCHS}\n  \
        - BATCH SIZE : {BATCH_SIZE}\n  \
        - HIDDEN UNITS : {HIDDEN_UNITS}\n  \
        - LEARNING RATE : {LEARNING_RATE}\n  \
        - DEVICE : {device}'
        )
  

  

  # # Create transforms
  # data_transform = transforms.Compose([
  #   transforms.Resize((64, 64)),
  #   transforms.ToTensor()
  # ])

  # # Create DataLoaders 
  # train_dataloader, test_dataloader, class_names = data_setup.create_dataloaders(
  #                                                                                   train_dir=train_dir,
  #                                                                                   test_dir=test_dir,
  #                                                                                   transform=data_transform,
  #                                                                                   batch_size=BATCH_SIZE
  # )

  # # Instantiate model
  # model = model_builder.TinyVGG(
  #   input_shape=3,
  #   hidden_units=HIDDEN_UNITS,
  #   output_shape=len(class_names)
  #   ).to(device)


  # # Set loss and optimizer
  # loss_fn = torch.nn.CrossEntropyLoss()
  # optimizer = torch.optim.Adam(model.parameters(),
  #                              lr=LEARNING_RATE)
  
  # # Train
  # engine.train(model=model,
  #             train_dataloader=train_dataloader,
  #             test_dataloader=test_dataloader,
  #             loss_fn=loss_fn,
  #             optimizer=optimizer,
  #             epochs=NUM_EPOCHS,
  #             device=device)
  # print('Starting Saving')

  # # Save
  # utils.save_model(model=model,
  #                 target_dir="models",
  #                 model_name="05_going_modular_script_mode_tinyvgg_model.pth")
  

########################################################################   
if __name__ == '__main__':
  train()