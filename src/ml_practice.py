import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# trial data
data = {
    'prompt_length': [50, 80, 120, 30, 90, 110, 70, 60],
    'clarity_score': [7, 8, 9, 5, 8, 9, 7, 6],
    'response_quality': [6.5, 7.8, 8.9, 4.5, 7.5, 8.7, 6.8, 6.0]
}
df = pd.DataFrame(data)

# Features and target
X = df[['prompt_length', 'clarity_score']]
y = df['response_quality']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
print("R2 Score:", r2_score(y_test, y_pred))
print("MSE:", mean_squared_error(y_test, y_pred))
