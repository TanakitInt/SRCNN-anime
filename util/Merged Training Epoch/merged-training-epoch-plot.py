import os
import json
import pandas as pd
from matplotlib import pyplot as plt

def prepare_json():

    # Parsing JSON ---
    with open("training_merged_1.json") as json_file:
        data = json.load(json_file)
    #print(data)

    # Read JSON as a dataframe ---
    df = pd.read_json("training_merged_1.json")
    #print(df)

    # export to csv ---
    df.to_csv("training.csv")
    print("Export to csv Done!")

def plot():

    df = pd.read_csv("training.csv")

    print(df)

    fig = plt.figure()

    plt.plot(df['loss'])
    plt.plot(df['val_loss'])
    plt.title('val_loss')
    plt.ylabel('val_loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
        
    # save fig and show
    plt.savefig('srcnn-anime_model_loss', dpi=120)
    plt.show()
    print("Training Fig Saved.")

    # summarize history for val_mean_squared_error
    fig = plt.figure()

    plt.plot(df['mean_squared_error'])
    plt.plot(df['val_mean_squared_error'])
    plt.title('val_mean_squared_error')
    plt.ylabel('val_mean_squared_error')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')

    # save fig and show
    plt.savefig('srcnn-anime_model_mean_squared_error', dpi=120)
    plt.show()
    print("Training Fig Saved.")


if __name__ == "__main__":

    prepare_json()
    plot()

