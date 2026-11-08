#!/usr/bin/env python3
"""Build the Midad narration; publish nothing unless technical and ASR checks pass."""
import json, re, subprocess, tempfile, unicodedata, wave
from pathlib import Path
from difflib import SequenceMatcher
import numpy as np
from piper import PiperVoice
from faster_whisper import WhisperModel
root=Path(__file__).resolve().parents[1]
media=root/'assets/media'
lines=['كُلُّ فِكْرَةٍ تَسْتَحِقُّ مَسَاحَةً. مِدَاد.',
'خَطِّطْ لِيَوْمِكَ، وَدَوِّنْ أَفْكَارَكَ.',
'صَفَحَاتٌ مُنَقَّطَةٌ، تُرَافِقُ تَفَاصِيلَ يَوْمِكَ.',
'اِبْدَأْ بِصَفْحَةٍ. مِدَاد، مَسَاحَةٌ لِفِكْرَتِكَ.']
voice=PiperVoice.load('/tmp/midad-model/arabic-emirati-female-model.onnx')
tmp=Path(tempfile.mkdtemp(prefix='midad-'))
takes=[];rate=None;durations=[]
for i,sentence in enumerate(lines):
    with wave.open(str(tmp/f'{i}.wav'),'wb') as dst: voice.synthesize_wav(sentence,dst)
    with wave.open(str(tmp/f'{i}.wav'),'rb') as src:
        assert src.getnchannels()==1 and src.getsampwidth()==2
        if rate is None: rate=src.getframerate()
        assert rate==src.getframerate()
        clip=np.frombuffer(src.readframes(src.getnframes()),dtype='<i2').astype(float)/32768
    secs=len(clip)/rate
    if not .65<secs<4.65: raise RuntimeError(f'Bad scene duration: {i}: {secs:.2f}')
    if not .008<float(np.sqrt(np.mean(clip**2)))<.7: raise RuntimeError(f'Bad scene loudness {i}')
    durations.append(round(secs,3));takes.append(clip)
track=np.zeros(rate*20)
for i,clip in enumerate(takes):
    clip=clip.copy()
    fade=min(int(rate*.05),len(clip)//8)
    clip[:fade]*=np.linspace(0,1,fade)
    clip[-fade:]*=np.linspace(1,0,fade)
    offset=int((i*5+.19)*rate)
    track[offset:offset+len(clip)]+=clip
track*=.78/max(np.max(np.abs(track)),1e-12)
if float(np.sqrt(np.mean(track**2)))<.025: raise RuntimeError('Narration too quiet')
wav=tmp/'narration.wav'
with wave.open(str(wav),'wb') as dst:
    dst.setnchannels(1);dst.setsampwidth(2);dst.setframerate(rate)
    dst.writeframes((track*32767).astype('<i2').tobytes())
asr=WhisperModel('base',device='cpu',compute_type='int8')
parts,_=asr.transcribe(str(wav),language='ar',beam_size=5)
heard=' '.join(p.text for p in parts)
def norm(s):
    s=''.join(c for c in unicodedata.normalize('NFD',s) if not unicodedata.combining(c))
    s=re.sub('[إأآٱ]','ا',s).replace('ى','ي').replace('ة','ه')
    return re.sub(r'[^\u0621-\u064a ]+',' ',s).strip()
similarity=SequenceMatcher(None,norm(' '.join(lines)),norm(heard)).ratio()
if similarity<.48: raise RuntimeError(f'ASR mismatch: {similarity:.2f}, heard: {heard}')
out=tmp/'midad.mp4'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(media/'midad-ad.mp4'),
'-i',str(wav),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac',
'-b:a','160k','-ar','48000','-t','20','-movflags','+faststart',str(out)],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)]))
assert abs(float(probe['format']['duration'])-20)<.12
assert [x['codec_name'] for x in probe['streams']]==['h264','aac']
assert probe['streams'][0]['width']==720 and probe['streams'][0]['height']==1280
assert float(probe['streams'][1]['duration'])>19.8
# From here onward, all QA gates have passed.
times=['00:00.000','00:05.000','00:10.000','00:15.000','00:20.000']
vtt='WEBVTT\n\n'+''.join(f'{times[i]} --> {times[i+1]}\n{s}\n\n' for i,s in enumerate(lines))
story=('مِداد — مساحة لفكرتك\nإعلان تجريبي بصوت عربي مولّد آليًا، 20 ثانية\n\n'+
''.join(f'{times[i]} إلى {times[i+1]}\nالتعليق المنطوق: {s}\n\n' for i,s in enumerate(lines))+
'المشاهد: دفتر كحلي، دفتر مفتوح، تفاصيل الدفتر، ولقطة ختامية.\n'+
'عبارة «إعلان تجريبي · منتج افتراضي» ظاهرة طوال المقطع. لا موسيقى.\n')
page=root/'samples/short-ad/index.html'
html=page.read_text()
replacements=[
('فيديو إعلاني رأسي صامت','فيديو إعلاني رأسي بصوت عربي'),
('فيديو صامت، دون موسيقى أو تعليق صوتي','تعليق صوتي عربي مولّد آليًا، دون موسيقى'),
('إعلان مِداد التجريبي، 20 ثانية، صامت','إعلان مِداد التجريبي، 20 ثانية، بصوت عربي'),
('label="النص العربي ووصف المشاهد"','label="نص التعليق الصوتي العربي"'),
('لا يوجد كلام مسموع أو موسيقى أو مؤثرات صوتية. هذا الوصف يشمل النصوص','يوجد تعليق صوتي عربي مولّد آليًا دون موسيقى. هذا الوصف يشمل النصوص'),
('النموذج الصامت مكتمل. لا يتضمن تعليقًا صوتيًا سعوديًا؛ إضافة تعليق\n            بشري أو موسيقى مرخّصة تحتاج قرارًا مستقلًا، وليست جزءًا من النسخة\n            الحالية.',
'أُضيف تعليق صوتي آلي عربي باستخدام صوت إماراتي مرخّص MIT.\n            المحتوى تجريبي لمنتج افتراضي ولا يحتوي على موسيقى.')]
for old,new in replacements:
    if old not in html: raise RuntimeError(f'HTML expected string absent: {old[:30]}')
    html=html.replace(old,new)
