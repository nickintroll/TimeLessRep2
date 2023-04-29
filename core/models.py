from channels.layers import get_channel_layer
from django.db import models
from deep_translator import GoogleTranslator
# from .consumers import ChatConsumer


class ChatSession(models.Model):
	channel_name = models.CharField(max_length=100)


class Parameters(models.Model):
	title = models.CharField(max_length=100)
	value = models.CharField(max_length=400)


class TextBlock(models.Model):
	title = models.CharField(max_length=300, unique=True)

	def __str__(self):
		return self.title

langs = (
	('en', 'English'),
	('ru', 'Russian')
)
langs_trans = {
	'en': 'English',
	'ru': 'Russian',
	'English': 'en',
	'Russian': 'ru',
}

class Text(models.Model):
	block = models.ForeignKey(TextBlock, related_name='texts', on_delete=models.CASCADE)
	language = models.CharField(max_length=3, choices=langs)
	text = models.TextField()
	source = models.BooleanField(default=False)

	def save(self, *args, **kwargs):
		if self.source:	
			print('WORK: auto translation...')

			success = False
			for lang in langs:
				if not lang[0] in [self.language, langs_trans[self.language]]:
					print(lang[0],[self.language, langs_trans[self.language]])
					try:
						trsl = GoogleTranslator(source=self.language, target=lang[0], timeout=5).translate
						translated = trsl(self.text)
						success = True
					except Exception as exp:
						print('ERROR: could not translate: ', exp)
	
					if success:
						Text(
							block=self.block,
							language=lang[0],
							text=translated
						).save()
			if success:
				self.source = False

		super().save(*args, kwargs)


"""
for i in lines:
	if i[0] == '-':
		i = i.split('|')
		TextBlock.objects.create(id=i[0].replace('-', ''), title=i[1])


for i in lines:
	if i[0] != '-':
		i = i.split('|')
		block = TextBlock.objects.get(id=int(i[2]))
		print(Text.objects.create(id=i[0], language=i[1], block=block, text=i[3]))
"""