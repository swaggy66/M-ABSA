# This file contains the evaluation functions

import re
import editdistance

sentiment_word_list = ['positive', 'negative', 'neutral']

## res
aspect_cate_list = ['location general',
 'food prices',
 'food quality',
 'ambience general',
 'service general',
 'restaurant prices',
 'drinks prices',
 'restaurant miscellaneous',
 'drinks quality',
 'drinks style_options',
 'restaurant general',
 'food style_options']


## laptop 
# aspect_cate_list =  ['BATTERY#DESIGN_FEATURES', 'BATTERY#GENERAL', 'BATTERY#OPERATION_PERFORMANCE', 'BATTERY#QUALITY', 'COMPANY#DESIGN_FEATURES', 'COMPANY#GENERAL', 'COMPANY#OPERATION_PERFORMANCE', 'COMPANY#PRICE', 'COMPANY#QUALITY', 'CPU#DESIGN_FEATURES', 'CPU#GENERAL', 'CPU#OPERATION_PERFORMANCE', 'CPU#PRICE', 'CPU#QUALITY', 'DISPLAY#DESIGN_FEATURES', 'DISPLAY#GENERAL', 'DISPLAY#OPERATION_PERFORMANCE', 'DISPLAY#PRICE', 'DISPLAY#QUALITY', 'DISPLAY#USABILITY', 'FANS&COOLING#DESIGN_FEATURES', 'FANS&COOLING#GENERAL', 'FANS&COOLING#OPERATION_PERFORMANCE', 'FANS&COOLING#QUALITY', 'GRAPHICS#DESIGN_FEATURES', 'GRAPHICS#GENERAL', 'GRAPHICS#OPERATION_PERFORMANCE', 'GRAPHICS#USABILITY', 'HARDWARE#DESIGN_FEATURES', 'HARDWARE#GENERAL', 'HARDWARE#OPERATION_PERFORMANCE', 'HARDWARE#PRICE', 'HARDWARE#QUALITY', 'HARDWARE#USABILITY', 'HARD_DISC#DESIGN_FEATURES', 'HARD_DISC#GENERAL', 'HARD_DISC#OPERATION_PERFORMANCE', 'HARD_DISC#PRICE', 'HARD_DISC#QUALITY', 'HARD_DISC#USABILITY', 'KEYBOARD#DESIGN_FEATURES', 'KEYBOARD#GENERAL', 'KEYBOARD#OPERATION_PERFORMANCE', 'KEYBOARD#PORTABILITY', 'KEYBOARD#PRICE', 'KEYBOARD#QUALITY', 'KEYBOARD#USABILITY', 'LAPTOP#CONNECTIVITY', 'LAPTOP#DESIGN_FEATURES', 'LAPTOP#GENERAL', 'LAPTOP#MISCELLANEOUS', 'LAPTOP#OPERATION_PERFORMANCE', 'LAPTOP#PORTABILITY', 'LAPTOP#PRICE', 'LAPTOP#QUALITY', 'LAPTOP#USABILITY', 'MEMORY#DESIGN_FEATURES', 'MEMORY#GENERAL', 'MEMORY#OPERATION_PERFORMANCE', 'MEMORY#QUALITY', 'MEMORY#USABILITY', 'MOTHERBOARD#OPERATION_PERFORMANCE', 'MOTHERBOARD#QUALITY', 'MOUSE#GENERAL', 'MULTIMEDIA_DEVICES#CONNECTIVITY', 'MULTIMEDIA_DEVICES#DESIGN_FEATURES', 'MULTIMEDIA_DEVICES#GENERAL', 'MULTIMEDIA_DEVICES#OPERATION_PERFORMANCE', 'MULTIMEDIA_DEVICES#PRICE', 'MULTIMEDIA_DEVICES#QUALITY', 'MULTIMEDIA_DEVICES#USABILITY', 'OPTICAL_DRIVES#DESIGN_FEATURES', 'OPTICAL_DRIVES#GENERAL', 'OPTICAL_DRIVES#OPERATION_PERFORMANCE', 'OPTICAL_DRIVES#USABILITY', 'OS#DESIGN_FEATURES', 'OS#GENERAL', 'OS#MISCELLANEOUS', 'OS#OPERATION_PERFORMANCE', 'OS#QUALITY', 'OS#USABILITY', 'Out_Of_Scope#GENERAL', 'Out_Of_Scope#OPERATION_PERFORMANCE', 'Out_Of_Scope#USABILITY', 'PORTS#CONNECTIVITY', 'PORTS#DESIGN_FEATURES', 'PORTS#GENERAL', 'PORTS#OPERATION_PERFORMANCE', 'PORTS#PORTABILITY', 'PORTS#QUALITY', 'PORTS#USABILITY', 'POWER_SUPPLY#CONNECTIVITY', 'POWER_SUPPLY#DESIGN_FEATURES', 'POWER_SUPPLY#GENERAL', 'POWER_SUPPLY#OPERATION_PERFORMANCE', 'POWER_SUPPLY#QUALITY', 'SHIPPING#GENERAL', 'SHIPPING#OPERATION_PERFORMANCE', 'SHIPPING#PRICE', 'SHIPPING#QUALITY', 'SOFTWARE#DESIGN_FEATURES', 'SOFTWARE#GENERAL', 'SOFTWARE#OPERATION_PERFORMANCE', 'SOFTWARE#PORTABILITY', 'SOFTWARE#PRICE', 'SOFTWARE#QUALITY', 'SOFTWARE#USABILITY', 'SUPPORT#DESIGN_FEATURES', 'SUPPORT#GENERAL', 'SUPPORT#OPERATION_PERFORMANCE', 'SUPPORT#PRICE', 'SUPPORT#QUALITY', 'WARRANTY#GENERAL', 'WARRANTY#QUALITY']
## phone
# aspect_cate_list =  ['After-sales Service#Exchange/Warranty/Return', 'Appearance Design#Aesthetics General', 'Appearance Design#Color', 'Appearance Design#Exterior Design Material', 'Appearance Design#Fuselage Size', 'Appearance Design#Grip Feeling', 'Appearance Design#Thickness', 'Appearance Design#Weight', 'Appearance Design#Workmanship and Texture', 'Audio/Sound#Tone quality', 'Audio/Sound#Volume and Speaker', 'Battery/Longevity#Battery Capacity', 'Battery/Longevity#Battery Life', 'Battery/Longevity#Charging Method', 'Battery/Longevity#Charging Speed', 'Battery/Longevity#General', 'Battery/Longevity#Power Consumption Speed', 'Battery/Longevity#Standby Time', 'Branding/Marketing#Promotional Giveaways', 'Buyer Attitude#Loyalty', 'Buyer Attitude#Recommendable', 'Buyer Attitude#Repurchase and Churn Tendency', 'Buyer Attitude#Shopping Experiences', 'Buyer Attitude#Shopping Willingness', 'Camera#Fill light', 'Camera#Front Camera', 'Camera#General', 'Camera#Rear Camera', 'Ease of Use#Audience Groups', 'Ease of Use#Easy to Use', 'Intelligent Assistant#Intelligent Assistant General', 'Intelligent Assistant#Wake-up Function', 'Key Design#General', 'Logistics#Lost and Damaged', 'Logistics#Shipping Fee', 'Logistics#Speed', 'Logistics#general', 'Overall#Overall', 'Performance#General', 'Performance#Heat Generation', 'Performance#Running Speed', 'Price#Price', 'Price#Value for Money', 'Product Accessories#Cell Phone Film', 'Product Accessories#Charger', 'Product Accessories#Charging Cable', 'Product Accessories#Headphones', 'Product Accessories#Phone Cases', 'Product Configuration#CPU', 'Product Configuration#Memory', 'Product Configuration#Operating Memory', 'Product Packaging#Completeness of Accessories', 'Product Packaging#General', 'Product Packaging#Instruction Manual', 'Product Packaging#Packaging Grade', 'Product Packaging#Packaging Materials', 'Product Quality#Cleanliness', 'Product Quality#Dustproof', 'Product Quality#Fall Protection', 'Product Quality#General', 'Product Quality#Genuine Product', 'Product Quality#Water Resistant', 'Screen#Clarity', 'Screen#General', 'Screen#Screen-to-Body Ratio', 'Screen#Size', 'Security#Screen Unlock', 'Seller Service#Attitude', 'Seller Service#Inventory', 'Seller Service#Seller Expertise', 'Seller Service#Shipping', 'Seller Service#Timeliness of Seller Service', 'Shooting Functions#General', 'Shooting Functions#Pixel', 'Signal#Call Quality', 'Signal#Signal General', 'Signal#Signal of Mobile Network', 'Signal#Wifi Signal', 'Smart Connect#Bluetooth Connection', 'Smart Connect#Positioning and GPS', 'System#Application', 'System#Lock Screen Design', 'System#NFC', 'System#Operation Smoothness', 'System#Software Compatibility', 'System#System General', 'System#System Upgrade', 'System#UI Interface Aesthetics']

