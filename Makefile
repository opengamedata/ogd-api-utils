.PHONY: deploy

deploy-server:
	rsync -vrc ./wsgi/* fieldday-web.ad.education.wisc.edu:/var/www/wsgi-bin --exclude-from rsync-exclude;

deploy-indexer:
	rsync -vrc ./site/* fieldday-web.ad.education.wisc.edu:/var/www/opengamedata --exclude-from rsync-exclude;
