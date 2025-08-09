from inference import Chain
import yf
import json

if __name__=='__main__':
    chain=Chain()
    TICKER="INTC"
    news=yf.fetch_full_news(TICKER)
    news_json=json.dumps(news,indent=4)
    x=chain.infer_news(news_json,TICKER)
    for i in x:
        print(i['article'])
        print(i['reception'])
        print(i['impact'])
        print('-'*50)
