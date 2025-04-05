def calculate_variance_max_score(outputs):
    logits = outputs.logits.squeeze(0)  # 去掉batch维度 (seq_length,32000)
    probabilities = torch.softmax(logits, dim=-1) # (seq_length,32000)

    top_k = 3
    onto_list = []
    i = 0
    for position_probs in probabilities:
        top_probs, top_indices = torch.topk(position_probs, top_k)
        maxx = torch.max(top_probs).item()
        varr = torch.var(top_probs, unbiased=False).item()
        onto_score = 1/(maxx+varr)
        decay_weight = math.exp(i/(probabilities.shape[0])-1)
        onto_list.append(onto_score*(1+decay_weight))
        # print(onto_score,decay_weight,onto_score*decay_weight)
        i += 1

    return onto_list
