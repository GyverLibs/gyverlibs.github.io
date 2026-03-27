#pip install PyGithub
import time
import json
import os
from github import Github, Auth

token = os.getenv("PAT_GITHUB")
git = Github(auth=Auth.Token(token))

rep = git.get_repo('GyverLibs/gyverlibs.github.io')
#if 'traf.json' not in str(rep.get_contents('')): rep.create_file('traf.json', 'create traf.json', "{}")
cont = rep.get_contents('traf.json')
data = json.loads(cont.decoded_content.decode())
t = int(time.time()) * 1000
total = 0
repos = git.get_user().get_repos()

for repo in repos:
    if repo.name not in data: data[repo.name] = []
    traf_obj = repo.get_views_traffic()
    traf = traf_obj.views
    if len(traf) < 10: continue
    per_week = sum(traf[i].count for i in range(1, 8))
    data[repo.name].append([t, per_week])
    total += per_week

if 'total' not in data: data['total'] = []
data['total'].append([t, total])
rep.update_file('traf.json', 'update traf.json', json.dumps(data), cont.sha)
exit()