## hotel
# aspect_cate_list =  ['facilities cleanliness', 'facilities comfort', 'facilities design_features', 'facilities general', 'facilities miscellaneous', 
#                      'facilities prices', 'facilities quality', 'food_drinks miscellaneous', 'food_drinks prices', 'food_drinks quality', 'food_drinks style_options', 
#                      'hotel cleanliness', 'hotel comfort', 'hotel design_features', 'hotel general', 'hotel miscellaneous', 'hotel prices', 'hotel quality', 'location general', 
#                      'polarity negative', 'polarity neutral', 'polarity positive', 'room_amenities cleanliness', 'room_amenities comfort', 'room_amenities design_features', 
#                      'room_amenities general', 'room_amenities miscellaneous', 'room_amenities prices', 'room_amenities quality', 'rooms cleanliness', 'rooms comfort', 
#                      'rooms design_features', 'rooms general', 'rooms miscellaneous', 'rooms prices', 'rooms quality', 'service general']

## cousera
# aspect_cate_list =  ['assignments comprehensiveness', 'assignments quality', 'assignments quantity', 'assignments relatability', 'assignments workload', 'course comprehensiveness', 'course general', 'course quality', 'course relatability', 'course value', 'course workload', 'faculty comprehensiveness', 'faculty general', 'faculty relatability', 'faculty response', 'faculty value', 'grades general', 'material comprehensiveness', 'material quality', 'material quantity', 'material relatability', 'material workload', 'polarity negative', 'polarity neutral', 'polarity positive', 'presentation comprehensiveness', 'presentation quality', 'presentation quantity', 'presentation relatability', 'presentation workload']

