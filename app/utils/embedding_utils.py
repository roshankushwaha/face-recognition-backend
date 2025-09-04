import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import numpy as np

# Load model
def load_model(pb_path):
    graph = tf.Graph()
    with graph.as_default():
        with tf.gfile.GFile(pb_path, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            tf.import_graph_def(graph_def, name='')
    return graph

# Load once
model_path = "app/models/20180408-102900.pb"
graph = load_model(model_path)
sess = tf.Session(graph=graph)

# Grab tensors
input_tensor = graph.get_tensor_by_name("input:0")
embeddings_tensor = graph.get_tensor_by_name("embeddings:0")
phase_tensor = graph.get_tensor_by_name("phase_train:0")

def get_face_embedding(face_img):
    """Takes 160x160 normalized face and returns 128D embedding"""
    feed_dict = {
        input_tensor: [face_img],
        phase_tensor: False
    }
    embedding = sess.run(embeddings_tensor, feed_dict=feed_dict)
    return embedding[0]


# Cosine Similarity
def cosine_similarity(emb1, emb2):
    dot = np.dot(emb1, emb2)
    norm1 = np.linalg.norm(emb1)
    norm2 = np.linalg.norm(emb2)
    return dot / (norm1 * norm2)
