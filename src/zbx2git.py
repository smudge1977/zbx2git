import os
from pathlib import Path
from zabbix_utils import ZabbixAPI

ZABBIX_INSTANCE = "DC01"
REPOSITORY = "repository"
FORMAT = "yaml"

def dump2file(path: str, content):
    dir, _, _ = path.rpartition('/')
    print(dir)
    Path(dir).mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        f.writelines(content)

api = ZabbixAPI(url="10.100.100.4/zabbix",
                user=os.getenv('ZABBIX_USER','zbx2git'))

# api.login(token=os.getenv('ZABBIX_TOKEN'))
api.login(user=os.getenv('ZABBIX_USER','zbx2git'), password=os.getenv('ZABBIX_PASSWORD'))


type_ = "template"
templates = api.template.get(
    output=['templateid','name'],
    sortorder="templateid",
    # id="templateid"
)

for template in templates:
    # print(template["templateid"])
    id = template["templateid"]
    content = api.configuration.export(
        options = {
            "templates" : [id],
        },
            # template = [10621],
            
        
        format = FORMAT,
    )

    dump2file(f'{REPOSITORY}/{ZABBIX_INSTANCE}/{type_}/{id}-{template["name"]}.{FORMAT}', content=content)


users = api.user.get(
    output=['userid','name']
)

for user in users:
    print(user['name'])

api.logout()

"""
    {
      "type": "valueMaps",
      "method": "valuemap.get",
      "output": [ "valuemapid", "name" ],
      "sortorder": "valuemapid",
      "id": "valuemapid"
    },
    {
      "type": "templates",
      "method": "template.get",
      "output": [ "templateid", "name" ],
      "sortorder": "templateid",
      "id": "templateid"
    },



/repository/#{inst}/#{cfg[:type]}
        json = JSON.parse(zbx.query(
          :method => "configuration.export",
          :params => {
            :options => {
              cfg[:type] => [ result[cfg[:id]] ],
            },
            :format => 'json'
          }
        ))

"""