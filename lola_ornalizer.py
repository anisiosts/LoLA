import json

def 

def main():
    lola = json.loads(open('lola-patch.json').read())
    for item in lola:
        frase = ''
        if item['Nome'] == 'Nidalee':
            if item['Patch'] !=  None:
                item['Patch'] = item['Patch'].strip()
                frase += item['Patch']
                """passar isso pra funcao tb"""
            if item['Sumario'] !=  None:
                item['Sumario'] = item['Sumario'].strip()
                frase += 'Summary: ' + item['Sumario']
            if item['Texto'] !=  None:
                item['Texto'] = item['Texto'].strip()
                frase += 'Text: ' + item['Texto']
            for skill in item['Skills']:
                if skill !=  None:
                    skill = skill.strip()
                    frase += skill
            if len(frase) > 280:
                frase1 = frase[:280]
                frase2 = frase[280:]
                """fazer funcao para ir diminuindo recursivamente"""
                print len(frase)

if __name__ == "__main__":
    main()