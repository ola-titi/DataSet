pip install translate

from translate import Translator
import pandas as pd

#stoplist = stopwords.words('arabic')

def main():
    training_data = "Test-propaganda-English.csv"
    #training_data = "B.csv"

    train_aug = pd.read_csv(training_data)

    translation11 = []

    for i in train_aug['span']: #FalseSent
        translator = Translator(from_lang="en", to_lang="ar")
        translation = translator.translate(i)


        print(translation)

if __name__ == "__main__":
    main()

