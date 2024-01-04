import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

class GensimBertDataProcessor:
    def __init__(self, input_file=None, text_column=None, output_path=None):
        self.input_file = input_file or 'output/preprocessed.csv'
        self.text_column = text_column or 'text'
        self.corpus = None
        self.processed_corpus = []
        self.output_path = output_path or 'output/Preprocessed_text_GensimBert.csv'

    def clean(self, doc):
        stop = set(stopwords.words('english'))
        exclude = set(string.punctuation)
        wordnet_lemmatizer = WordNetLemmatizer()
        
        # Küçük harfe dönüştürme
        doc = doc.lower()
        
        # Noktalama işaretlerini kaldırma
        doc = ''.join(ch for ch in doc if ch not in exclude)
        
        # Stopword'leri kaldırma ve lemmatize etme
        cleaned_doc = " ".join(wordnet_lemmatizer.lemmatize(word) for word in doc.split() if word not in stop)
        
        return cleaned_doc

    def load_data(self):
        data = pd.read_csv(self.input_file)
        self.corpus = data[self.text_column].dropna().tolist()

    def preprocess(self):
        # Her bir doküman için temizleme işlemini uygula
        cleaned_corpus = [self.clean(doc) for doc in self.corpus]
        self.processed_corpus = cleaned_corpus

    def save_preprocessed_data(self):
        preprocessed_df = pd.DataFrame({'text': self.processed_corpus})
        preprocessed_df.to_csv(self.output_path, index=False)

    def run(self):
        self.load_data()
        self.preprocess()
        self.save_preprocessed_data()

# Veri yükleme ve işleme (varsayılan değerlerle)
# bert_preprocessor = GensimBertDataProcessor()
# bert_preprocessor.run()
