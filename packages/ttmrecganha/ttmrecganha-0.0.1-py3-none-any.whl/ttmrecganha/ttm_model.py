#-----------------------------------------------------------------------
# IMPORTS
#-----------------------------------------------------------------------
from os import name
import tensorflow as tf

import keras
from keras import callbacks
from keras import layers

import pickle

import json
from pathlib import Path

#-----------------------------------------------------------------------
# VOCAB IMPORT
#-----------------------------------------------------------------------

def load_unique_client_dsc(configs):
    
    with open(configs["unique_client_dsc_path"], 'rb') as file:
        unique_client_dsc = pickle.load(file)
        
    return unique_client_dsc

def load_unique_client_id(configs):
        
    with open(configs["unique_client_id_path"], 'rb') as file:
        unique_client_id = pickle.load(file)
        
    return unique_client_id

def load_unique_offer_id(configs):
    
    with open(configs["unique_offer_id_path"], 'rb') as file:
        unique_offer_id = pickle.load(file)
        
    return unique_offer_id

#-----------------------------------------------------------------------
# TWO TOWER MODEL
#-----------------------------------------------------------------------

class TwoTowerModel:
    
    def __init__(self, configs):

        self.configs = configs
        self.max_tokens = 10000
        
        self.unique_client_id = load_unique_client_id(configs)
        self.unique_client_dsc = load_unique_client_dsc(configs)
        self.unique_offer_id = load_unique_offer_id(configs)
        
        self.model_path = configs["model_path"]
        
        self.model_creation()
        
    '''
    def setup_optimizer_and_loss_function(self):
        
        self.optimizer=tf.keras.optimizers.Adagrad(0.1)
        
        self.loss = tf.keras.losses.BinaryCrossentropy(
            from_logits=False,
            label_smoothing=0.0,
            axis=-1,
            reduction="auto",
            name="binary_cross-entropy",
        )
    '''
    
    def model_creation(self):
        
        #-----------------------------------------------------------------------
        # INPUTS
        #-----------------------------------------------------------------------
        
        client_dsc = keras.Input(shape=(1,), dtype=tf.string ,name='client_dsc')
        client_id = keras.Input(shape=(1,), dtype=tf.string, name='client_id')
        offer_id = keras.Input(shape=(1,), dtype=tf.string, name='offer_id')

        #-----------------------------------------------------------------------
        # CLIENT TOWER
        #-----------------------------------------------------------------------
        
        #CLIENT ID EMBEDDING
        client_id_vectorized = layers.StringLookup(vocabulary=self.unique_client_id, mask_token=None, name='client_id_vectorizer')(client_id)
        client_id_embedding = layers.Embedding(len(self.unique_client_id) + 1, 32, name='client_id_embedding')(client_id_vectorized)
        reshaped_client_id_embedding = layers.Reshape((32,), name='client_id_reshape')(client_id_embedding)
        
        #CLIENT DSC EMBEDDING
        client_dsc_vectorized = layers.TextVectorization(max_tokens=self.max_tokens, vocabulary= self.unique_client_dsc, name='client_dsc_vectorizer')(client_dsc)
        client_dsc_int_embedding = layers.Embedding(self.max_tokens, 32, mask_zero=True, name='client_dsc_embedding')(client_dsc_vectorized)
        client_dsc_embedding = layers.GlobalAveragePooling1D(name='client_dsc_pooling')(client_dsc_int_embedding)

        #CLIENT EMBEDDING
        client_embedding_concat = layers.Concatenate(axis=1, name='client_embedding_concat')([reshaped_client_id_embedding,client_dsc_embedding])
        
        #DENSE LAYERS
        client_int_embedding = layers.Dense(32, name='client_dense_1')(client_embedding_concat)
        client_embedding = layers.Dense(32, name='client_dense_2')(client_int_embedding)
        
        #-----------------------------------------------------------------------
        # OFFER TOWER
        #-----------------------------------------------------------------------
        
        #OFFER ID EMBEDDING
        offer_id_vectorized = layers.StringLookup(vocabulary=self.unique_offer_id, mask_token=None, name='offer_id_vectorizer')(offer_id)
        offer_id_embedding = layers.Embedding(len(self.unique_offer_id) + 1, 32, name='offer_id_embedding')(offer_id_vectorized)
        reshaped_offer_id_embedding = layers.Reshape((32,), name='offer_id_reshape')(offer_id_embedding)
      
        
        #OFFER DSC EMBEDDING
        offer_dsc_vectorized = layers.TextVectorization(max_tokens=self.max_tokens, vocabulary= self.unique_offer_id, name='offer_dsc_vectorizer')(offer_id)
        offer_dsc_int_embedding = layers.Embedding(self.max_tokens, 32, mask_zero=True, name='offer_dsc_embedding')(offer_dsc_vectorized)
        offer_dsc_embedding = layers.GlobalAveragePooling1D(name='offer_dsc_pooling')(offer_dsc_int_embedding)
        
        #OFFER EMBEDDING
        offer_embedding_concat = layers.Concatenate(axis=1, name='offer_embedding_concat')([reshaped_offer_id_embedding,offer_dsc_embedding])
        
        #DENSE LAYERS
        offer_int_embedding = layers.Dense(32, name='offer_dense_1')(offer_embedding_concat)
        offer_embedding = layers.Dense(32, name='offer_dense_2')(offer_int_embedding)
        
        #-----------------------------------------------------------------------
        # DOT PRODUCT
        #-----------------------------------------------------------------------
        
        similarity_score = layers.Dot(axes=1, normalize=True)([client_embedding, offer_embedding])
        
        #-----------------------------------------------------------------------
        # MODELS THAT RETURNS EMBEDDINGS
        #-----------------------------------------------------------------------
        
        client_embeddings = keras.Model(
            inputs = [client_dsc, client_id],
            outputs = client_embedding
        )
        
        offer_embeddings = keras.Model(
            inputs = offer_id,
            outputs = offer_embedding
        )
        
        self.client_embeddings = client_embeddings
        self.offer_embeddings = offer_embeddings
        
        #-----------------------------------------------------------------------
        # MODEL CREATION
        #-----------------------------------------------------------------------
        
        model = keras.Model(
            inputs = [client_dsc, client_id, offer_id],
            outputs = similarity_score
        )
        
        #-----------------------------------------------------------------------
        # MODEL COMPILE
        #-----------------------------------------------------------------------
        
        #self.setup_optimizer_and_loss_function()
        
        optimizer=tf.keras.optimizers.Adagrad(0.1)
        
        loss = tf.keras.losses.BinaryCrossentropy(
            from_logits=False,
            label_smoothing=0.0,
            axis=-1,
            reduction="auto",
            name="binary_cross-entropy",
        )
        
        model.compile(
            optimizer=optimizer,
            loss=loss,
            metrics=[tf.keras.metrics.BinaryCrossentropy(),
                     'accuracy', tf.keras.metrics.BinaryAccuracy(name='Acc.9', threshold=.5),
                     tf.keras.metrics.AUC(name='AUC'),
                     tf.keras.metrics.Recall(thresholds=.5, name='Recall.5'),
                     tf.keras.metrics.Precision(thresholds=.5, name='Precision.5')]
        )
        
        self.model = model

        return model