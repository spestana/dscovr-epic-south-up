from __future__ import division, absolute_import, print_function, unicode_literals
import tempfile
from datetime import datetime, timedelta
from epic import EPIC
import os
import glob

def make_animation():
	e = EPIC()
	ENDPOINT = 'http://epic.gsfc.nasa.gov'
	
	# get recent images
	day_before_yesterday = datetime.today() + timedelta(days=-2)
	recent_images = e.get_recent_images(since=day_before_yesterday)
		
	# download each image to a temp directory
	for i, image in enumerate(recent_images):
		n = str(i).rjust(2, '0')
		with tempfile.NamedTemporaryFile(dir='tmp/', prefix=f'tmp{n}_', suffix=f'.png', delete=False) as downloadfile:
			e.download_image(image, downloadfile)
			# Add annotation to image, resize, rotate
			annotation = image['image']
			os.system(f"magick mogrify -resize 1000x1000 -rotate 180 -fill white -gravity South -pointsize 30 -annotate +0+10 {annotation} {downloadfile.name}")

	# list of image magick options we want to use for convert to gif animation
	options = [#'-channel', 'B', '-gamma', '0.90',
			#'-channel', 'R', '-gamma', '1.03',
			'-channel', 'RGB',
			#'-sigmoidal-contrast', '4x5%',
			'-modulate', '100,130,100',
			#'-resize', '1000x1000',
			#'-unsharp', '0x1',
			#'-rotate', '180',
			'-delay', '50',
			'-loop', '0',
			'-dispose', 'previous']
	
	# put all options into string
	options_str= ''
	for element in options:
		options_str += str(element) + ' '
	
	# combine individual frames into an animated gif
	os.system(f'convert {options_str} tmp/*.png animation.gif')
	
	# remove temporary image frames
	tmp_files = glob.glob('tmp/*')
	for f in tmp_files:
		os.remove(f)
		
	return image['image']