## amazon food
# aspect_cate_list =  ['amazon availability', 'amazon prices', 'food general', 'food misc', 'food prices', 'food quality', 'food recommendation', 'food style_options', 'polarity negative', 'polarity positive', 'shipment delivery', 'shipment prices', 'shipment quality']

## uabsa
# aspect_cate_list =  ['-1', '0', '1']

# education
# aspect_cate_list =  ['Course_General_Feedback', 'Instructor', 'Mathematical_Related_Concept', 'Other', 'Teaching_Setup']


def extract_spans_extraction(task, seq):
    extractions = []
    if task == 'uabsa' and seq.lower() == 'none':
        return []
    else:
        if task in ['uabsa', 'aope']:
            all_pt = seq.split('; ')
            for pt in all_pt:
                pt = pt[1:-1]
                try:
                    a, b = pt.split(', ')
                except ValueError:
                    a, b = '', ''
                extractions.append((a, b))
        elif task in ['tasd', 'aste']:
            all_pt = seq.split('; ')
            for pt in all_pt:
                pt = pt[1:-1]
                try:
                    a, b, c = pt.split(', ')
                except ValueError:
                    a, b, c = '', '', ''
                extractions.append((a, b, c))            
        return extractions


def extract_spans_annotation(task, seq):
    if task in ['aste', 'tasd']:
        extracted_spans = extract_triplets(seq)
    elif task in ['aope', 'uabsa']:
        extracted_spans = extract_pairs(seq)

    return extracted_spans


def extract_pairs(seq):
    aps = re.findall('\[.*?\]', seq)
    aps = [ap[1:-1] for ap in aps]
    pairs = []
    for ap in aps:
        # the original sentence might have 
        try:
            at, ots = ap.split('|')
        except ValueError:
            at, ots  = '', ''
        
        if ',' in ots:     # multiple ots 
            for ot in ots.split(', '):
                pairs.append((at, ot))
        else:
            pairs.append((at, ots))    
    return pairs        


