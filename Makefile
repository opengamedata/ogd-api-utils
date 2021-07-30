.PHONY: deploy

deploy:
	rsync -vrc * fieldday-web.ad.education.wisc.edu:/var/www/wsgi-bin --exclude-from rsync-exclude
