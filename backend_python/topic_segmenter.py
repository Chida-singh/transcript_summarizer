"""
Topic Segmenter Module
Segments text into topics using TF-IDF and K-Means clustering.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np


def calculate_optimal_topics(text):
    """
    Calculate optimal number of topics based on text length.
    
    Args:
        text (str): Full text to analyze
    
    Returns:
        int: Optimal number of topics (between 3 and 10)
    """
    word_count = len(text.split())
    
    # ~1 topic per 200 words
    num_topics = max(3, min(10, word_count // 200))
    
    print(f"Auto-calculating topics: {word_count} words → {num_topics} topics")
    return num_topics


def segment_into_topics(sentences, num_topics=None):
    """
    Segment sentences into different topics using TF-IDF and K-Means clustering.
    
    Args:
        sentences (list): List of sentences
        num_topics (int, optional): Number of topic groups. If None, auto-calculated.
    
    Returns:
        list: List of topic sections with sentences grouped together
    """
    try:
        if not sentences or len(sentences) == 0:
            return []
        
        # Auto-calculate topics if not provided
        if num_topics is None:
            full_text = ' '.join(sentences)
            num_topics = calculate_optimal_topics(full_text)
        
        # Adjust if we have fewer sentences than topics
        if len(sentences) < num_topics:
            num_topics = max(1, len(sentences) // 3)
        
        # Ensure at least 1 topic
        num_topics = max(1, num_topics)
        
        print(f"Segmenting {len(sentences)} sentences into {num_topics} topics...")
        
        # Vectorize sentences using TF-IDF
        vectorizer = TfidfVectorizer(
            max_features=100,
            stop_words='english',
            min_df=1,
            max_df=0.9
        )
        X = vectorizer.fit_transform(sentences)
        
        # Cluster sentences into topics
        kmeans = KMeans(
            n_clusters=num_topics,
            random_state=42,
            n_init=10
        )
        kmeans.fit(X)
        
        # Group sentences by cluster
        topics = {}
        for idx, label in enumerate(kmeans.labels_):
            if label not in topics:
                topics[label] = []
            topics[label].append({
                'index': idx,
                'text': sentences[idx]
            })
        
        # Sort topics by first sentence appearance
        topic_sections = []
        for topic_id in sorted(topics.keys(), key=lambda k: min(s['index'] for s in topics[k])):
            # Get top keywords for this cluster
            cluster_center = kmeans.cluster_centers_[topic_id]
            top_indices = cluster_center.argsort()[-3:][::-1]
            keywords = [vectorizer.get_feature_names_out()[i] for i in top_indices]
            
            topic_sentences = [
                s['text'] 
                for s in sorted(topics[topic_id], key=lambda x: x['index'])
            ]
            
            topic_sections.append({
                'topic_id': int(topic_id),
                'topic_name': f"Topic {topic_id + 1}: {', '.join(keywords)}",
                'keywords': keywords,
                'sentences': topic_sentences,
                'text': ' '.join(topic_sentences)
            })
        
        print(f"Successfully created {len(topic_sections)} topic sections")
        return topic_sections
        
    except Exception as e:
        print(f"Error segmenting topics: {str(e)}")
        import traceback
        traceback.print_exc()
        return []