readme=root/'README.md'
md=readme.read_text().replace('إعلان مِداد الأصلي الصامت، 20 ثانية','إعلان مِداد الأصلي بصوت عربي، 20 ثانية')
medreadme=media/'README.md'
mr=medreadme.read_text().replace('إعلان صامت أصلي','إعلان أصلي بصوت عربي مولّد آليًا').replace('لا تعليق صوتي أو موسيقى أو لقطات خارجية.','لا موسيقى أو لقطات خارجية.')
mr+='\n## الصوت والترخيص\nالصوت الاصطناعي: vadimbelsky/arabic-emirati-female-piper، يصفه الناشر بترخيص MIT المجيز للاستخدام التجاري. صوت إماراتي لا سعودي، وليس تسجيلًا بشريًا. https://huggingface.co/vadimbelsky/arabic-emirati-female-piper\nالمحرك: Piper 1.8.0، GPL-3.0-or-later؛ لم تُضمّن شيفرته أو الأوزان في المستودع. https://github.com/OHF-Voice/piper1-gpl\nGitHub Actions على مشغّل قياسي في مستودع عام مجاني؛ دون اشتراك أو رصيد مدفوع. لا موسيقى. إعادة تشغيل scripts/render_media.py تعيد الفيديو للصمت؛ أعد سير عمل الصوت بعده.\n'
qa={'voice':'Piper 1.8.0, Emirati female','license':'MIT model; GPL-3.0-or-later engine','commercial_use':True,
'duration':20,'segment_duration_seconds':durations,'peak':round(float(np.max(np.abs(track))),3),
'rms':round(float(np.sqrt(np.mean(track**2))),4),'asr_match':round(similarity,3),'asr_text':heard,
'video_codecs':['h264','aac'],'music':None,'listened_by_human':False,
'caveat':'Automated tests do not guarantee human-natural pronunciation.'}
(media/'midad-ar.vtt').write_text(vtt)
(media/'midad-storyboard.txt').write_text(story)
(media/'midad-voiceover.wav').write_bytes(wav.read_bytes())
(media/'midad-ad.mp4').write_bytes(out.read_bytes())
page.write_text(html);readme.write_text(md);medreadme.write_text(mr)
(root/'docs/midad-voice-qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(qa,ensure_ascii=False,indent=2))