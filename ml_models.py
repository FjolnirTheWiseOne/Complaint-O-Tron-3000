import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import IsolationForest
from textblob import TextBlob
from datetime import datetime
import random

# Define colors to match the UI
COLORS = {
    "bg_main": "#2E3440",
    "bg_secondary": "#3B4252",
    "text_primary": "#D8DEE9",
    "text_secondary": "#88C0D0",
    "accent": "#A3BE8C",
    "error": "#BF616A",
    "highlight": "#5E81AC",
}

class MLModels:
    def __init__(self, data_handler):
        """Initialize the ML models with data handler."""
        self.data_handler = data_handler
        self.vectorizer = TfidfVectorizer(max_features=100)
        self.kmeans = KMeans(n_clusters=3, random_state=42)
        self.logistic_regression = LogisticRegression(random_state=42)
        self.linear_regression = LinearRegression()
        self.isolation_forest = IsolationForest(contamination=0.1, random_state=42)
        self.complaints = []
        self.X_tfidf = None
        self.fit_models()

    def fit_models(self):
        """Fit the ML models with complaint data."""
        self.complaints = self.data_handler.get_all_complaints()
        if not self.complaints:
            return

        descriptions = [complaint['description'] for complaint in self.complaints]
        severities = [complaint['severity'] for complaint in self.complaints]
        categories = [complaint['category'] for complaint in self.complaints]
        complaint_lengths = [len(desc) for desc in descriptions]

        self.X_tfidf = self.vectorizer.fit_transform(descriptions).toarray()

        self.kmeans.fit(self.X_tfidf)

        X_features = np.column_stack((self.X_tfidf, severities, complaint_lengths))
        y_urgency = [1 if s >= 4 else 0 for s in severities]

        self.logistic_regression.fit(X_features, y_urgency)

        y_resolution = [s * 10 + random.uniform(-5, 5) for s in severities]
        self.linear_regression.fit(X_features, y_resolution)

        self.isolation_forest.fit(X_features)

    def predict_urgency(self):
        """Predict urgency of complaints using logistic regression."""
        if not self.complaints:
            return "No complaints to analyze", None

        descriptions = [complaint['description'] for complaint in self.complaints]
        severities = [complaint['severity'] for complaint in self.complaints]
        complaint_lengths = [len(desc) for desc in descriptions]
        X_tfidf = self.vectorizer.transform(descriptions).toarray()
        X_features = np.column_stack((X_tfidf, severities, complaint_lengths))

        predictions = self.logistic_regression.predict(X_features)
        high_urgency_count = sum(predictions)
        total_complaints = len(predictions)
        percentage = (high_urgency_count / total_complaints) * 100 if total_complaints > 0 else 0

        if percentage > 50:
            urgency = "High"
        elif percentage > 20:
            urgency = "Medium"
        else:
            urgency = "Low"

        details = f"{high_urgency_count}/{total_complaints} complaints are high urgency ({percentage:.1f}%)"
        return (urgency, details), predictions

    def plot_urgency(self, ax, predictions):
        """Plot a pie chart of urgency distribution with updated colors."""
        if not self.complaints:
            ax.text(0.5, 0.5, "No complaints to plot", ha='center', va='center', color=COLORS["text_primary"], fontfamily='Courier New')
            return "No complaints to plot"

        high_count = sum(predictions)
        low_count = len(predictions) - high_count
        labels = ['High Urgency', 'Low Urgency']
        sizes = [high_count, low_count]
        colors = [COLORS["error"], COLORS["accent"]]

        ax.clear()
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, textprops={'color': COLORS["text_primary"], 'fontfamily': 'Courier New', 'fontsize': 12})
        ax.set_title("Urgency Distribution", fontsize=14, color=COLORS["text_primary"], fontfamily='Courier New', fontweight='bold')
        ax.set_facecolor(COLORS["bg_main"])
        ax.figure.set_facecolor(COLORS["bg_main"])

        explanation = ("This pie chart shows the proportion of complaints classified as high urgency (severity >= 4) vs. low urgency.\n"
                       "A larger 'High Urgency' slice indicates more complaints that may need immediate attention.")
        return explanation

    def cluster_complaints(self):
        """Cluster complaints using K-Means and return cluster labels."""
        if not self.complaints:
            return [], "No complaints to cluster", None

        labels = self.kmeans.labels_
        cluster_counts = pd.Series(labels).value_counts().to_dict()
        explanation = "Clusters identified:\n"
        for cluster, count in cluster_counts.items():
            explanation += f"Cluster {cluster}: {count} complaints\n"
        return labels, explanation, cluster_counts

    def plot_clusters(self, ax, cluster_counts):
        """Plot a bar chart of complaint clusters with updated colors."""
        if not self.complaints:
            ax.text(0.5, 0.5, "No complaints to plot", ha='center', va='center', color=COLORS["text_primary"], fontfamily='Courier New')
            return "No complaints to plot"

        clusters = list(cluster_counts.keys())
        counts = list(cluster_counts.values())

        ax.clear()
        ax.bar(clusters, counts, color=COLORS["accent"], edgecolor=COLORS["text_primary"])
        ax.set_title("Complaints by Cluster", fontsize=14, color=COLORS["text_primary"], fontfamily='Courier New', fontweight='bold')
        ax.set_xlabel("Cluster", fontsize=12, color=COLORS["text_primary"], fontfamily='Courier New')
        ax.set_ylabel("Number of Complaints", fontsize=12, color=COLORS["text_primary"], fontfamily='Courier New')
        ax.set_facecolor(COLORS["bg_main"])
        ax.figure.set_facecolor(COLORS["bg_main"])
        ax.tick_params(axis='x', colors=COLORS["text_primary"], labelsize=10)
        ax.tick_params(axis='y', colors=COLORS["text_primary"], labelsize=10)
        for spine in ax.spines.values():
            spine.set_color(COLORS["text_primary"])

        explanation = ("This bar chart shows the number of complaints in each cluster.\n"
                       "Each cluster represents a group of complaints with similar themes based on their descriptions.")
        return explanation

    def predict_resolution_time(self):
        """Predict average resolution time using linear regression."""
        if not self.complaints:
            return 0, "No complaints to analyze", None

        descriptions = [complaint['description'] for complaint in self.complaints]
        severities = [complaint['severity'] for complaint in self.complaints]
        complaint_lengths = [len(desc) for desc in descriptions]
        X_tfidf = self.vectorizer.transform(descriptions).toarray()
        X_features = np.column_stack((X_tfidf, severities, complaint_lengths))

        predictions = self.linear_regression.predict(X_features)
        avg_resolution_time = np.mean(predictions)
        explanation = f"Average predicted resolution time: {avg_resolution_time:.2f} hours\nBased on severity, description length, and content."
        return avg_resolution_time, explanation, predictions

    def plot_resolution_time(self, ax, predictions):
        """Plot a histogram of predicted resolution times with updated colors."""
        if not self.complaints:
            ax.text(0.5, 0.5, "No complaints to plot", ha='center', va='center', color=COLORS["text_primary"], fontfamily='Courier New')
            return "No complaints to plot"

        ax.clear()
        ax.hist(predictions, bins=10, color=COLORS["accent"], edgecolor=COLORS["text_primary"])
        ax.set_title("Distribution of Predicted Resolution Times", fontsize=14, color=COLORS["text_primary"], fontfamily='Courier New', fontweight='bold')
        ax.set_xlabel("Resolution Time (hours)", fontsize=12, color=COLORS["text_primary"], fontfamily='Courier New')
        ax.set_ylabel("Number of Complaints", fontsize=12, color=COLORS["text_primary"], fontfamily='Courier New')
        ax.set_facecolor(COLORS["bg_main"])
        ax.figure.set_facecolor(COLORS["bg_main"])
        ax.tick_params(axis='x', colors=COLORS["text_primary"], labelsize=10)
        ax.tick_params(axis='y', colors=COLORS["text_primary"], labelsize=10)
        for spine in ax.spines.values():
            spine.set_color(COLORS["text_primary"])

        explanation = ("This histogram shows the distribution of predicted resolution times for all complaints.\n"
                       "A peak at a certain time indicates that many complaints are expected to take around that amount of time to resolve.")
        return explanation

    def analyze_sentiment(self):
        """Analyze sentiment of complaints using TextBlob."""
        if not self.complaints:
            return {}, "No complaints to analyze", None

        sentiments = {'positive': 0, 'neutral': 0, 'negative': 0}
        for complaint in self.complaints:
            description = complaint['description']
            polarity = TextBlob(description).sentiment.polarity
            if polarity > 0:
                sentiments['positive'] += 1
            elif polarity < 0:
                sentiments['negative'] += 1
            else:
                sentiments['neutral'] += 1

        total = sum(sentiments.values())
        explanation = "Sentiment distribution:\n"
        for sentiment, count in sentiments.items():
            percentage = (count / total) * 100 if total > 0 else 0
            explanation += f"{sentiment.capitalize()}: {count} complaints ({percentage:.1f}%)\n"
        return sentiments, explanation, sentiments

    def plot_sentiment(self, ax, sentiments):
        """Plot a donut chart of sentiment distribution with updated colors."""
        if not self.complaints:
            ax.text(0.5, 0.5, "No complaints to plot", ha='center', va='center', color=COLORS["text_primary"], fontfamily='Courier New')
            return "No complaints to plot"

        labels = list(sentiments.keys())
        sizes = list(sentiments.values())
        colors = [COLORS["accent"], COLORS["highlight"], COLORS["error"]]

        ax.clear()
        ax.pie(sizes, labels=[l.capitalize() for l in labels], colors=colors, autopct='%1.1f%%', startangle=90,
               textprops={'color': COLORS["text_primary"], 'fontfamily': 'Courier New', 'fontsize': 12}, wedgeprops=dict(width=0.3))
        ax.set_title("Sentiment Distribution", fontsize=14, color=COLORS["text_primary"], fontfamily='Courier New', fontweight='bold')
        ax.set_facecolor(COLORS["bg_main"])
        ax.figure.set_facecolor(COLORS["bg_main"])

        explanation = ("This donut chart shows the proportion of complaints with positive, neutral, and negative sentiments.\n"
                       "A large 'Negative' slice may indicate widespread dissatisfaction among users.")
        return explanation

    def detect_anomalies(self):
        """Detect anomalous complaints using Isolation Forest."""
        if not self.complaints:
            return [], "No complaints to analyze", None, None, None

        descriptions = [complaint['description'] for complaint in self.complaints]
        severities = [complaint['severity'] for complaint in self.complaints]
        complaint_lengths = [len(desc) for desc in descriptions]
        X_tfidf = self.vectorizer.transform(descriptions).toarray()
        X_features = np.column_stack((X_tfidf, severities, complaint_lengths))

        anomaly_labels = self.isolation_forest.predict(X_features)
        anomaly_ids = [complaint['id'] for i, complaint in enumerate(self.complaints) if anomaly_labels[i] == -1]
        explanation = f"Anomalous complaints detected: {len(anomaly_ids)}\nIDs: {', '.join(map(str, anomaly_ids)) if anomaly_ids else 'None'}\nAnomalies may indicate unusual severity or description patterns."
        return anomaly_ids, explanation, anomaly_labels, severities, complaint_lengths

    def plot_anomalies(self, ax, anomaly_labels, severities, complaint_lengths):
        """Plot a scatter plot of complaints with anomalies highlighted using updated colors."""
        if not self.complaints:
            ax.text(0.5, 0.5, "No complaints to plot", ha='center', va='center', color=COLORS["text_primary"], fontfamily='Courier New')
            return "No complaints to plot"

        normal_indices = [i for i, label in enumerate(anomaly_labels) if label == 1]
        anomaly_indices = [i for i, label in enumerate(anomaly_labels) if label == -1]

        ax.clear()
        ax.scatter([complaint_lengths[i] for i in normal_indices], [severities[i] for i in normal_indices],
                   color=COLORS["accent"], label='Normal', alpha=0.6)
        ax.scatter([complaint_lengths[i] for i in anomaly_indices], [severities[i] for i in anomaly_indices],
                   color=COLORS["error"], label='Anomaly', alpha=0.6)
        ax.set_title("Anomalies in Complaints", fontsize=14, color=COLORS["text_primary"], fontfamily='Courier New', fontweight='bold')
        ax.set_xlabel("Description Length", fontsize=12, color=COLORS["text_primary"], fontfamily='Courier New')
        ax.set_ylabel("Severity", fontsize=12, color=COLORS["text_primary"], fontfamily='Courier New')
        ax.set_facecolor(COLORS["bg_main"])
        ax.figure.set_facecolor(COLORS["bg_main"])
        ax.tick_params(axis='x', colors=COLORS["text_primary"], labelsize=10)
        ax.tick_params(axis='y', colors=COLORS["text_primary"], labelsize=10)
        ax.legend(facecolor=COLORS["bg_main"], edgecolor=COLORS["text_primary"], labelcolor=COLORS["text_primary"], fontsize=10)
        for spine in ax.spines.values():
            spine.set_color(COLORS["text_primary"])

        explanation = ("This scatter plot shows complaints by severity and description length.\n"
                       "Red points are anomalies, which may have unusual patterns (e.g., high severity, long descriptions) and might need special attention.")
        return explanation

    def plot_complaint_trends(self, ax):
        """Plot complaint trends over time with updated styling."""
        if not self.complaints:
            ax.text(0.5, 0.5, "No complaints to plot", ha='center', va='center')
            return

        dates = [datetime.strptime(complaint['date'], "%Y-%m-%d") for complaint in self.complaints]
        date_range = pd.date_range(min(dates), max(dates), freq='D')
        complaint_counts = pd.Series(0, index=date_range)
        for date in dates:
            complaint_counts[date] += 1

        ax.clear()
        ax.plot(date_range, complaint_counts, marker='o', color=COLORS["accent"], linewidth=2, markersize=8, label='Complaints')
        ax.set_title("Complaint Trends Over Time", fontsize=14, color=COLORS["text_primary"], fontfamily='Courier New', fontweight='bold')
        ax.set_xlabel("Date", fontsize=12, color=COLORS["text_primary"], fontfamily='Courier New')
        ax.set_ylabel("Number of Complaints", fontsize=12, color=COLORS["text_primary"], fontfamily='Courier New')
        ax.grid(True, linestyle='--', alpha=0.7, color=COLORS["bg_secondary"])
        ax.set_facecolor(COLORS["bg_main"])
        ax.figure.set_facecolor(COLORS["bg_main"])
        ax.tick_params(axis='x', rotation=45, colors=COLORS["text_primary"], labelsize=10)
        ax.tick_params(axis='y', colors=COLORS["text_primary"], labelsize=10)
        ax.legend(facecolor=COLORS["bg_main"], edgecolor=COLORS["text_primary"], labelcolor=COLORS["text_primary"], fontsize=10)
        for spine in ax.spines.values():
            spine.set_color(COLORS["text_primary"])

        ax.set_xticks(date_range[::7])
        ax.set_xticklabels([d.strftime('%Y-%m-%d') for d in date_range[::7]])

        explanation = ("This graph shows the number of complaints filed each day over time.\n"
                       "Peaks indicate days with higher complaint volumes, which may need further investigation.")

        return explanation

    def plot_category_distribution(self, ax):
        """Plot distribution of complaints by category with updated colors."""
        if not self.complaints:
            ax.text(0.5, 0.5, "No complaints to plot", ha='center', va='center')
            return

        categories = [complaint['category'] for complaint in self.complaints]
        category_counts = pd.Series(categories).value_counts()

        ax.clear()
        category_counts.plot(kind='bar', ax=ax, color=COLORS["accent"], edgecolor=COLORS["text_primary"])
        ax.set_title("Complaints by Category", fontsize=14, color=COLORS["text_primary"], fontfamily='Courier New', fontweight='bold')
        ax.set_xlabel("Category", fontsize=12, color=COLORS["text_primary"], fontfamily='Courier New')
        ax.set_ylabel("Number of Complaints", fontsize=12, color=COLORS["text_primary"], fontfamily='Courier New')
        ax.set_facecolor(COLORS["bg_main"])
        ax.figure.set_facecolor(COLORS["bg_main"])
        ax.tick_params(axis='x', colors=COLORS["text_primary"], labelsize=10)
        ax.tick_params(axis='y', colors=COLORS["text_primary"], labelsize=10)
        for spine in ax.spines.values():
            spine.set_color(COLORS["text_primary"])

        explanation = ("This bar chart shows the distribution of complaints across categories.\n"
                       "Categories with higher bars indicate areas that may need more attention.")

        return explanation