import os
from pathlib import Path
from zabbix_utils import ZabbixAPI

ZABBIX_INSTANCE = "DC01"
REPOSITORY = "repository"
FORMAT = "yaml"


def dump2file(path: str, content):
    dir, _, _ = path.rpartition("/")
    Path(dir).mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.writelines(content)


def dump_data_template(api: ZabbixAPI):
    type_ = "templates"
    key = "templateid"
    obj_ref_list = api.template.get(
        output=[key, "name"],
        sortorder=key,
    )
    for obj in obj_ref_list:
        id = obj[key]
        content = api.configuration.export(
            options={
                f"{type_}": [obj[key]],
            },
            format=FORMAT,
        )
        print(f'{ZABBIX_INSTANCE}/{type_}/{id}-{obj["name"]}')
        dump2file(
            f'{REPOSITORY}/{ZABBIX_INSTANCE}/{type_}/{id}-{obj["name"]}.{FORMAT}',
            content=content,
        )


def dump_data_valueMaps(api: ZabbixAPI):
    type_ = "valueMaps"
    key = "valuemapid"
    obj_ref_list = api.valuemap.get(
        output=[key, "name"],
    )
    for obj in obj_ref_list:
        id = obj[key]
        content = api.valuemap.get(
            output = "extend",
            selectMappings = "extend",
            valuemapids = [obj[key]],
            
            # format=FORMAT,
        )
        print(f'{ZABBIX_INSTANCE}/{type_}/{id}-{obj["name"]}')
        dump2file(
            f'{REPOSITORY}/{ZABBIX_INSTANCE}/{type_}/{id}-{obj["name"]}.{FORMAT}',
            content=content[0],
        )


api = ZabbixAPI(url="10.100.100.4/zabbix", user=os.getenv("ZABBIX_USER", "zbx2git"))

# api.login(token=os.getenv('ZABBIX_TOKEN'))
api.login(
    user=os.getenv("ZABBIX_USER", "zbx2git"), password=os.getenv("ZABBIX_PASSWORD")
)


# dump_data_template(api)

dump_data_valueMaps(api)
# users = api.user.get(
#     output=['userid','name']
# )

# for user in users:
#     print(user['name'])

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
