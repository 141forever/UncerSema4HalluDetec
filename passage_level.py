def read_co():
    with open('co.json', 'r', encoding='utf-8') as file:
        co_dict = json.load(file)
    with open('co.json', 'r', encoding='utf-8') as file:
        co_dict2 = json.load(file)

    for key in co_dict.keys():
        key_list = key.split("+")
        co_dict2[key_list[0]+"+"+key_list[2]+"+"+key_list[1]]= 1

    return co_dict2
    
def calculate_NLI_score(loss_data):
    co_dict = read_co()

    score_dict = {}
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    selfcheck_nli = SelfCheckNLI(device=device,nli_model="pretrained_models/deberta-v3-large/")
    #,nli_model = "/home/ubuntu/CKD/pretrained_models/deberta-v3-large/"
    # set device to 'cuda' if GPU is available
    # co_result = {}
    for i in range(len(loss_data[0])):
        print(i)
        score_dict[i] = []
        sentences = hallucination_data[i]["gpt3_sentences"]
        for s_idx, s in enumerate(sentences):
            cans = []
            refs = []
            cans.append(sentences[s_idx])
            f = 1
            for j in range(len(sentences)):
                if j != s_idx:
                    # sentence1 = sentences[s_idx]
                    # sentence2 = sentences[j]
                    # ff = coreference_resolution(sentence1, sentence2)
                    # if ff == 0:
                    #     continue
                    # co_result[str(i)+"+"+str(s_idx)+"+"+str(j)]=ff

                    key_now = str(i)+"+"+str(s_idx)+"+"+str(j)
                    if key_now in co_dict.keys():
                        refs.append(sentences[j])
                        f = 0
                    # if s_idx - 1 > -1:
                    #     refs.append(sentences[s_idx-1])
                    # if s_idx+1 < len(sentences):
                    #     refs.append(sentences[s_idx+1])

            # if f == 1:
            #     # print(i,s_idx)
            #     for j in range(len(sentences)):
            #         if j != s_idx:
            #             refs.append(sentences[j])
            # if len(refs) == 0 :
            #     score_dict[i].append(0)
            #     continue
            sent_scores_nli = selfcheck_nli.predict(
                sentences=cans,  # list of sentences
                sampled_passages=refs,  # list of sampled passages
            )
            # pdb.set_trace()
            if f == 1:
                score_dict[i].append(1)
            else:
                score_dict[i].append(sent_scores_nli[0])

def sentnece_quantile(socre_list):
    sorted_score = sorted(socre_list)
    # pdb.set_trace()
    alpha = #######
    qua_posi = math.floor(len(sorted_score) * alpha)
    qua_v = sorted_score[qua_posi]
    return qua_v

    # with open('co.json', 'w') as json_file:
    #     json.dump(co_result, json_file, indent=4)
    return score_dict
