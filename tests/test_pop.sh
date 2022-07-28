 #!/bin/bash

curl --header "Connection: close" --url https://fieldday-web.wcer.wisc.edu/wsgi-bin/opengamedata.wsgi/game/AQUALAB/metrics?start_datetime=2022-07-01T00:00&end_datetime=2022-07-02T23:59&metrics=[JobActiveTime,JobCompletionTime,PlayerSummary]
exit 0