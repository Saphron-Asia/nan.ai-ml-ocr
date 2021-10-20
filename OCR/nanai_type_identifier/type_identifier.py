import re
import difflib

import cv2
import pytesseract

form_patterns = ['CARD CARE RETURN STUB #1', 'CARD CARE RETURN STUB #2',
                 'KABUKLOD RETURN STUB #1', 'KABUKLOD RETURN STUB #2',
                 'SAGIP RETURN STUB #1', 'SAGIP RETURN STUB #2']

keywords = ['CARD CARE', 'KABUKLOD', 'SAGIP']


def aabb(img, data, regex, i):
    if re.match(regex, data['text'][i]):
        (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return img, True
    else:
        return img, False


def get_similarity(top_str, patterns):
    splice = top_str.split(' ')
    scores = {}
    occurrences = {}

    for pattern in patterns:
        pattern_len = len(pattern.split(' '))
        # print(f'Matching pattern: {pattern}')
        for i in range(len(splice)):
            splice_list = splice[i: i + pattern_len]
            curr_splice = ' '.join(str(e) for e in splice[i: i + pattern_len])

            if len(splice_list) < pattern_len:
                break

            similarity = difflib.SequenceMatcher(None, pattern, curr_splice).ratio()
            if similarity > 0.7:
                # print(f'curr_splice: {curr_splice} len: {len(splice_list)} \t || sim_score: {similarity}')
                scores[pattern] = similarity
                occurrences[pattern] = occurrences.get(pattern, 0) + 1

    return occurrences, scores


def get_type(imgPath):
    img = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
    
    # img = cv2.imread(imgPath)
    custom_config = r'--oem 3 --psm 6'
    infer = pytesseract.image_to_string(img, config=custom_config)
    top_string = infer.split('\n')[0]

    print(f'First line read: {top_string}')
    # print('Getting form matches')
    _, form_matches = get_similarity(top_string, form_patterns)
    # print(form_matches)

    # print('Getting keyword matches')
    keyword_matches, _ = get_similarity(top_string, keywords)
    # print(f'Keyword matches: {keyword_matches}')

    # Sort similarity scores
    # then get highest nth values
    sorted_scores = dict(sorted(form_matches.items(), key=lambda x: x[1], reverse=True)[:])
    print(f'Sorted scores: {sorted_scores}')

    final_form_type = []
    get_highest = 0

    for form, sim in sorted_scores.items():
        for keyword, occurrences in keyword_matches.items():
            # Got nth highest, exit loop
            if get_highest == occurrences:
                break
            elif keyword in form:
                final_form_type.append(form)
                get_highest += 1
            else:
                continue

    return final_form_type


if __name__ == '__main__':
    form_type = get_type('sagip1.jpg')
    print(form_type)
    print('-------------\n-------------')
    form_type = get_type('kbd20.jpg')
    print(form_type)
    print('-------------\n-------------')
    form_type = get_type('cc19.jpg')
    print(form_type)
    print('-------------\n-------------')
    form_type = get_type('02220103NANAISTAGGING - 2020062011285820200620112945.jpg')
    print(form_type)
    print('-------------\n-------------')
    form_type = get_type('cardcare.jpg')
    print(form_type)