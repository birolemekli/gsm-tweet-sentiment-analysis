# -*- coding: utf-8-*-
with open('../türkcell/2020-03-18-turkcell.txt','r') as f:
    lines=f.readlines()

vodafone=['^','Arena','ev','Ev','eba','Eba','seyircisiz','seyirci','Şampiyonluk','Uzman Desteği','nakil','mac','Mac','Maç',
    'Destek Al','park','Online','maç','Merhaba','Kampanya','Vodafone Cep','Vodafone Müşteri Hizmetleri',
    'Galatasaray','Beşiktaş' ,'beşiktaş','besiktas','galatasaray','ekran','Evde','evde','TV','ttnet','Vodafone Park',
    'derbi','corona','korona','#corona']

turkcell=['mevlutcavusoglu','3gb','eba','vodafone','telekom','tc_disisleri','maç','ev','eba','seyircisiz','seyirci',
          'nakil','mac','park','maç','besiktas','galatasaray','ekran','evde','TV','ttnet',
        'derbi','corona','korona','#corona','ücretsiz','eğitim','beşiktaş','araneda','arena','virüs','fener',
          'fenerbahçe','galatasaray','eba','eğitim','taahhut','taahhüt','maç','@anadoluefessk','sayı','basketbol',
          'film','maaş','milli','çanakkale','18mart','atatürk','mart','zafer','cennet','rahmet','minnetle🇹🇷','🇹🇷','asker',
          'şad','minnetle','vodafon','Çanakkale','Şehit','ensar','atatÜrk','mehmetçik','enver','saygıyla','canakkale','ordu',
          'hizmetleri','gb'
          ]

turktelekom=['beşiktaş','araneda','arena','virüs','fener','fenerbahçe','galatasaray','eba','eğitim','turkcell',
             'taahhut','taahhüt','maç','maçın','@anadoluefessk','sayı','basketbol','film','maaş','milli','vodafone',
             'fatura','3gb','eba','mevlutcavusoglu','3gb','eba','vodafone','tc_disisleri','maç','^','Arena','ev','Ev','eba','Eba',
             'seyircisiz','seyirci','Şampiyonluk','Uzman Desteği','nakil','mac','Mac','Maç',
            'Destek Al','park','Online','maç','Merhaba','Kampanya','Vodafone Cep','Vodafone Müşteri Hizmetleri',
            'Galatasaray','Beşiktaş' ,'beşiktaş','besiktas','galatasaray','ekran','Evde','evde','TV','ttnet','Vodafone Park',
            'derbi','corona','korona','#corona','ücretsiz','eğitim','gb','hizmetleri'
             ]

with open ('./türkcell/2020-03-18-turkcell-1.txt','w') as f:
    for line in lines:
        x=0
        y=0
        line=line.lower()
        if len(line.split())  > 3 and len(line.split())  < 40:
            for item in turkcell:
                if item in line:
                    x=x+1
            if x==0:
                if line != '	':
                    f.write(line.lstrip())
