lep photon create -n github-analytics-data -m lepton_data.py
lep photon push -n github-analytics-data
lep deployment remove -n github-analytics-data
lep photon run -n github-analytics-data -dn github-analytics-data --no-traffic-timeout 0 --min-replicas 1 --mount /github-analytics/data:/mnt/data
