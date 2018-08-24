import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import watson_developer_cloud as wdc
from flask import Flask


app = Flask(__name__)

@app.route('/')
def index():
    return max_tone_value

if __name__=="__main__":
    app.run
 
tone_analyzer = wdc.ToneAnalyzerV3(
  version='2016-05-19',
  username='76776a39-f5a4-4ffc-a415-2d90626252a9',
  password='5ILsVeprCpCE',
  url= "https://gateway.watsonplatform.net/tone-analyzer/api",
)


 
message = input("Input the context you want to test emotional analysis : ")

 
tone=tone_analyzer.tone(message, sentences=False, content_type='text/plain')
 
#assign each tone name and value to its respective category 
emotion_tone={}
language_tone={}
social_tone={}
 
for cat in tone['document_tone']['tone_categories']:
    print('Category:', cat['category_name'])
    if cat['category_name'] == 'Emotion Tone':
        for tone in cat['tones']:
            print('-', tone['tone_name'], tone['score'])
            emotion_tone.update({tone['tone_name']:tone['score']})     
    if cat['category_name'] == 'Social Tone':
        for tone in cat['tones']:
            print('-', tone['tone_name'], tone['score'])
            social_tone.update({tone['tone_name']:tone['score']}) 
    if cat['category_name'] == 'Language Tone':
        for tone in cat['tones']:
            print('-', tone['tone_name'], tone['score'])
            language_tone.update({tone['tone_name']:tone['score']})             
 
 
#find largest value in all tones to adjust the x scale accordingly
max_tone_value = {**emotion_tone, **language_tone, **social_tone}
if max(max_tone_value.values()) > 0.9:
    max_tone_value = 1
else:
    max_tone_value = max(max_tone_value.values())+0.1
 
 
#plot all tones by category
fig = plt.figure(figsize=(7,7))
mpl.style.use('seaborn')
fig.suptitle('Tones by Intensity, scale range: 0(min) - 1(max)', fontsize=14, fontweight='bold')
 
x1=fig.add_subplot(311)
y_pos = np.arange(len(emotion_tone.keys()))
plt.barh(y_pos, list(emotion_tone.values()), align='center', alpha=0.6, color='limegreen')
plt.yticks(y_pos, emotion_tone.keys())
plt.title('Emotion Tone', fontsize=12)
x1.set_xlim([0, max_tone_value])
 
x2=fig.add_subplot(312)
y_pos = np.arange(len(social_tone.keys()))
plt.barh(y_pos, list(social_tone.values()), align='center', alpha=0.6,color='red')
plt.yticks(y_pos, social_tone.keys())
plt.title('Social Tone',fontsize=12)
x2.set_xlim([0, max_tone_value])
 
x3=fig.add_subplot(313)
y_pos = np.arange(len(language_tone.keys()))
plt.barh(y_pos, list(language_tone.values()), height = 0.4, align='center', alpha=0.6, color='deepskyblue')
plt.yticks(y_pos, language_tone.keys())
plt.title('Language Tone',fontsize=12)
x3.set_xlim([0, max_tone_value])
 
plt.tight_layout(pad=0.9, w_pad=0.5, h_pad=1.7)
fig.subplots_adjust(top=0.85, left=0.20)
plt.show()

