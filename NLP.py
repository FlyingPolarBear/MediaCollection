'''
Author: Derry
Date: 2022-12-06 09:19:54
LastEditors: Derry
Email: drlv@mail.ustc.edu.cn
LastEditTime: 2022-12-06 09:25:01
Description: None
'''

import torch
from sentence_transformers import SentenceTransformer, util


class NLPEmbedding:
    def __init__(self):
        self.model_name = "multi-qa-MiniLM-L6-cos-v1"
        self.model_path = "E:/Research/Causal/data/model/sentence-transformers/"+self.model_name
        self.model = SentenceTransformer(self.model_path)
        print(f"NLP pre-trained model [{self.model_name}] has loaded!")

    def sentense_similarity(self, query, passage):
        query_embedding = self.model.encode(query)
        passage_embedding = self.model.encode(passage)
        return util.dot_score(query_embedding, passage_embedding)

    def init_passage(self, passage):
        self.passage = passage
        self.passage_embedding = self.model.encode(passage)

    def find_similar(self, query, passage=None, topk=1, threshold=None):
        """
        Find the most similar sentence in passage, according to query.

        Parameters
        ----------
        query : str
            The query sentence.
        passage : list, optional
            The passage sentences. If None, use the passage in init_passage. The default is None.
        topk : int, optional
            The number of similar sentences. The default is 1. (able only when threshold is None)
        threshold : float, optional
            The threshold of similarity. The default is 0.75.

        Returns
        -------
        1. The most similar sentence.
        2. The similarity score of the most similar sentence.
        """
        if passage:
            self.init_passage(passage)
        elif not hasattr(self, "passage"):
            raise Exception("Passage is not initialized!")

        query_embedding = self.model.encode(query)
        score = util.dot_score(query_embedding, self.passage_embedding)[0]
        topk_value, topk_index = torch.topk(score, topk)
        topk_concept = [self.passage[i] for i in topk_index]
        if threshold:
            thres_index = torch.where(score > threshold)[0]
            # sort by score
            thres_index = thres_index[torch.argsort(score[thres_index], descending=True)]
            thres_concept = [self.passage[i] for i in thres_index]
            thres_value = score[thres_index]
            if len(topk_concept) < len(thres_concept):
                topk_concept = thres_concept
                topk_value = thres_value
        return topk_concept, topk_value


if __name__ == "__main__":
    query = 'How big is London'
    passage = ['London has 9,787,426 inhabitants at the 2011 census',
               'London is known for its finacial district']
    nlp = NLPEmbedding()
    nlp.init_passage(passage)
    print(nlp.find_similar(query))
