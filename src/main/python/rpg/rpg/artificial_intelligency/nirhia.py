import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

class ArtificialIntelligence:
    def __init__(self) -> None:
        self.__model: tf.keras.Sequential = tf.keras.Sequential()
    
    def train(self, training_data: pd.DataFrame, feature_to_predict: str, categories: list[str]):
        
        # Diviser les données en caractéristiques (features) et cible (target)
        features = training_data.drop(feature_to_predict, axis=1)  # Caractéristiques (distance, mana, has_wand, etc.)
        target = training_data[feature_to_predict]  # Cible (action de l'ennemi)

        # Encodage des variables catégorielles si nécessaire
        encoder = LabelEncoder()
        for category in categories:
            features[category] = encoder.fit_transform(features[category])  # Exemple pour 'distance', répéter pour les autres

        # Normalisation des données
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)

        # Diviser les données en ensembles d'entraînement et de test
        train_features, test_features, train_target, test_target = train_test_split(scaled_features, target, test_size=0.2, random_state=42)

        # Créer et entraîner le modèle avec TensorFlow (exemple basique)
        self.__model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=(train_features.shape[1],)),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(10, activation='softmax')  # Remplace '10' avec le nombre de classes d'actions possibles
        ])

        self.__model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        self.__model.fit(train_features, train_target, epochs=2, batch_size=32, validation_data=(test_features, test_target))    

    def predict(self, inputs: list):
        prediction = self.__model.predict(inputs)
        return prediction

class MasterSpellStrategistAI:
    def __init__(self) -> None:
        self.__ai: ArtificialIntelligence = ArtificialIntelligence()
        file_path = "./ia-magic-fight.csv"  # Remplace avec le chemin vers ton fichier CSV
        data: pd.DataFrame = pd.read_csv(file_path)
        to_be_predicted: str = "action"
        categories: list[str] = ["distance", "power", "has_weapon", "has_wand", "attackers"]
        self.__ai.train(data, to_be_predicted, categories)
    
    def purpose_fight_strategy(self, distance: int, power: int, has_weapon: bool, has_wand: bool, targets: int):
        return self.__ai.predict([[distance, power, int(has_weapon), int(has_wand), 0, targets]])