def extract_triplets(seq):
    aps = re.findall('\[.*?\]', seq)
    aps = [ap[1:-1] for ap in aps]
    triplets = []
    for ap in aps:
        try:
            a, b, c = ap.split('|')
        except ValueError:
            a, b, c = '', '', ''
        
        # for ASTE
        if b in sentiment_word_list:
            if ',' in c:
                for op in c.split(', '):
                    triplets.append((a, b, op))
            else:
                triplets.append((a, b, c))
        # for TASD
        else:
            if ',' in b:
                for ac in b.split(', '):
                    triplets.append((a, ac, c))
            else:
                triplets.append((a, b, c))
    # print('tri',triplets)
    return triplets


def recover_terms_with_editdistance(original_term, sent):
    words = original_term.split(' ')
    new_words = []
    for word in words:
        edit_dis = []
        for token in sent:
            edit_dis.append(editdistance.eval(word, token))
        smallest_idx = edit_dis.index(min(edit_dis))
        new_words.append(sent[smallest_idx])
    new_term = ' '.join(new_words)
    return new_term


def fix_preds_uabsa(all_pairs, sents):

    all_new_pairs = []
    for i, pairs in enumerate(all_pairs):
        new_pairs = []
        if pairs == []:
            all_new_pairs.append(pairs)
        else:
            for pair in pairs:
                # AT not in the original sentence
                if pair[0] not in  ' '.join(sents[i]):
                    # print('Issue')
                    new_at = recover_terms_with_editdistance(pair[0], sents[i])
                else:
                    new_at = pair[0]

                if pair[1] not in sentiment_word_list:
                    new_sentiment = recover_terms_with_editdistance(pair[1], sentiment_word_list)
                else:
                    new_sentiment = pair[1]

                new_pairs.append((new_at, new_sentiment))
                # print(pair, '>>>>>', word_and_sentiment)
                # print(all_target_pairs[i])
            all_new_pairs.append(new_pairs)

    return all_new_pairs


def fix_preds_aope(all_pairs, sents):

    all_new_pairs = []

    for i, pairs in enumerate(all_pairs):
        new_pairs = []
        if pairs == []:
            all_new_pairs.append(pairs)
        else:
            for pair in pairs:
                #print(pair)
                # AT not in the original sentence
                if pair[0] not in  ' '.join(sents[i]):
                    # print('Issue')
                    new_at = recover_terms_with_editdistance(pair[0], sents[i])
                else:
                    new_at = pair[0]

                # OT not in the original sentence
                ots = pair[1].split(', ')
                new_ot_list = []
                for ot in ots:
                    if ot not in ' '.join(sents[i]):
                        # print('Issue')
                        new_ot_list.append(recover_terms_with_editdistance(ot, sents[i]))
                    else:
                        new_ot_list.append(ot)
                new_ot = ', '.join(new_ot_list)

                new_pairs.append((new_at, new_ot))
                # print(pair, '>>>>>', word_and_sentiment)
                # print(all_target_pairs[i])
            all_new_pairs.append(new_pairs)

    return all_new_pairs


# for ASTE
def fix_preds_aste(all_pairs, sents):

    all_new_pairs = []

    for i, pairs in enumerate(all_pairs):
        new_pairs = []
        if pairs == []:
            all_new_pairs.append(pairs)
        else:
            for pair in pairs:
                #two formats have different orders
                p0, p1, p2 = pair
                # for annotation-type
                if p1 in sentiment_word_list:
                    at, ott, ac = p0, p2, p1
                    io_format = 'annotation'
                # for extraction type
                elif p2 in sentiment_word_list:
                    at, ott, ac = p0, p1, p2
                    io_format = 'extraction'

                #print(pair)
                # AT not in the original sentence
                if at not in  ' '.join(sents[i]):
                    # print('Issue')
                    new_at = recover_terms_with_editdistance(at, sents[i])
                else:
                    new_at = at
                
                if ac not in sentiment_word_list:
                    new_sentiment = recover_terms_with_editdistance(ac, sentiment_word_list)
                else:
                    new_sentiment = ac
                
                # OT not in the original sentence
                ots = ott.split(', ')
                new_ot_list = []
                for ot in ots:
                    if ot not in ' '.join(sents[i]):
                        # print('Issue')
                        new_ot_list.append(recover_terms_with_editdistance(ot, sents[i]))
                    else:
                        new_ot_list.append(ot)
                new_ot = ', '.join(new_ot_list)
                if io_format == 'extraction':
                    new_pairs.append((new_at, new_ot, new_sentiment))
                else:
                    new_pairs.append((new_at, new_sentiment, new_ot))
                # print(pair, '>>>>>', word_and_sentiment)
                # print(all_target_pairs[i])
            all_new_pairs.append(new_pairs)
    
    return all_new_pairs


