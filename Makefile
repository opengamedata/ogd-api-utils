.PHONY: deploy

deploy-server:
	rsync -vrc ./* fieldday-web.ad.education.wisc.edu:/var/www/wsgi-bin --exclude-from rsync-exclude;

deploy-dashboard:
	rsync -vrc ./apis/DashboardAPI.py fieldday-web.ad.education.wisc.edu:/var/www/wsgi-bin/apis --exclude-from rsync-exclude;

deploy-indexer:
	rsync -vrc ./store/* fieldday-web.ad.education.wisc.edu:/var/www/opengamedata --exclude-from rsync-exclude;
