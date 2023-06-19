import io
import requests
from PyPDF2 import PdfReader
import pandas as pd


url = 'https://hagstofan.s3.amazonaws.com/media/public/0acb20a5-fcc7-459b-8072-0fae7fb7af39/pub_doc_ediOqLC.pdf'
response = requests.get(url)
pdf_in_mem = io.BytesIO(response.content)
pdf = PdfReader(pdf_in_mem)

# Eða ef þú hefur þegar skjalið vistað:
# pdf = PdfReader('./pub_doc_ediOqLC.pdf')


def is_isat_digit(x):
    return all(i.isdigit() for i in x.split('.'))

isat08 = {}
for page in pdf.pages:
    lines = page.extract_text().replace('\t','').split('\n')
    # Finnum blaðsíðu sem er með isat08 yfirlitstöflu
    if 'yfirlitstöflur' in lines[0].lower():
        lines = [line.strip().split(' ') for line in lines]
        for line in lines:
            # Finnum línu sem inniheldur isat08 gildi og nafn
            if is_isat_digit(line[0]) and not is_isat_digit(line[-1]):
                isat_name = ' '.join([i for i in line if not is_isat_digit(i)]).strip().lower().capitalize()
                # Sumstaðar er fyrsti stafurinn hangandi?
                if isat_name[1] == ' ':
                    isat_name = isat_name[0] + isat_name[2:]
                the_isat_line = [i for i in line if is_isat_digit(i)]
                for i in the_isat_line:
                    isat08[i] = isat_name
            # Finnum bálkana
            elif line[0].isalpha() and len(line[0]) == 1 and line[-1].replace('–','').isdigit():
                isat08[line[0].upper()] = ' '.join(line[1:-1]).strip().lower().capitalize()

isat08_yfirlit = {
    'threp': [],
    'balk': [],
    'deild': [],
    'isat08': [],
    'isat08_nafn': []
}

for k, v in isat08.items():
    isat08_val = k.replace('.', '')
    threp = len(isat08_val)
    if k in ['A', *['0' + str(i) for i in range(1, 3 + 1)]]: balk = 'A'
    elif k in ['B', *['0' + str(i) for i in range(5, 9 + 1)]]: balk = 'B'
    elif k in ['C', *[str(i) for i in range(10, 33 + 1)]]: balk = 'C'
    elif k in ['D', '35']: balk = 'D'
    elif k in ['E', *[str(i) for i in range(36, 39 + 1)]]: balk = 'E'
    elif k in ['F', *[str(i) for i in range(41, 43 + 1)]]: balk = 'F'
    elif k in ['G', *[str(i) for i in range(45, 47 + 1)]]: balk = 'G'
    elif k in ['H', *[str(i) for i in range(49, 53 + 1)]]: balk = 'H'
    elif k in ['I', *[str(i) for i in range(55, 56 + 1)]]: balk = 'I'
    elif k in ['J', *[str(i) for i in range(58, 63 + 1)]]: balk = 'J'
    elif k in ['K', *[str(i) for i in range(64, 66 + 1)]]: balk = 'K'
    elif k in ['L', '68']: balk = 'L'
    elif k in ['M', *[str(i) for i in range(69, 75 + 1)]]: balk = 'M'
    elif k in ['N', *[str(i) for i in range(77, 82 + 1)]]: balk = 'N'
    elif k in ['O', '84']: balk = 'O'
    elif k in ['P', '85']: balk = 'P'
    elif k in ['Q', *[str(i) for i in range(86, 88 + 1)]]: balk = 'Q'
    elif k in ['R', *[str(i) for i in range(90, 93 + 1)]]: balk = 'R'
    elif k in ['S', *[str(i) for i in range(94, 96 + 1)]]: balk = 'S'
    elif k in ['T', *[str(i) for i in range(97, 98 + 1)]]: balk = 'T'
    elif k in ['U', '99']: balk = 'U'
    deild = k[:2] if len(k) > 1 else None
    isat08_yfirlit['threp'].append(threp)
    isat08_yfirlit['balk'].append(balk)
    isat08_yfirlit['deild'].append(deild)
    isat08_yfirlit['isat08'].append(isat08_val)
    isat08_yfirlit['isat08_nafn'].append(v)


isat08_yfirlit = pd.DataFrame(isat08_yfirlit)