def fix_preds_tasd(all_pairs, sents):

    all_new_pairs = []

    for i, pairs in enumerate(all_pairs):
        # print(i,pairs)
        new_pairs = []
        if pairs == []:
            all_new_pairs.append(pairs)
        else:
            for pair in pairs:
                #print(pair)
                # AT not in the original sentence
                sents_and_null = ' '.join(sents[i]) + 'NULL'
                if pair[0] not in  sents_and_null:
                    # print('Issue')
                    new_at = recover_terms_with_editdistance(pair[0], sents[i])
                else:
                    new_at = pair[0]
                
                # AC not in the list
                acs = pair[1].split(', ')
                new_ac_list = []
                for ac in acs:
                    if ac not in aspect_cate_list:
                        new_ac_list.append(recover_terms_with_editdistance(ac, aspect_cate_list))
                    else:
                        new_ac_list.append(ac)
                new_ac = ', '.join(new_ac_list)
                
                if pair[2] not in sentiment_word_list:
                    new_sentiment = recover_terms_with_editdistance(pair[2], sentiment_word_list)
                else:
                    new_sentiment = pair[2]
            
                new_pairs.append((new_at, new_ac, new_sentiment))
                # print(pair, '>>>>>', word_and_sentiment)
                # print(all_target_pairs[i])
            all_new_pairs.append(new_pairs)
    
    return all_new_pairs


def fix_pred_with_editdistance(all_predictions, sents, task):
    if task == 'uabsa':
        fixed_preds = fix_preds_uabsa(all_predictions, sents)
    elif task == 'aope':
        fixed_preds = fix_preds_aope(all_predictions, sents) 
    elif task == 'aste': 
        fixed_preds = fix_preds_aste(all_predictions, sents) 
    elif task == 'tasd':
        fixed_preds = fix_preds_tasd(all_predictions, sents) 
    else:
        print("*** Unimplemented Error ***")
        fixed_preds = all_predictions

    return fixed_preds


def compute_f1_scores(pred_pt, gold_pt):
    """
    Function to compute F1 scores with pred and gold pairs/triplets
    The input needs to be already processed
    """
    # number of true postive, gold standard, predicted aspect terms
    n_tp, n_gold, n_pred = 0, 0, 0

    for i in range(len(pred_pt)):
        n_gold += len(gold_pt[i])
        n_pred += len(pred_pt[i])

        for t in pred_pt[i]:
            if t in gold_pt[i]:
                n_tp += 1

    precision = float(n_tp) / float(n_pred) if n_pred != 0 else 0
    recall = float(n_tp) / float(n_gold) if n_gold != 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if precision != 0 or recall != 0 else 0
    scores = {'precision': precision, 'recall': recall, 'f1': f1}

    return scores


def compute_scores(pred_seqs, gold_seqs, sents, io_format, task):
    """
    compute metrics for multiple tasks
    """
    assert len(pred_seqs) == len(gold_seqs) 
    num_samples = len(gold_seqs)

    all_labels, all_predictions = [], []

    for i in range(num_samples):
        if io_format == 'annotation':
            gold_list = extract_spans_annotation(task, gold_seqs[i])
            pred_list = extract_spans_annotation(task, pred_seqs[i])
        elif io_format == 'extraction':
            gold_list = extract_spans_extraction(task, gold_seqs[i])
            pred_list = extract_spans_extraction(task, pred_seqs[i])

        all_labels.append(gold_list)
        all_predictions.append(pred_list)
    
    print("\nResults of raw output")
    raw_scores = compute_f1_scores(all_predictions, all_labels)
    print(raw_scores)

    # fix the issues due to generation
    all_predictions_fixed = fix_pred_with_editdistance(all_predictions, sents, task)
    print("\nResults of fixed output")
    fixed_scores = compute_f1_scores(all_predictions_fixed, all_labels)
    print(fixed_scores)
    
    return raw_scores, fixed_scores, all_labels, all_predictions, all_predictions_fixed