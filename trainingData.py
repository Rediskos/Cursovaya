import os
import cv2
import torch
from torch.autograd import Variable
import numpy as np
import torch.functional as F
import torch.nn.functional as F
from tqdm import tqdm

REBUILD_DATA = True




class tr():
    SPORT = "BD_articles/SportArticles"
    MEDIC = "BD_articles/MedArticles"
    MATH = "BD_articles/MathArticles"
    LABELS = {SPORT: 0, MEDIC: 1, MATH: 2}
    training_data = []
    SPORTcount = 0
    MEDICcount = 0
    MATHcount = 0
    
    def get_input_layer(self, word_idx, vocabulary_size):
        x = torch.zeros(vocabulary_size).float()
        x[word_idx] = 1.0
        return x
    
    def word2vec(self, words):
        vocabulary = []
        for token in words:
            if token not in vocabulary:
                vocabulary.append(token)
        
        word2idx = {w: idx for (idx, w) in enumerate(vocabulary)}
        idx2word = {idx: w for (idx, w) in enumerate(vocabulary)}
        
        vocabulary_size = len(vocabulary)
        
        
        window_size = 2
        idx_pairs = []
        
        # for sentence in words:
        indices = [word2idx[word] for word in words]
        
        for center_word_pos in range(len(indices)):
            for w in range(-window_size, window_size + 1):
                context_word_pos = center_word_pos + w
                if context_word_pos < 0 or context_word_pos >= len(indices) or center_word_pos == context_word_pos:
                    continue
                context_word_idx = indices[context_word_pos]
                idx_pairs.append((indices[center_word_pos], context_word_idx))
        
        idx_pairs = np.array(idx_pairs)
        
        embedding_dims = 5
        W1 = Variable(torch.randn(embedding_dims, vocabulary_size).float(), requires_grad=True)
        W2 = Variable(torch.randn(vocabulary_size, embedding_dims).float(), requires_grad=True)
        num_epochs = 1
        learning_rate = 0.01
        
        
        for epo in range(num_epochs):
            loss_val = 0
            for data, target in idx_pairs:
                x = Variable(self.get_input_layer(data, vocabulary_size)).float()
                y_true = Variable(torch.from_numpy(np.array([target])).long())
        
                z1 = torch.matmul(W1, x)
                z2 = torch.matmul(W2, z1)
            
                log_softmax = F.log_softmax(z2, dim=0)
        
                loss = F.nll_loss(log_softmax.view(1,-1), y_true)
                loss_val += loss.item()
                loss.backward()
                W1.data -= learning_rate * W1.grad.data
                W2.data -= learning_rate * W2.grad.data
        
                W1.grad.data.zero_()
                W2.grad.data.zero_()
            if epo % 10 == 0:    
                print(f'Loss at epo {epo}: {loss_val/len(idx_pairs)}')
                
        tmp = []
        for data, target in idx_pairs:
             x = Variable(self.get_input_layer(data, vocabulary_size)).float()
             z1 = torch.matmul(W1, x)
             tmp.append(z1)
        return tmp
    
    def make_training_data(self):
        for label in self.LABELS:
            for f in tqdm(os.listdir(label)):
                if("_Ref" not in f):
                    # try:
                        path = os.path.join(label, f)
                        with open(path, "r", encoding = 'utf-8') as inpt:
                            words = inpt.read().split()
                            
                            
                            
                            tmp = self.word2vec(words)
                            # print(tmp)
                            self.training_data.append([np.array(tmp), np.eye(3)[self.LABELS[label]]])
                                
                    # except Exception as e:
                    #    pass
        np.random.shuffle(self.training_data)
        np.save("training_data.npy", self.training_data)
        
if REBUILD_DATA:
    t = tr()
    t.make_training_data()