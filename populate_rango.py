import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','tango_with_django_project.settings')
import django
django.setup()
from rango.models import Category,Page

def populate():
    business_pages = [
        {'title': 'Vanguard: Investment giant to pay vaccinated workers $1,000','url':'https://www.bbc.co.uk/news/business-58091534','views': 90,'likes':30,'marks':21,
        'description':'Vanguard, one of the world top investment firms, is to pay its US workers $1,000 if they get vaccinated.Staff must prove they have been jabbed by October and will still qualify if they were inoculated before the company made its offer.It speaks to the different approaches US firms are taking to vaccination as the Delta variant of coronavirus surges across the country.',
        'image':'page_images/business_news1.jpg'}, 
        {'title':'Robinhood shares surge 80 percentage amid frenzied trading','url':'https://www.bbc.co.uk/news/business-58091533','views': 84,'likes':35,'marks':12,
        'description':'Shares in the trading platform Robinhood have surged, amid speculation the firm could be seeing the same frenzied trading that surrounded the video game retailer Gamestop.The stock climbed as much as 82 percentage on Wednesday, with trading paused several times due to wild price swings.',
        'image':'page_images/business_news2.jpg'},
        {'title':'Rihanna now officially a billionaire', 'url':'https://www.bbc.co.uk/news/world-us-canada-58092465','views': 45,'likes':39,'marks':18,
        'description':'Rihanna is now officially a billionaire and the wealthiest female musician in the world, according to Forbes.The pop star is worth $1.7 billion (£1.2 billion), with an estimated $1.4 billion coming from the value of her Fenty Beauty cosmetics company.The rest of her fortune mostly comes from lingerie company, Savage x Fenty, worth an estimated $270 million, and her earnings from music and acting.'
        ,'image':'page_images/business_news3.jpg'} 
    ]
    tech_pages = [
        {'title': 'WhatsApp ''view once'' brings disappearing photos and videos','url':'https://www.bbc.co.uk/news/technology-58087379','views': 120,'likes':39,'marks':10,
        'description':'WhatsApp is rolling out a feature that allows users to have photos or videos vanish after they are seen.After the recipient opens the image for the first time, "view once" deletes it, without saving it to a phone.WhatsApp said the feature was aimed at "giving users even more control over their privacy".',
        'image':'page_images/tech_news1.png'}, 
        {'title':'MP Maria Miller wants AI nudifying tool banned','url':'https://www.bbc.co.uk/news/technology-57996910','views': 72,'likes':31,'marks':27,
        'description':'MP Maria Miller wants a parliamentary debate on whether digitally generated nude images need to be banned.It comes as another service which allows users to undress women in photos, using Artificial intelligence (AI), spreads rapidly on social media.',
        'image':'page_images/tech_news2.png'},
        {'title':'Facebook and academics row over data access', 'url':'https://www.bbc.co.uk/news/technology-58086628','views': 105,'likes':77,'marks':37,
        'description':'A row has blown up between Facebook and academics over the use of its data for reporting trends on the social network.Members of the Cybersecurity for Democracy team, based at New York University, tweeted they had had their accounts shut down.Facebook said the tools they had used to gain access to its data violated user privacy.'
        ,'image':'page_images/tech_news3.jpg'}
    ]
    sport_pages = [
        {'title': 'Sky Brown becomes GB is youngest medallist, plus sailing and showjumping golds','url':'https://www.bbc.co.uk/sport/olympics/58082545','views': 150,'likes':71,'marks':32,
        'description':'Thirteen-year-old Sky Brown earned a momentous skateboarding bronze to become Great Britain is youngest Olympic medallist as victories in sailing and showjumping on Wednesday took Team GB''s gold medal tally to 15.',
        'image':'page_images/sport_news1.jpg'}, 
        {'title':'Andre de Grasse claims 200m gold','url':'https://www.bbc.co.uk/sport/olympics/58088922','views': 56,'likes':37,'marks':37,
        'description':'Canada Andre de Grasse won his first gold and fifth Olympic medal overall as he overhauled world champion Noah Lyles in the final 50m of the 200m final.The 26-year-old, who took bronze in the 100m final on Sunday, won in 19.62 seconds, making him the eighth-fastest man in history.',
        'image':'page_images/sport_news2.jpg'},
        {'title':'Great Britain''s Ben Whittaker wins boxing silver after defeat by Arlen Lopez', 'url':'https://www.bbc.co.uk/sport/olympics/58083205','views': 135,'likes':87,'marks':57,
        'description':'Ben Whittaker won Great Britain second boxing silver of Tokyo 2020 after defeat by Cuba Arlen Lopez in the light-heavyweight gold-medal bout.Whittaker, 24, was left in tears on the podium after losing on a split decision to the classy Lopez.'
        ,'image':'page_images/sport_news3.jpg'}
    ]
    cats = {'Business': {'pages': business_pages,'views' : 128, 'likes' : 64,'description':'Real-time reporting of global breaking news, business, economics, finance, finance, and international news. At the same time provide high-quality business analysis and in-depth reports.',
    'image':'category_images/business.jpg'},
    'Tech': {'pages': tech_pages,'views' : 240, 'likes' : 122,'description':'24-hour rolling reports on IT industry, telecommunications, Internet, scientific exploration information, timely and accurate delivery of valuable content.',
    'image':'category_images/tech.jpg'},
    'Sport': {'pages': sport_pages,'views' : 310, 'likes' : 192,'description':'Provide the fastest, most comprehensive and professional sports news and event reports.',
    'image':'category_images/sport.jpg'}
    }

    def add_page(cat,title,url,views,likes,description,marks,image):
        p = Page.objects.get_or_create(category=cat, title=title)[0] 
        p.url = url
        p.views = views
        p.likes = likes
        p.marks = marks
        p.description = description
        p.image = image
        p.save()
        return p
    def add_cat(name,views,likes,description,image):
        c = Category.objects.get_or_create(name = name)[0]
        c.views = views
        c.likes = likes
        c.description = description
        c.image = image
        c.save()
        return c
    for cat, cat_data in cats.items(): 
        c = add_cat(cat,cat_data['views'],cat_data['likes'],cat_data['description'],cat_data['image']) 
        for p in cat_data['pages']: 
            add_page(c, p['title'], p['url'],p['views'],p['likes'],p['description'],p['marks'],p['image']) 
    
    for c in Category.objects.all(): 
        for p in Page.objects.filter(category=c): 
            print(f'- {c}: {p}') 

if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()  
