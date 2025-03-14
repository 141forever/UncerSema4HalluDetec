# UncerSema4HalluDetec
This is the repository for the paper **Enhancing Uncertainty Modeling with Semantic Graph for Hallucination Detection** (AAAI2025).

# Abstract
Large Language Models (LLMs) are prone to hallucination with non-factual or unfaithful statements, which undermines the applications in real-world scenarios. 
In this paper, we propose a method to enhance uncertainty modeling with semantic graph for hallucination detection. Specifically, we first construct a semantic graph that
well captures the relations among entity tokens and sentences. Then, we incorporate the relations between two entities for uncertainty propagation to enhance sentence-level hallucination detection. Given that hallucination occurs due to the conflict between sentences, we further present a graph-based uncertainty calibration method that integrates the contradiction probability of the sentence with its neighbors in the semantic graph for uncertainty calculation.

[[Paper Homepage]]() [[ARXIV]](https://arxiv.org/abs/2501.02020)

# Method
The overview of our approach for hallucination detection. For token-level uncertainty, we integrate the maximum and variance of the probabilities, along with a sequence decay term. Regarding to sentence-level uncertainty, we interpolate the sum of entity uncertainty through relation-based propagation and global uncertainty via quantile. Finally, we incorporate the relations of neighbor sentences in the semantic graph with graph-based uncertainty calibration for passage-level uncertainty.

![image](https://github.com/141forever/UncerSema4HalluDetec/blob/main/figures/method.jpg)

# Citation
If you think this method helps, welcome to cite our paper.
```
@article{DBLP:journals/corr/abs-2501-02020,
  author       = {Kedi Chen and
                  Qin Chen and
                  Jie Zhou and
                  Xinqi Tao and
                  Bowen Ding and
                  Jingwen Xie and
                  Mingchen Xie and
                  Peilong Li and
                  Feng Zheng and
                  Liang He},
  title        = {Enhancing Uncertainty Modeling with Semantic Graph for Hallucination
                  Detection},
  journal      = {CoRR},
  volume       = {abs/2501.02020},
  year         = {2025},
  url          = {https://doi.org/10.48550/arXiv.2501.02020},
  doi          = {10.48550/ARXIV.2501.02020},
  eprinttype    = {arXiv},
  eprint       = {2501.02020},
  timestamp    = {Mon, 17 Feb 2025 22:09:02 +0100},
  biburl       = {https://dblp.org/rec/journals/corr/abs-2501-02020.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}
```
