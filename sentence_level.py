def read_path(path):
    f = open(path,'r',encoding='utf-8')
    line = f.readline()
    d = {}
    while line:
        if '+' not in line:
            line = f.readline()
            continue
        split_list = line.split("+")
        id1 = split_list[0]
        id2 = split_list[1]
        idx1 = -1
        idx2 = -1
        for i in range(len(split_list[2])):
            if split_list[2][i] == '(':
                idx1 = i
            if split_list[2][i] == ')':
                idx2 = i
                break
        try:
            assert idx1 != -1
            assert idx2 != -1
        except:
            line = f.readline()
            continue
        strr_now = split_list[2][idx1+1:idx2]
        head_now_list = strr_now.split(",")[0].split(" ")
        for item in head_now_list:
            if item!="":
                head_now = item
                break
        try:
            predict_now_list = strr_now.split(",")[1].split(" ")
        except:
            pdb.set_trace()
        for item in predict_now_list:
            if item!="":
                predict_now = item
                break
        try:
            tail_now_list = strr_now.split(",")[2].split(" ")
        except:
            pdb.set_trace()
        for item in tail_now_list:
            if item!="":
                tail_now = item
                break
        if ('<'not in head_now and '>' not in head_now) and ('<' not in predict_now and '>' not in predict_now) and ('<' not in tail_now and '>' not in tail_now):
            d[id1+"-"+id2] = [head_now,predict_now,tail_now]
        line =f.readline()
    return d


# caculation
def calculate_verb_score(last_noun,hallu_score,span,use_threshold,encodings,attention):
    # pdb.set_trace()
    start, end = span.idx, span.idx + len(span)

    score_list = []
    posi_list = []
    vis = {}
    for i in range(start, end):
        final_score = 0
        loss_index = encodings.char_to_token(i) - 1
        if loss_index not in vis.keys():
            vis[loss_index] = 1
        else:
            continue
        noun_mask_verb = torch.ones_like(hallu_score)
        for idx in last_noun:
            noun_mask_verb[idx] = 0
        noun_mask_verb[loss_index] = 0
        try:
            attention[loss_index][noun_mask_verb.bool()] = 0
        except:
            pdb.set_trace()

        weight = attention[loss_index] / (torch.sum(attention[loss_index]) + 1e-6)
        if use_threshold:
            weight = weight.view(-1, 1)
            penalty = torch.sum(weight * hallu_score,dim=0).tolist()[0] # 在这里不用担心阈值的问题
            final_score += penalty
        else:
            pdb.set_trace()
            # penalty = torch.sum(weight * hallu_score).item()
            # hallu_score[loss_index] += discount * penalty

        score_list.append(final_score)
        posi_list.append(loss_index)
    return score_list,posi_list

def calculate_verb_score2(last_verb,hallu_score,span,use_threshold,encodings,attention):
    start, end = span.idx, span.idx + len(span)

    score_list = []
    posi_list = []
    vis = {}
    for i in range(start, end):
        final_score = 0
        loss_index = encodings.char_to_token(i) - 1
        if loss_index not in vis.keys():
            vis[loss_index] = 1
        else:
            continue
        noun_mask_verb = torch.ones_like(hallu_score)
        for idx in last_verb:
            noun_mask_verb[idx] = 0
        noun_mask_verb[loss_index] = 0
        attention[loss_index][noun_mask_verb.bool()] = 0

        weight = attention[loss_index] / (torch.sum(attention[loss_index]) + 1e-6)
        if use_threshold:
            weight = weight.view(-1, 1)
            penalty = torch.sum(weight * hallu_score,dim=0).tolist()[0] # 在这里不用担心阈值的问题
            final_score += penalty
        else:
            pdb.set_trace()
            # penalty = torch.sum(weight * hallu_score).item()
            # hallu_score[loss_index] += discount * penalty

        score_list.append(final_score)
        posi_list.append(loss_index)
    return score_list,posi_list
  
def write_result(list):
    f = open("result_sentence.txt","w",encoding="utf-8")
    for item in list:
        f.write(str(item[0])+"  "+str(item[1])+"\n")

# code slot1
path_dic = read_path("./amr_path_spacy1.txt")

# code slot2
if f == 1 and ff == 1:
    if span.pos_ == "VERB":
        if len(noun_now) != 0:
            score_verb_now,posi_verb_now = calculate_verb_score(noun_now,hallu_score1,span,use_threshold,encodings,attention)
            for idx in score_verb_now:
                verb_score_tmp.append(idx)
            for idx in posi_verb_now:
                verb_posi_tmp.append(idx)

            if span.text == pr and ff == 1 and f == 1:
                ff = 2
        assert len(verb_score_tmp) == len(verb_posi_tmp)

# code slot3
if span.text not in NER_type and (span.ent_type_ in NER_type or span.pos_ in pos_tag):
  last_noun = noun_now
  noun_now = []
  if span.text == h_e and f == 1 and ff == 0:
      ff = 1
  if ff == 2 and f == 1 and span.text == t_e:
      ff = 3
      f = open("right_tuple.txt","a",encoding='utf-8')
      f.write(str(passage_id)+"-"+str(sent_id)+"\n")
      f.close()

# code slot4
noun_now.append(loss_index)
if len(verb_score_tmp)!=0 and len(verb_posi_tmp)!=0 and ff == 3 and f == 1:
    verb_score_list2,_ = calculate_verb_score2(verb_posi_tmp,hallu_score1, span, use_threshold, encodings, attention)
    ave1 = sum(verb_score_tmp)/len(verb_score_tmp)
    ave2 = sum(verb_score_list2)/len(verb_score_list2)
    ave = (ave1 + ave2)/2
    print(ave)
else:
    ave = 1
  
# code slot5
if len(last_noun) == 0:
    ont_score = ontolog_hallu_list[loss_index]
else:
    onto_sum = 0
    for ss in last_noun:
        onto_sum += ontolog_hallu_list[ss]
    ont_score = onto_sum/len(last_noun)

# code slot6
verb_score_tmp = []
verb_posi_tmp = []
last_noun = []
f = 1
ff = 0

