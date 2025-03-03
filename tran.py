import asyncio
from googletrans import Translator
async def translate_bulk(text):
    async with Translator() as translator:
        translations = await translator.translate([text], dest='en', src='auto')
        for translation in translations:
            print(translation.src)
            print(translation.origin, ' -> ', translation.text)
            
        return translation.text

if __name__ == "__main__":
    origin = """To students of the Faculty of Information Science

The Center for International Relations has organized the Taiwan Mini Job Fair 2025, which aims to act as a medium for connecting job search and application between students and graduates of the university and entrepreneurs/companies in the Republic of China (Taiwan). The event will feature booths for entrepreneurs/companies on Thursday, January 9, 2024, from 9:30 a.m. to 4:00 p.m. at the lobby on the 1st floor of the Automation Park Building.

In this regard, the Center for International Relations would like to ask for your cooperation in publicizing the event to students and graduates under your departments. Details are in the attached document.

I would like to inform you that
To unsubscribe from this group and stop receiving emails from it, send an email to aai65+unsubscribe@informatics.buu.ac.th."""
    
    translated = asyncio.run(translate_bulk(origin))
    print(translated == origin)