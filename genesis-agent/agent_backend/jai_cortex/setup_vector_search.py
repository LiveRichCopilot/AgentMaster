#!/usr/bin/env python3
"""
Setup script for Vertex AI Vector Search
Run this to provision the vector database for infinite memory
"""

import os
from google.cloud import aiplatform

PROJECT_ID = "studio-2416451423-f2d96"
LOCATION = "us-central1"

aiplatform.init(project=PROJECT_ID, location=LOCATION)

def create_vector_search_index():
    """Create a Vertex AI Vector Search index for conversation memory"""
    
    print("Creating Vertex AI Vector Search Index...")
    print("This provisions the vector database for infinite memory.")
    print()
    
    # Index configuration
    index_config = {
        "display_name": "jai-cortex-conversation-memory",
        "description": "Long-term memory for JAi Cortex OS - stores all conversations",
        "metadata": {
            "contentsDeltaUri": f"gs://{PROJECT_ID}-vector-memory/",
            "config": {
                "dimensions": 768,  # text-embedding-004 dimensions
                "approximateNeighborsCount": 150,
                "distanceMeasureType": "DOT_PRODUCT_DISTANCE",
                "algorithmConfig": {
                    "treeAhConfig": {
                        "leafNodeEmbeddingCount": 1000,
                        "leafNodesToSearchPercent": 10
                    }
                }
            }
        }
    }
    
    print(f"Index Name: jai-cortex-conversation-memory")
    print(f"Location: {LOCATION}")
    print(f"Embedding Dimensions: 768 (text-embedding-004)")
    print()
    print("To create this index, run:")
    print()
    print(f"""
gcloud ai indexes create \\
  --display-name="jai-cortex-conversation-memory" \\
  --description="Long-term memory for JAi Cortex OS" \\
  --metadata-file=vector_index_config.json \\
  --region={LOCATION} \\
  --project={PROJECT_ID}
    """)
    
    print()
    print("After index is created, create an endpoint:")
    print()
    print(f"""
gcloud ai index-endpoints create \\
  --display-name="jai-cortex-memory-endpoint" \\
  --region={LOCATION} \\
  --project={PROJECT_ID}
    """)
    
    print()
    print("⚠️  Note: Vector Search provisioning takes 30-60 minutes")
    print("For now, memory will use Firestore (slower but works immediately)")
    print()

if __name__ == "__main__":
    create_vector_search_index()

