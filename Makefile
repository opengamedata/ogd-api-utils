.PHONY: deploy

deploy-server:
	rsync -vrc ./* fieldday-web.ad.education.wisc.edu:/var/www/wsgi-bin --exclude-from rsync-exclude;
	ssh -t fieldday-web.ad.education.wisc.edu sudo /sbin/service httpd restart

deploy-ogd:
	rsync -vrc ./* fieldday-web.ad.education.wisc.edu:/var/www/wsgi-bin --exclude-from rsync-exclude;
	ssh -t fieldday-web.ad.education.wisc.edu sudo /sbin/service httpd restart

deploy-apis:
	rsync -vrc ./apis/* fieldday-web.ad.education.wisc.edu:/var/www/wsgi-bin/apis/ --exclude-from rsync-exclude;
	ssh -t fieldday-web.ad.education.wisc.edu sudo /sbin/service httpd restart

deploy-dashboard:
	rsync -vrc ./apis/DashboardAPI.py fieldday-web.ad.education.wisc.edu:/var/www/wsgi-bin/apis --exclude-from rsync-exclude;
	ssh -t fieldday-web.ad.education.wisc.edu sudo /sbin/service httpd restart

deploy-indexer:
	rsync -vrc ./store/* fieldday-web.ad.education.wisc.edu:/var/www/opengamedata --exclude-from rsync-exclude;

update-submodules:
	git submodule update --remote
	git add opengamedata/
	git commit -m "Update submodule from remote upstream"