from typing import List
from jpype import JClass, JString, getDefaultJVMPath, shutdownJVM, startJVM, java
import pandas as pd
from os.path import join
from sklearn.utils import shuffle
from pandas import ExcelWriter
import re
from nltk.corpus import stopwords


ZEMBEREK_PATH = "./bin/zemberek-full.jar"

startJVM(getDefaultJVMPath(), '-ea', '-Djava.class.path=%s' % (ZEMBEREK_PATH))

dosya = ['vodafone.xlsx','türkcell.xlsx','türktelekom.xlsx']

for item in dosya:
    data = pd.read_excel(item)

    # tüm harfler küçüğe dönüştülür
    data = data.apply(lambda x: x.astype(str).str.lower())

    # Regex işlemleri
    for i in range(len(data)):

        # https://t.co/osUgGrOJSz kelimeleri silme
        output = re.sub(r"http[s]?:(?:[a-zA-Z]|[0-9]|[$-_@.& +]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", "",
                        data['tweet'][i])

        # @kullanıcı adlarını ve etiketleri silme
        output = re.sub(r"\@\w*\b", "", output)
        output = re.sub(r"\#\w*\b", "", output)
        # Rakamları temizleme
        output = re.sub(r"\b\d+", "", output)

        # 3 karakterden az olanları silme
        output = re.sub(r"\W*\b\w{1,2}\b", "", output)

        data['tweet'][i] = output

    ## Karakterleri temizleme
    data['tweet'] = data['tweet'].str.findall('\w{2,}').str.join(' ')

    ## Kelime düzeltme işlemi
    TurkishMorphology: JClass = JClass('zemberek.morphology.TurkishMorphology')
    TurkishSentenceNormalizer: JClass = JClass(
        'zemberek.normalization.TurkishSentenceNormalizer'
    )
    Paths: JClass = JClass('java.nio.file.Paths')

    normalizer = TurkishSentenceNormalizer(
        TurkishMorphology.createWithDefaults(),
        Paths.get(join('data', 'normalization')),
        Paths.get(join('data', 'lm', 'lm.2gram.slm'))
    )

    for num in range(len(data.tweet)):
        # print((
        #    f'\nNormal      : {data.tweet[num]}'
        #    f'\nDuzenlenmiş : {normalizer.normalize(JString(data.tweet[num]))}'
        #
        #        ))
        data.xs(num)['tweet'] = normalizer.normalize(JString(data.tweet[num]))

    ## Kelime köklerini bulma ve anlamsızlar UNK yazar
    '''
    TurkishMorphology = JClass('zemberek.morphology.TurkishMorphology')
    morphology = TurkishMorphology.createWithDefaults()
    
    for num in range(len(data.tweet)):
       # print("Orjinal tweet --->", data.tweet[num])
        analysis: java.util.ArrayList = (morphology.analyzeAndDisambiguate(data.tweet[num]).bestAnalysis())
        pos: List[str] = []
        for i, analysis in enumerate(analysis, start=1):
            f'\nAnalysis {i}: {analysis}', f'\nPrimary POS {i}: {analysis.getPos()}' f'\nPrimary POS (Short Form) {i}: {analysis.getPos().shortForm}'
            pos.append(
                f'{str(analysis.getLemmas()[0])}'
            )
        data.xs(num)['tweet'] = " ".join(pos)
       # print(f'Islem Gormus  ---> {" ".join(pos)}',"\n")
    
    data['tweet']=data['tweet'].str.replace("UNK"," ")
    #data['tweet']=data['tweet'].str.findall('\w{UNK}').str.join(' ')
    '''

    stop_words = stopwords.words('turkish')
    with open('turkce-stop-words.txt', encoding='utf-8') as file:
        stw = file.read()
    stw = stw.split()
    stw = [s.lower() for s in stw]
    stop_words += stw

    data['tweet'] = data['tweet'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop_words)]))

    data = shuffle(data)

    ad = 'temizlendi' + item
    writer = ExcelWriter(ad)
    data.to_excel(writer, item)
    writer.save()

shutdownJVM()
