import json

# # # ORGANIZADOR DA LOLA # # #
class LolaOrganizer():
    # Classe responsavel por tratar os dados raspados pela LolaSpider.

    def __init__(self, patchs_file):
        self.patchs_file = patchs_file

    def champion_search(self, champion):
        # Procura por todas as ocorrencias de um dado campeão (atualmente esse metodo tambem gera a lista de tweets, passar essa funcao para outro metodo no futuro).
        lola = json.loads(open(self.patchs_file).read())

        for item in lola:
            texts = ''
            link = ''
            if item['Nome'] == champion:
                texts += self.string_check(item['Patch'])
                texts += self.string_check(item['Sumario'])
                texts += self.string_check(item['Texto'])
                for skill in item['Skills']:
                    texts += self.string_check(skill)
                link += self.string_check(item['Link'])
                tweet_block = []
                tweets = self.create_tweet_blocks(texts, tweet_block)
                tweets.append('Fonte: ' + link)
        return tweets       

    def string_check(self, checker):
        # Trata as strings recolhidas, tirando \n's e \t's. 
        if checker !=  None:
            checker = checker.strip()
            return "\n" + checker
        return ''

    def create_tweet_blocks(self, checker, support):
        # Funcao recursiva que pega todo texto passado e divide em blocos do tamanho ideal de um Tweet.
        if len(checker) > 280:
            #o checker era 275 ate eu perceber q precisava de mais espaco
            support.append(checker[:260] + "(...)")
            return self.create_tweet_blocks(checker[260:], support)
        support.append(checker)
        return support
"""
def main():
    lola = LolaOrganizer("20180909LoLA.json")
    lola.champion_search('Urgot')

if __name__ == "__main__":
    main()
"""