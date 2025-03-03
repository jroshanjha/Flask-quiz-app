# 2. Machine Learning Pipeline Example
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# 4. API Implementation with FastAPI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# 3. NLP Processing Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import re

app = FastAPI()

class FinancialModelPipeline:
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = RandomForestRegressor(n_estimators=100)
        
    def preprocess_data(self, data):
        """
        Feature engineering for financial data
        """
        # Calculate moving averages
        data['MA5'] = data['close'].rolling(window=5).mean()
        data['MA20'] = data['close'].rolling(window=20).mean()
        
        # Calculate price momentum
        data['momentum'] = data['close'].pct_change()
        
        # Calculate volatility
        data['volatility'] = data['close'].rolling(window=20).std()
        
        # Drop NaN values
        return data.dropna()
    
    def prepare_features(self, data):
        """
        Prepare feature matrix X and target vector y
        """
        feature_columns = ['MA5', 'MA20', 'momentum', 'volatility']
        X = data[feature_columns]
        y = data['close'].shift(-1)  # Next day's price as target
        return X[:-1], y[:-1]  # Remove last row due to shift
    
    def train(self, X, y):
        """
        Train the model
        """
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
    
    def predict(self, X):
        """
        Make predictions
        """
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)

class FinancialNewsAnalyzer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000)
        self.classifier = MultinomialNB()
    
    def preprocess_text(self, text):
        """
        Clean and preprocess text data
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def train(self, texts, labels):
        """
        Train the sentiment analyzer
        """
        # Preprocess all texts
        processed_texts = [self.preprocess_text(text) for text in texts]
        
        # Convert texts to TF-IDF features
        X = self.vectorizer.fit_transform(processed_texts)
        
        # Train classifier
        self.classifier.fit(X, labels)
    
    def predict_sentiment(self, text):
        """
        Predict sentiment of new text
        """
        processed_text = self.preprocess_text(text)
        X = self.vectorizer.transform([processed_text])
        return self.classifier.predict(X)[0]

class StockPredictionRequest(BaseModel):
    features: List[float]

class NewsAnalysisRequest(BaseModel):
    text: str

@app.post("/predict/stock")
async def predict_stock(request: StockPredictionRequest):
    try:
        # Assuming we have an instance of FinancialModelPipeline called model
        model = FinancialModelPipeline()
        prediction = model.predict(np.array(request.features).reshape(1, -1))
        return {"predicted_price": float(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/news")
async def analyze_news(request: NewsAnalysisRequest):
    try:
        # Assuming we have an instance of FinancialNewsAnalyzer called analyzer
        analyzer = FinancialNewsAnalyzer()
        sentiment = analyzer.predict_sentiment(request.text)
        return {"sentiment": sentiment}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))